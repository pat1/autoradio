#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import logging
from datetime import *

from autoradio_config import *

from django.db.models import Q
from programs.models import Schedule
from programs.models import Program
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

        datesched_min=self.now - timedelta( seconds=60*self.minelab)
        datesched_max=self.now + timedelta( milliseconds=60000*self.minelab-1) # 1 millisecond tollerance
        timesched_min=datesched_min.time()
        timesched_max=datesched_max.time()
        logging.debug( "PROGRAM: elaborate from %s to %s",datesched_min,datesched_max)

        if (Configure.objects.filter(active__exact=False).count() == 1):
            self.schedule=()
            return
        #todo: the use of ora here is not exact
        if (Configure.objects.filter(emission_starttime__gt=ora).count() == 1) :
            self.schedule=()
            return
        if (Configure.objects.filter(emission_endtime__lt=ora).count() == 1):
            self.schedule=()
            return

        # estraggo i record di mio interesse
        self.schedule=Schedule.objects.select_related()\
            .filter(emission_date__gte=datesched_min)\
            .filter(emission_date__lte=datesched_max)\
            .filter(program__active__exact=True)\
            .order_by('emission_date')
#               .filter(emission_done__isnull=True).order_by('emission_date')

    def get_program(self):
        "iterale to get program"
                
        for programma in self.schedule:
            logging.debug("PROGRAM: %s %s %s", programma.program.file , ' --> '\
                              ,  programma.emission_date.isoformat())

            logging.debug("PROGRAM: %s", programma.program.file.path)

            programma.ar_filename=programma.program.file.path
            programma.ar_scheduledatetime=programma.emission_date
            programma.ar_emission_done=programma.emission_done

            # calcolo la lunghezza del programma
	    try:
                programma.ar_length=mutagen.File(programma.ar_filename).info.length
                logging.debug("PROGRAM: elaborate time length: %s",programma.ar_length)
	    except:
                logging.error("PROGRAM: error establish time length; use an estimation %s", programma.ar_filename)
            	programma.ar_length=3600

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
        print programma.ar_scheduledatetime
        print programma.ar_length

        #programma.program.get_file_filename()

        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
