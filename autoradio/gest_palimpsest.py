#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'
from django.conf import settings

import logging
from datetime import *

from .autoradio_config import *

from django.db.models import Q
from .programs.models import Configure
from .programs.models import PeriodicSchedule
from .programs.models import AperiodicSchedule

import os,calendar

class gest_palimpsest(object):

    def __init__ (self,datetimeelab,minelab):
        """init of palimpsest application:
        datetimeelab : datetime to elaborate
        execute the right data retrival to get the schedued programs"""
        
        self.radiostation=None
        self.channel=None
        self.mezzo=None
        self.type=None

        self.datetimeelab = datetimeelab
        self.oggi=self.datetimeelab.date()

        ora=datetimeelab.time()

        self.giorno=calendar.day_name[self.datetimeelab.weekday()]

        self.schedule=()
        self.periodicschedule=()

        self.datesched_min=self.datetimeelab - timedelta( seconds=60*minelab)
        self.datesched_max=self.datetimeelab + timedelta( milliseconds=60000*minelab-1) #1 millisecond tollerance
        self.timesched_min=self.datesched_min.time()
        self.timesched_max=self.datesched_max.time()

        logging.debug( "PALIMPSEST: elaborate date from %s to %s",self.datesched_min, self.datesched_max)
        logging.debug( "PALIMPSEST: elaborate time from %s to %s",self.timesched_min, self.timesched_max)


        if (Configure.objects.filter(active__exact=False).count() == 1):
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            return


        # retrive the right records relative to schedule
        self.schedule=AperiodicSchedule.objects.select_related()\
            .filter(emission_date__gte=self.datesched_min)\
            .filter(emission_date__lte=self.datesched_max)\
            .filter(show__active__exact=True)\
            .order_by('emission_date')



        # retrive the right records relative to periodicschedule
        if (self.timesched_min < self.timesched_max):
            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(time__gte=self.timesched_min)\
                .filter(time__lte=self.timesched_max)\
                .filter(giorni__name__exact=self.giorno)\
                .filter(show__active__exact=True)\
                .order_by('time')

        else:
            # warning here we are around midnight
            logging.debug("PALIMPSEST: around midnight")

            domani=calendar.day_name[self.datesched_max.weekday()]

            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(Q(time__gte=self.timesched_min) & Q(giorni__name__exact=self.giorno) |\
                        Q(time__lte=self.timesched_max) & Q(giorni__name__exact=domani))\
                .filter(show__active__exact=True)\
                .order_by('time')


        infos=Configure.objects.filter(active__exact=True)
        if (infos.count() == 1):

            for info in infos:

                self.radiostation=info.radiostation
                self.channel=info.channel
                self.mezzo=info.mezzo
                self.type=info.type


    def get_program(self):
        "iterable to get programs"

        ora=self.datetimeelab.time()
                
        for program in self.schedule:
            logging.debug("PALIMPSEST: schedule %s %s", program.show.title, ' --> '\
                              ,program.emission_date.isoformat())


            program.ar_scheduledatetime=program.emission_date

            yield program


        for program in self.periodicschedule:
            logging.debug("PALIMPSEST: periodic schedule %s %s", program.show.title, ' --> '\
                              ,  program.time.isoformat())


            if (self.timesched_min < self.timesched_max):

                program.ar_scheduledatetime=datetime.combine(self.datesched_min.date(), program.time)
                
            else:
                # we are around midnight we have to check the correct date (today, tomorrow)

                if program.time > time(12):
                    program.ar_scheduledatetime=datetime.combine(self.datesched_min.date(), program.time)
                else:
                    program.ar_scheduledatetime=datetime.combine(self.datesched_max.date(), program.time)

            yield program



    def get_info(self):
        """ get station info

        yield:
        radiostation
        channel
        mezzo
        type
        """
        
        yield self.radiostation
        yield self.channel
        yield self.mezzo
        yield self.type


def main():

    logging.basicConfig(level=logging.DEBUG,)
    # time constants
    datetimeelab=datetime.now()
    minelab=60*4

    # get the programs of my insterest
    pro=gest_palimpsest(datetimeelab,minelab)

    for info in pro.get_info():
        print("info: ",info)

    # I do a list
    for program in pro.get_program():
        
        #pass
        print(program)
        print(program.ar_scheduledatetime)
        print(program.program.length)
        print("program",program.program)
        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
