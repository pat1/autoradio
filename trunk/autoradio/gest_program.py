#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'
from django.conf import settings

import logging
from datetime import *

from autoradio_config import *

from programs.models import Schedule
from programs.models import ScheduleDone
from programs.models import Show
from programs.models import Configure

# to get metadata from audio files
import mutagen
import os

class gest_program:

    def __init__ (self,now,minelab):
        """init of program application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued programs"""
        
        self.now = now
        self.minelab = minelab
        ora=self.now.time()
        self.schedules=()

        datesched_min=self.now - timedelta( seconds=60*self.minelab)
        datesched_max=self.now + timedelta( milliseconds=60000*self.minelab-1) # 1 millisecond tollerance
        timesched_min=datesched_min.time()
        timesched_max=datesched_max.time()
        logging.debug( "PROGRAM: elaborate from %s to %s",datesched_min,datesched_max)

        if (Configure.objects.filter(active__exact=False).count() == 1):
            self.schedules=()
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            self.schedules=()
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            self.schedules=()
            return

        # estraggo i record di mio interesse
        self.schedules=Schedule.objects.select_related()\
            .filter(emission_date__gte=datesched_min)\
            .filter(emission_date__lte=datesched_max)\
            .filter(episode__active__exact=True)\
            .order_by('emission_date')
#               .filter(emission_done__isnull=True).order_by('emission_date')

    def get_program(self):
        "iterate to get program"

        for schedule in self.schedules:
#            logging.debug("PROGRAM: %s %s %s", programma.program.file , ' --> '\
#                              ,  programma.emission_date.isoformat())
            logging.debug("PROGRAM: %s %s %s", schedule.episode , ' --> '\
                              ,  schedule.emission_date.isoformat())

            firth=True
            for enclosure in schedule.episode.enclosure_set.order_by('id'):
                logging.debug("PROGRAM: files: %s", enclosure.file.path)
                ar_filename=enclosure.file.path
                ar_url=enclosure.file.url
                ar_title=schedule.episode.show.title+" / "\
                    +schedule.episode.title+" / "\
                    +enclosure.title

                query=ScheduleDone.objects.filter(enclosure=enclosure,schedule=schedule)

                if query:
                    scheduledone=query.all()[0]
                else:
                    #create new entry in table if necessary
                    scheduledone=ScheduleDone(schedule=schedule,enclosure=enclosure)
                    scheduledone.save()

                ar_emission_done=scheduledone.emission_done

                # calcolo la lunghezza del programma
                try:
                    ar_length=mutagen.File(ar_filename).info.length
                    logging.debug("PROGRAM: elaborate time length: %s",ar_length)
                except:
                    logging.error("PROGRAM: error establish time length; use an estimation %s", ar_filename)
                    ar_length=3600

                # the schedule time is postponed every enclosure
                if firth:
                    ar_scheduledatetime=schedule.emission_date
                    lengthold=ar_length
                    firth=False

                else:
                   ar_scheduledatetime=schedule.emission_date+timedelta(seconds=lengthold)

                programma=scheduledone
                programma.ar_filename=ar_filename
                programma.ar_url=ar_url
                programma.ar_length=ar_length
                programma.ar_title=ar_title
                programma.ar_emission_done=ar_emission_done
                programma.ar_scheduledatetime=ar_scheduledatetime


                yield programma



def main():

    logging.basicConfig(level=logging.DEBUG,)
    # time constants
    now=datetime.now()

    #select the programs
    pro=gest_program(now,minelab)
    
    # do a list
    for programma in pro.get_program():
        
        #pass

        print programma.ar_filename
        print programma.ar_url
        print programma.ar_scheduledatetime
        print programma.ar_length

        #programma.program.get_file_filename()

        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
