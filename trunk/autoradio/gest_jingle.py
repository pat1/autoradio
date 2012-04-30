#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
# GPL. (C) 2007-2009 Paolo Patruno.

import logging
from datetime import *

from autoradio_config import *

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from itertools import *
import calendar

from jingles.models import Configure
from jingles.models import Jingle
from jingles.models import Giorno

# used to get metadata from audio files
import mutagen

import os

freq_default=time(00,15,00)

def time_iterator(datesched_min,datesched_max,emission_freq):

    datai=datesched_min.date()
    delta=timedelta(hours=emission_freq.hour,minutes=emission_freq.minute,\
                    seconds=emission_freq.second)

    datac=datetime.combine(datai,time(00,00,00))
    
    while datac < datesched_min:
        datac=datac+delta

    yield datac

    while datesched_max>= datac:
        datac=datac+delta
        yield datac
    

class gest_jingle:
            
    def __init__ (self,now,minelab):
        """init of jingle application:
        now : currenti datetime
        minelab: minutes to elaborate 
        execute the right data retrival to get the schedued jingles"""

        self.now=now
        self.minelab=minelab

        self.ora=now.time()
        self.oggi=now.date()
        self.giorno=calendar.day_name[now.weekday()]

        self.datesched_min=self.now - timedelta( seconds=60*self.minelab)
        self.datesched_max=self.now + timedelta( seconds=60*self.minelab)
        logging.debug( "JINGLE: elaborate from %s to %s",self.datesched_min, self.datesched_max)
        #self.timesched_min=self.datesched_min.time()
        #self.timesched_max=self.datesched_max.time()
        #logging.debug( "JINGLE: elaborate from %s to %s",timesched_min, timesched_max)

        try:
            self.emission_freq = Configure.objects.get().emission_freq

        except ObjectDoesNotExist:
            logging.warning( "JINGLE: emission_freq doesn't exist. Setting default")
            self.emission_freq = freq_default

            logging.debug("JINGLE: frequenza di emissione %s",self.emission_freq)

        if (Configure.objects.filter(active__exact=False).count() == 1):
            self.jingles=()
            return


#todo: ma i NULL nel sort dove stanno? all'inizio o alla fine?
#todo: l'order by qui non funziona in quanto vale praticamente sempre
#quello che è stato emesso piu' in la nel tempo
#la priorità di fatto non viene considerata


#        if (timesched_min < timesched_max):
        # we select every jingle active at "now"
        # if not selected some time limits is like 00 for start and 24 for end
        # warning: if you set 18:00 for start and nothing for end it start 18:00 and stop at 24:00
        self.jingles= Jingle.objects.filter\
            (Q(start_date__lte=self.oggi) | Q(start_date__isnull=True),\
             Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True),\
             Q(start_time__lte=self.ora)  | Q(start_time__isnull=True),\
             Q(end_time__gte=self.ora)    | Q(end_time__isnull=True),\
             Q(giorni__name__exact=self.giorno) , Q(active__exact=True))\
             .order_by('emission_done','priorita')

# TODO: we have to add case were start_time > end_time

# this is only a special case; no good
#        else:
#            # warning here we are around midnight
#            # we select every jingle active at "now"
#            # but we have a value of 24 and 00 for implicit max and min
#            self.jingles= Jingle.objects.filter\
#                (Q(start_date__lte=self.oggi) | Q(start_date__isnull=True),\
#                 Q(end_date__gte=self.oggi)   | Q(end_date__isnull=True),\
#                 Q(start_time__lte=self.ora)  | Q(start_time__isnull=True) | Q(end_time__gte=self.ora) | Q(end_time__isnull=True),\
#                 Q(giorni__name__exact=self.giorno) , Q(active__exact=True))\
#                 .order_by('emission_done','priorita')


    def get_jingle(self):

        many_jingles=cycle(self.jingles)

#        for datac in time_iterator(self.datesched_min,self.datesched_max,self.emission_freq):
        for datac in time_iterator(self.now,self.datesched_max,self.emission_freq):

            jingle=many_jingles.next()
            jingle.ar_filename=jingle.file.path
            jingle.ar_url=jingle.file.url
#            jingle.ar_filename=jingle.get_file_filename()
            jingle.ar_scheduledatetime=datac
            jingle.ar_emission_done=jingle.emission_done

            # elaborate the media time length
	    try:
            	jingle.ar_length=mutagen.File(jingle.ar_filename).info.length
                logging.debug("JINGLE: time length: %s",jingle.ar_length)
	    except:
                logging.error("JINGLE: error establish time length; use an estimation %s", jingle.ar_filename)
            	jingle.ar_length=30

            yield jingle


def main():

    now=datetime.now()
    jingles=gest_jingle(now,minelab)
    
    for jingle in jingles.get_jingle():

        print jingle.ar_filename
        print jingle.ar_url
        print jingle.ar_scheduledatetime
        print jingle.ar_length

if __name__ == '__main__':
    main()  # (this code was run as script)
