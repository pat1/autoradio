#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

from autoradio_config import *

from gest_program import *
from gest_spot import *
from gest_jingle import *
from gest_playlist import *


class schedule:
    """
    Single schedule object
    attributes:
    djobj : dajngo retrive object
    scheduledatetime : datetime of schedule
    media
    length=None : time length in seconds
    type=None   : "spot"/""playlist"/"jingle"/"programma"
    emission_done=None
    shuffle=False):
    """
    def __init__ (self,djobj,scheduledatetime,media,length=None,type=None,emission_done=None,shuffle=False):
        """
        init of schedule object:
        """
        self.djobj=djobj
        self.scheduledatetime=scheduledatetime
        self.media=media
        self.mediaweb = self.media[len(BASE_PATH)+1:]
        self.length=length
        self.type=type
        self.emission_done=emission_done
        self.shuffle=shuffle


    def __cmp__ (self, b):

        if self.scheduledatetime is None and b.scheduledatetime is None :
            return 0
    
        if self.scheduledatetime is None :
            return -1
    
        if b.scheduledatetime is None :
            return 1
    

        if  self.scheduledatetime == b.scheduledatetime :
            return 0
        elif   self.scheduledatetime < b.scheduledatetime :
            return -1
        elif    self.scheduledatetime > b.scheduledatetime :
            return 1

    def future (self,now=None):
        self.future=self.scheduledatetime > now
        return self.future

    def filter (self):

        if self.scheduledatetime is None :
            return False

        return True

    def __str__ (self):

        return self.type+" "+self.media


    def __iter__(self,now=None):
        '''
        return a list  nome,datet,media,len,tipo,datetdone,future 
        '''

        if now is None : now=datetime.now()

        #return iter((self.djobj,self.scheduledatetime,self.media,self.length,self.type,self.emission_done,self.shuffle,self.future(now)))

        yield self.djobj
        yield self.scheduledatetime
        yield self.mediaweb
        yield str((datetime(2000,1,1)+timedelta(seconds=int(self.length))).time())
        yield self.type
        yield self.emission_done
        yield self.future(now)


class schedules(list):
    """
    multiple schedule object
    """

    def districa(self):
        '''
        english:
        try to extricate fron an schedules ensemble
        the more easy operation is to delete jingles inside programs and spots
        italian: cerca di sdistricarsi tra un insieme di schedule
        la prima operazione da fare e' togliere i jingle che coincidono con programmi e pubblicita'
        '''
        logging.debug("execute districa")

    #Jingles
        v=0
        for schedulej in self:

            scheduledatetimej=schedulej.scheduledatetime
            if ( scheduledatetimej == None ): continue

            lengthj=schedulej.length
            typej=schedulej.type
            endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
            #print "elaboro          ",typej,scheduledatetimej,endscheduledatetimej

            if (typej == "jingle"):
                for schedule in self:

                    scheduledatetime=schedule.scheduledatetime
                    if ( scheduledatetime== None ): continue

                    length=schedule.length
                    type=schedule.type
                    endscheduledatetime=scheduledatetime+timedelta(seconds=length)

                    if (type == "jingle" or type == "playlist"): continue
                    # here we have jingle versus programs ans spot

                    if (( scheduledatetime < scheduledatetimej and scheduledatetimej < endscheduledatetime )\
                            or \
                        ( scheduledatetime < endscheduledatetimej and endscheduledatetimej < endscheduledatetime )):
                        logging.debug( "remove this jingle overlapped %s", str(self[v]))
                        self[v].scheduledatetime=None

            v += 1


    #Spots
        v=0
        for schedulej in self:

            scheduledatetimej=schedulej.scheduledatetime
            if ( scheduledatetimej == None ): continue

            lengthj=schedulej.length
            typej=schedulej.type
            endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
            #print "elaborate          ",typej,scheduledatetimej,endscheduledatetimej

            if (typej == "spot"):

                for schedule in self:

                    scheduledatetime=schedule.scheduledatetime
                    if ( scheduledatetime== None ): continue

                    length=schedule.length
                    type=schedule.type
                    endscheduledatetime=scheduledatetime+timedelta(seconds=length)
                    halfscheduledatetime=scheduledatetime+timedelta(seconds=length/2)

                    if (type == "spot" or type == "playlist" or type == "jingle" ): continue

                    # here we have spot versus programs

                    if ( scheduledatetime < scheduledatetimej and scheduledatetimej < halfscheduledatetime ): 
                        logging.debug( "anticipate this spot overlapped %s", str(self[v]))

                        #we have to anticipate a epsilon to be shure to go before 
                        self[v].scheduledatetime=scheduledatetime-timedelta(seconds=30)

            v += 1


    def purge(self):

        from itertools import izip
        reverse_enumerate = lambda l: izip(xrange(len(l)-1, -1, -1), reversed(l))

        for ind,schedula in reverse_enumerate(self):
            if not schedula.filter():
                logging.debug( "purge %s", str(schedula))
                del self[ind]

    def get_all(self,now=None,genfile=True):

        # time constants

        #this is the first and last time that I set the current time
        if now is None : now=datetime.now()

        spots=gest_spot(now,minelab,playlistdir)

        for fascia in spots.get_fasce(genfile):

            # remove prefix
            media = spots.ar_filename
            scheduledatetime=spots.ar_scheduledatetime
            length=spots.ar_length
            emission_done=spots.ar_emission_done
            number=spots.ar_spots_in_fascia
            #print scheduledatetime,media,length,number,emission_done
            if (number <> 0 ):
                self.append(schedule(fascia,scheduledatetime,media,length,"spot",emission_done))

        programs=gest_program(now,minelab)

        for programma in programs.get_program():

            # remove prefix
            media = programma.ar_filename
            scheduledatetime=programma.ar_scheduledatetime
            length=programma.ar_length
            emission_done=programma.ar_emission_done

            #print scheduledatetime,media,length,emission_done
            self.append(schedule(programma,scheduledatetime,media,length,"program",emission_done))

        playlists=gest_playlist(now,minelab)

        for playlist in playlists.get_playlist():

            media = playlist.ar_filename
            scheduledatetime=playlist.ar_scheduledatetime
            length=playlist.ar_length
            emission_done=playlist.ar_emission_done
            shuffle=playlist.ar_shuffle
            #print scheduledatetime,media,length,emission_done
            self.append(schedule(playlist,scheduledatetime,media,length,"playlist",emission_done,shuffle))


        jingles=gest_jingle(now,minelab)

        for jingle in jingles.get_jingle():

            # remove prefix
            media = jingle.ar_filename
            scheduledatetime=jingle.ar_scheduledatetime

            length=jingle.ar_length
            emission_done=jingle.ar_emission_done

            #print scheduledatetime,media,length,emission_done
            self.append(schedule(jingle,scheduledatetime,media,length,"jingle",emission_done))


        return self


    def get_all_refine(self,now=None,genfile=True):


        self.get_all(now,genfile)
        self.districa()
        self.purge()
        self.sort()

        return self

def main():

    logging.basicConfig(level=logging.DEBUG,)

    scheds=schedules([])

    # get the schedule of my insterest
    # I do a list
    print "------- schedules --------"
    for sched in scheds.get_all_refine():
        
        #pass

        print "------- schedule --------"

        for elemento in sched:
            print elemento

        #print sched.type
        #print sched.media
        #print sched.scheduledatetime
        #print sched.shuffle
        #print sched.length



        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
