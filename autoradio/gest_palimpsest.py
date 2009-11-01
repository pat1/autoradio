#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import logging
from datetime import *

from autoradio_config import *

from django.db.models import Q
from palimpsest.models import Configure
from palimpsest.models import PeriodicSchedule
from palimpsest.models import Schedule
from palimpsest.models import Program

import os,calendar

class gest_palimpsest:

    def __init__ (self,now,minelab):
        """init of palimpsest application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued programs"""
        
        self.radiostation=None
        self.channel=None
        self.mezzo=None
        self.type=None

        self.now = now
        self.minelab = minelab

        ora=self.now.time()
        self.oggi=self.now.date()
        self.giorno=calendar.day_name[self.now.weekday()]

        self.schedule=()
        self.periodicschedule=()

        datesched_min=self.now - timedelta( seconds=60*self.minelab)
        datesched_max=self.now + timedelta( seconds=60*self.minelab)

        if ora < time(12):
            self.ieriodomani=calendar.day_name[datesched_min.weekday()]
        else:
            self.ieriodomani=calendar.day_name[datesched_max.weekday()]

        logging.debug( "PALIMPSEST: elaborate from %s to %s",datesched_min, datesched_max)

        timesched_min=datesched_min.time()
        timesched_max=datesched_max.time()
        logging.debug( "PALIMPSEST: elaborate from %s to %s",timesched_min, timesched_max)


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
            .filter(program__active__exact=True)\
            .order_by('emission_date')


        # retrive the right records relative to periodicschedule
        if (timesched_min < timesched_max):
            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(time__gte=timesched_min)\
                .filter(time__lte=timesched_max)\
                .filter(giorni__name__exact=self.giorno)\
                .filter(program__active__exact=True)\
                .order_by('time')

        else:
            # warning here we are around midnight
            logging.debug("PALIMPSEST: around midnight")

            self.periodicschedule=PeriodicSchedule.objects\
                .filter(Q(start_date__lte=self.oggi) | Q(start_date__isnull=True))\
                .filter(Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True))\
                .filter(Q(time__gte=timesched_min) & Q(giorni__name__exact=self.giorno) |\
                        Q(time__lte=timesched_max) & Q(giorni__name__exact=self.ieriodomani))\
                .filter(program__active__exact=True)\
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
                
        for program in self.schedule:
            logging.debug("PALIMPSEST: schedule %s %s %s", program.program.program, ' --> '\
                              ,program.emission_date.isoformat())


            program.ar_scheduledatetime=program.emission_date

            yield program


        for program in self.periodicschedule:
            logging.debug("PALIMPSEST: periodic schedule %s %s %s", program.program.program, ' --> '\
                              ,  program.time.isoformat())

            program.ar_scheduledatetime=datetime.combine(self.oggi, program.time)

            # if we are around midnight we have to check the correct date (today, iesterday, tomorrow)
            datesched_min=self.now - timedelta( seconds=60*self.minelab)
            datesched_max=self.now + timedelta( seconds=60*self.minelab)
            if not (datesched_min <= program.ar_scheduledatetime and  program.ar_scheduledatetime <= datesched_max  ):
                if self.now.time() < time(12):
                    program.ar_scheduledatetime=datetime.combine(datesched_min.date(), program.time)
                else:
                    program.ar_scheduledatetime=datetime.combine(datesched_max.date(), program.time)


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
    now=datetime.now()


    # get the programs of my insterest
    pro=gest_palimpsest(now,minelab)

    for info in pro.get_info():
        print "info: ",info

    # I do a list
    for program in pro.get_program():
        
        #pass
        print program
        print program.ar_scheduledatetime
        print program.ar_length

        print "program",program.program

        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
