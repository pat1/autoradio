#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# GPL. (C) 2007-2009 Paolo Patruno.

import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'
from django.conf import settings

import logging
import datetime
from .autoradio_config import *
from django.db.models import Q
from .spots.models import Configure
from .spots.models import Spot
from .spots.models import Fascia
from .spots.models import Giorno
import time

#used to get metadata from audio files
import mutagen
import tempfile,shutil


class gest_spot(object):

    def __init__ (self,now,minelab,playlistdir):
        """init of spot application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued spots"""

        import calendar

        playlistpath=os.path.join(settings.MEDIA_ROOT, playlistdir)

        try: # Create the date-based directory if it doesn't exist.
            os.makedirs(playlistpath)
        except OSError: # Directory probably already exists.
            pass


        self.now=now
        self.minelab=minelab
        self.playlistpath=playlistpath

        ora=self.now.time()
        self.oggi=self.now.date()
        self.giorno=calendar.day_name[self.now.weekday()]

        datesched_min=self.now - datetime.timedelta( seconds=60*self.minelab)
        datesched_max=self.now + datetime.timedelta( milliseconds=60000*self.minelab-1) # 1 millisec tollerance
        logging.debug( "SPOT: elaborate from %s to %s",datesched_min, datesched_max)
        timesched_min=datesched_min.time()
        timesched_max=datesched_max.time()
        logging.debug( "SPOT: elaborate from %s to %s",timesched_min, timesched_max)


        if (Configure.objects.filter(active__exact=False).count() == 1):
            self.fasce=()
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            self.fasce=()
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            self.fasce=()
            return


        if (timesched_min < timesched_max):
            self.fasce=Fascia.objects.filter(\
                Q(emission_time__gte=timesched_min),Q( emission_time__lte=timesched_max),\
                Q(active__exact = True)).order_by('emission_time')
        else:
           # here we are around midnight
            self.fasce=Fascia.objects.filter(\
                Q(emission_time__gte=timesched_min)|Q( emission_time__lte=timesched_max),\
                Q(active__exact = True)).order_by('emission_time')

        
    def get_fasce(self,genfile=True):

        for fascia in self.fasce:

            self.fascia=fascia

            # count the spots
            self.ar_spots_in_fascia=self.count_spots()
            self.ar_filename,self.ar_url=self.get_fascia_playlist_media(genfile)

            self.ar_scheduledatetime=datetime.datetime.combine(self.oggi, fascia.emission_time,tzinfo=None)

            # if we are around midnight we have to check the correct date (today, iesterday, tomorrow)
            datesched_min=self.now - datetime.timedelta( seconds=60*self.minelab)
            datesched_max=self.now + datetime.timedelta( seconds=60*self.minelab)
            if not (datesched_min <= self.ar_scheduledatetime and  self.ar_scheduledatetime <= datesched_max  ):
                if self.now.time() < datetime.time(12):
                    self.ar_scheduledatetime=datetime.datetime.combine(datesched_min.date(), fascia.emission_time,tzinfo=None)
                else:
                    self.ar_scheduledatetime=datetime.datetime.combine(datesched_max.date(), fascia.emission_time,tzinfo=None)

            self.ar_emission_done=fascia.emission_done
            yield fascia


    def get_prologhi(self):

        prologhi= self.fascia.spot_set.filter(Q(active__exact = True),\
                                    Q(start_date__lte=self.now) | Q(start_date__isnull=True),\
                                    Q(end_date__gte=self.now) | Q(end_date__isnull=True),\
                                    Q(giorni__name__exact=self.giorno) , Q(prologo__exact=True)).order_by('priorita')

        for prologo in prologhi:
            logging.debug( 'SPOT: prologo: %s',prologo)
            yield prologo



    def count_spots(self):

        return self.fascia.spot_set.filter(Q(active__exact = True),\
                                    Q(start_date__lte=self.now) | Q(start_date__isnull=True),\
                                    Q(end_date__gte=self.now) | Q(end_date__isnull=True),\
                                    Q(giorni__name__exact=self.giorno)).exclude(prologo__exact=True)\
                                    .exclude(epilogo__exact=True).count()

        

    def get_spots(self):

        spots=self.fascia.spot_set.filter(Q(active__exact = True),\
                                    Q(start_date__lte=self.now) | Q(start_date__isnull=True),\
                                    Q(end_date__gte=self.now) | Q(end_date__isnull=True),\
                                    Q(giorni__name__exact=self.giorno)).exclude(prologo__exact=True)\
                                    .exclude(epilogo__exact=True).order_by('priorita')

        for spot in spots:
            logging.debug('SPOT: spot: %s',spot)
            yield spot



    def get_epiloghi(self):

        epiloghi=self.fascia.spot_set.filter(Q(active__exact = True),\
                                    Q(start_date__lte=self.now) | Q(start_date__isnull=True),\
                                    Q(end_date__gte=self.now) | Q(end_date__isnull=True),\
                                    Q(giorni__name__exact=self.giorno) , Q(epilogo__exact=True)).order_by('priorita')
        for epilogo in epiloghi:
            logging.debug ('SPOT: epilogo: %s',epilogo)
            yield epilogo


    def get_fascia_spots(self):

        if (self.ar_spots_in_fascia == 0):
            # I have found an empty fascia
            return

        for prologo in self.get_prologhi():
            yield prologo

        for spot in self.get_spots():
            yield spot

        for epilogo in self.get_epiloghi():
            yield epilogo


    def get_fascia_playlist_media(self,genfile=True):

        name=self.fascia.name+".m3u"
        url=os.path.join(os.path.join(settings.MEDIA_URL, playlistdir),name)
        playlistname =os.path.join(self.playlistpath,name)

        if genfile :
            #        os.umask(002)
            #        f = open(playlistname, "w")
            fd,tmpfile=tempfile.mkstemp()
            f=os.fdopen(fd,"w")
            #        f = open(tmpfile, "w")
            #        f=tempfile.TemporaryFile()

        length=0

        for spot in self.get_fascia_spots():
            filename=spot.file.path
#            filename=spot.get_file_filename()
            #print >>f, os.path.basename(filename)
            logging.debug( "SPOT: include %s", filename)

            if genfile :
                # this work if LANG is set
                #f.write(os.path.basename(filename.encode(sys.getfilesystemencoding())))
                #f.write(os.path.basename(filename.encode("UTF-8")))
                f.write(filename)
                f.write("\n")

            # calcolo la lunghezza della fascia
            try:
                with open(filename,"rb") as mutagenfile:
                    onelength=mutagen.File(mutagenfile).info.length
                    logging.debug("SPOT: computed the partial time length: %d",onelength)
                    length=length+onelength
            except:

                logging.error( "SPOT: error establish time length; use an estimation %s", filename)
       	        length=length+30      # default for one spot

        self.ar_length=length
        logging.debug("SPOT: computed total time length: %d",self.ar_length)

        if genfile :
            f.close()
            os.chmod(tmpfile,0o644)


            #sometime I get:
            #shutil.move(tmpfile,playlistname)
            #File "/usr/lib64/python2.7/shutil.py", line 301, in move
            #copy2(src, real_dst)
            #File "/usr/lib64/python2.7/shutil.py", line 130, in copy2
            #copyfile(src, dst)
            #File "/usr/lib64/python2.7/shutil.py", line 83, in copyfile
            #with open(dst, 'wb') as fdst:
            #    IOError: [Errno 11] Risorsa temporaneamente non disponibile: u'/home/autoradio/media/pubblicita/ore 13.30.m3u'

            # so I try to do it in a delayed loop

            ntry=0
            while True:
                try:
                    shutil.move(tmpfile,playlistname)
                    logging.debug("SPOT: moved the playlist %s in %s",tmpfile,playlistname) 
                    break
                except:
                    logging.warning("SPOT: error moving the playlist %s in %s",tmpfile,playlistname) 
                    ntry +=1
                    if ntry > 5:
                        logging.error("SPOT: cannot move the playlist %s in %s",tmpfile,playlistname)
                        break
                        time.sleep(1)

        return playlistname,url


def main():

    logging.basicConfig(level=logging.DEBUG,)
    now=datetime.datetime.now()

    spots=gest_spot(now,minelab,"/tmp/")

    for fascia in spots.get_fasce(genfile=True):
        #print "elaborate fascia >>",fascia

        for spot in spots.get_fascia_spots():
            pass
            #print "fascia and spot ->",spots.fascia,spot

        print(spots.ar_filename)
        print(spots.ar_scheduledatetime)
        print(spots.ar_length)
        print(spots.ar_spots_in_fascia)


if __name__ == '__main__':
    main()  # (this code was run as script)
