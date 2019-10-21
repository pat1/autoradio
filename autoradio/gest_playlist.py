#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2007-2009 Paolo Patruno.

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import object
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'
from django.conf import settings

import logging
import datetime

from .autoradio_config import *

from django.db.models import Q
from .playlists.models import Configure
from .playlists.models import PeriodicSchedule
from .playlists.models import Schedule
from .playlists.models import Playlist

if (player == "amarok") :
    from autoradiod import amarok

import os,calendar

class gest_playlist(object):

    def __init__ (self,now,minelab):
        """init of playlist application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued playlists"""
        
        self.now = now

        ora=self.now.time()
        self.oggi=self.now.date()
        self.giorno=calendar.day_name[self.now.weekday()]

        self.schedule=()
        self.periodicschedule=()

        self.datesched_min=self.now - datetime.timedelta( seconds=60*minelab)
        self.datesched_max=self.now + datetime.timedelta( milliseconds=60000*minelab-1) # 1 millisecond tollerance

        self.timesched_min=self.datesched_min.time()
        self.timesched_max=self.datesched_max.time()

        logging.debug( "PLAYLIST: elaborate date from %s to %s",self.datesched_min, self.datesched_max)
        logging.debug( "PLAYLIST: elaborate time from %s to %s",self.timesched_min, self.timesched_max)

        if (Configure.objects.filter(active__exact=False).count() == 1):
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            return


        # retrive the right records relative to schedule
        self.schedule=Schedule.objects.select_related()\
            .filter(emission_date__gte=self.datesched_min)\
            .filter(emission_date__lte=self.datesched_max)\
            .filter(playlist__active__exact=True)\
            .order_by('emission_date')


        # retrive the right records relative to periodicschedule
        if (self.timesched_min < self.timesched_max):
            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(time__gte=self.timesched_min)\
                .filter(time__lte=self.timesched_max)\
                .filter(giorni__name__exact=self.giorno)\
                .filter(playlist__active__exact=True)\
                .order_by('time')

        else:
            # warning here we are around midnight
            logging.debug("PLAYLIST: around midnight")

            ieri=str(calendar.day_name[self.datesched_min.weekday()])
            domani=str(calendar.day_name[self.datesched_max.weekday()])
            
            self.periodicschedule=PeriodicSchedule.objects.filter \
                (Q(start_date__lte=self.oggi) | Q(start_date__isnull=True),\
                 Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True),\
                 (Q(time__gte=self.timesched_min) & Q(giorni__name__exact=ieri))\
                     |\
                 (Q(time__lte=self.timesched_max) & Q(giorni__name__exact=domani))\
                     ,\
                 playlist__active__exact=True)\
                 .order_by('time')

 
    def get_playlist(self):
        "iterable to get playlist"
                
        for playlist in self.schedule:
            logging.debug("PLAYLIST: schedule %s %s %s", playlist.playlist.playlist, ' --> '\
                              ,playlist.emission_date.isoformat())


            # amarok vuole il nome della playlist che deve gia' esistere del suo elenco
            # gli altri vogliono il file della playlist
            if (player == "amarok"):
                playlist.ar_filename=playlist.playlist.playlist
            else:
                playlist.ar_filename=playlist.playlist.file.path

            playlist.ar_url=playlist.playlist.file.url
            playlist.ar_scheduledatetime=playlist.emission_date
            playlist.ar_emission_done=playlist.emission_done

#            # calcolo la lunghezza del programma
#            relpath= os.path.basename(playlist.ar_filename)
#            basedir=os.path.dirname(playlist.ar_filename)

#	    try:
#            	meta = metadata.metadata_from_file(relpath, \
#                   basedir, tracknrandtitlere, postprocessors)
#            	playlist.ar_length=meta.length
#	    except:
#            	playlist.ar_length=3600

            playlist.ar_length=playlist.length
            if  playlist.ar_length is None : playlist.ar_length=3600*24-1

            playlist.ar_shuffle=playlist.shuffle

            yield playlist


        for playlist in self.periodicschedule:
            logging.debug("PLAYLIST: periodic schedule %s %s %s", playlist.playlist.playlist, ' --> '\
                              ,  playlist.time.isoformat())

            # amarok vuole il nome della playlist che deve gia' esistere del suo elenco
            # gli altri vogliono il file della playlist
            if (player == "amarok"):
                playlist.ar_filename=playlist.playlist.playlist
            else:
                playlist.ar_filename=playlist.playlist.file.path

            playlist.ar_url=playlist.playlist.file.url

            #print self.timesched_min, self.timesched_max

            if (self.timesched_min < self.timesched_max):

                #print self.datesched_min.date()
                #print playlist.time

                playlist.ar_scheduledatetime=datetime.datetime.combine(self.datesched_min.date(), playlist.time)
                
            else:
                # we are around midnight we have to check the correct date (today, tomorrow)

                if playlist.time > datetime.time(12):
                    playlist.ar_scheduledatetime=datetime.datetime.combine(self.datesched_min.date(), playlist.time)
                else:
                    playlist.ar_scheduledatetime=datetime.datetime.combine(self.datesched_max.date(), playlist.time)

            playlist.ar_emission_done=playlist.emission_done

#            # calcolo la lunghezza del programma
#            relpath= os.path.basename(playlist.ar_filename)
#            basedir=os.path.dirname(playlist.ar_filename)

#	    try:
#            	meta = metadata.metadata_from_file(relpath, \
#                   basedir, tracknrandtitlere, postprocessors)
#            	playlist.ar_length=meta.length
#	    except:
#            	playlist.ar_length=3600

            playlist.ar_length=playlist.length
            if  playlist.ar_length is None : playlist.ar_length=3600*24-1
            playlist.ar_shuffle=playlist.shuffle

            yield playlist



def main():

#    logging.basicConfig(level=logging.DEBUG,)
    logging.basicConfig(level=logging.INFO,)

    # time constants
    now=datetime.datetime.now()
    for hour in (0,3,6,9,12,15,18,21):

        now=now.replace(hour=hour)
        print()
        print("Runnig for date: ",now)

        # get the playlists of my insterest
        pla=gest_playlist(now,minelab)
    
        # I do a list
        for playlist in pla.get_playlist():

            print("--------------------------------")
            print("found schedule: ",playlist)
            print(playlist.ar_filename)
            print(playlist.ar_url)
            print(playlist.ar_scheduledatetime)
            print(playlist.ar_length)
            print("playlist",playlist.playlist)
            #.program.get_file_filename()
            print("--------------------------------")
        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
