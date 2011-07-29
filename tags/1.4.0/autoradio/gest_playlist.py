#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import logging
from datetime import *

from autoradio_config import *

from django.db.models import Q
from playlists.models import Configure
from playlists.models import PeriodicSchedule
from playlists.models import Schedule
from playlists.models import Playlist

if (player == "amarok") :
    from autoradiod import amarok

import os,calendar

class gest_playlist:

    def __init__ (self,now,minelab):
        """init of playlist application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued playlists"""
        
        self.now = now
        self.minelab = minelab

        ora=self.now.time()
        self.oggi=self.now.date()
        self.giorno=calendar.day_name[self.now.weekday()]

        self.schedule=()
        self.periodicschedule=()

        datesched_min=self.now - timedelta( seconds=60*self.minelab)
        datesched_max=self.now + timedelta( milliseconds=60000*self.minelab-1) # 1 millisecond tollerance

        if ora < time(12):
            self.ieriodomani=calendar.day_name[datesched_min.weekday()]
        else:
            self.ieriodomani=calendar.day_name[datesched_max.weekday()]

        logging.debug( "PLAYLIST: elaborate from %s to %s",datesched_min, datesched_max)

        timesched_min=datesched_min.time()
        timesched_max=datesched_max.time()
        logging.debug( "PLAYLIST: elaborate from %s to %s",timesched_min, timesched_max)


        if (Configure.objects.filter(active__exact=False).count() == 1):
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            return


        # retrive the right records relative to schedule
        self.schedule=Schedule.objects.select_related()\
            .filter(emission_date__gte=datesched_min)\
            .filter(emission_date__lte=datesched_max)\
            .filter(playlist__active__exact=True)\
            .order_by('emission_date')


        # retrive the right records relative to periodicschedule
        if (timesched_min < timesched_max):
            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(time__gte=timesched_min)\
                .filter(time__lte=timesched_max)\
                .filter(giorni__name__exact=self.giorno)\
                .filter(playlist__active__exact=True)\
                .order_by('time')

        else:
            # warning here we are around midnight
            logging.debug("PLAYLIST: around midnight")

            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(Q(time__gte=timesched_min) & Q(giorni__name__exact=self.giorno) |\
                        Q(time__lte=timesched_max) & Q(giorni__name__exact=self.ieriodomani))\
                .filter(playlist__active__exact=True)\
                .order_by('time')


#            self.periodicschedule=PeriodicSchedule.objects\
#                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
#                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
#                .filter(Q(time__gte=timesched_min)   | Q(time__lte=timesched_max))\
#                .filter(Q(giorni__name__exact=self.giorno) | Q(giorni__name__exact=self.ieriodomani))\
#                .filter(playlist__active__exact=True)\
#                .order_by('time')

 
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

            playlist.ar_scheduledatetime=datetime.combine(self.oggi, playlist.time)

            # if we are around midnight we have to check the correct date (today, iesterday, tomorrow)
            datesched_min=self.now - timedelta( seconds=60*self.minelab)
            datesched_max=self.now + timedelta( seconds=60*self.minelab)
            if not (datesched_min <= playlist.ar_scheduledatetime and  playlist.ar_scheduledatetime <= datesched_max  ):
                if self.now.time() < time(12):
                    playlist.ar_scheduledatetime=datetime.combine(datesched_min.date(), playlist.time)
                else:
                    playlist.ar_scheduledatetime=datetime.combine(datesched_max.date(), playlist.time)

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

    logging.basicConfig(level=logging.DEBUG,)
    # time constants
    now=datetime.now()

    # get the playlists of my insterest
    pla=gest_playlist(now,minelab)
    
    # I do a list
    for playlist in pla.get_playlist():
        
        #pass
        print playlist
        print playlist.ar_filename
        print playlist.ar_scheduledatetime
        print playlist.ar_length

        print "playlist",playlist.playlist
        #.program.get_file_filename()

        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
