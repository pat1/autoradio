#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2007-2009 Paolo Patruno.

from .autoradio_config import *

from .gest_program import *
from .gest_spot import *
from .gest_jingle import *
from .gest_playlist import *
from .gest_palimpsest import *


class schedule:
    """
    Single schedule object
    attributes:
    djobj : dajngo retrive object
    scheduledatetime : datetime of schedule
    media : url of media
    filename : path of media
    length=None : time length in seconds
    type=None   : "spot"/""playlist"/"jingle"/"programma"
    emission_done=None
    shuffle=False
    title=None):
    """
    def __init__ (self,djobj,scheduledatetime,media,filename,length=None,type=None,emission_done=None,\
                      shuffle=False,maxlength=None,title=None):
        """
        init of schedule object:
        """
        self.mydjobj=djobj
        self.scheduledatetime=scheduledatetime
        self.mymedia=media
        self.filename=filename
        #self.mediaweb = self.media[len(settings.MEDIA_URL)+1:]
        self.length=length
        self.type=type
        self.emission_done=emission_done
        self.shuffle=shuffle
        self.maxlength=maxlength
        self.mytitle=title


    def __eq__(self, other):
        if (self.scheduledatetime is None and other.scheduledatetime is None
            or self.scheduledatetime == other.scheduledatetime) :
            return True

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def __lt__(self, other):
        return self.scheduledatetime < other.scheduledatetime

    def __le__(self, other):
        return self.scheduledatetime <= other.scheduledatetime

    def __gt__(self, other):
        return self.scheduledatetime > other.scheduledatetime

    def __ge__(self, other):
        return self.scheduledatetime >= other.scheduledatetime

        
    def future (self,now=None):
        return self.scheduledatetime > now

    def filter (self):

        if self.scheduledatetime is None :
            return False

        return True

    def __repr__ (self):

        return self.type+" "+self.mymedia


#    def __iter__(self,now=None):
#        self.index=0
#        self.now=now
#        if self.now is None : self.now=datetime.now()
#        return self
#        
#    def __next__(self):
#        self.index+=1
#        if (self.index==1):
#            return self.mydjobj
#        if (self.index==2):
#            return self.mytitle
#        if (self.index==3):
#            return self.scheduledatetime
#        if (self.index==4):
#            return self.mymedia
#        if (self.index==5):
#            return str((datetime(2000,1,1)+timedelta(seconds=int(self.length))).time())
#        if (self.index==6):
#            return self.type
#        if (self.index==7):
#            return self.emission_done
#        if (self.index==8):
#            return self.future(self.now)
#        raise StopIteration

    def get_djobj(self):
        return self.mydjobj
    def get_title(self):
        return self.mytitle
    def get_datet(self):
        return self.scheduledatetime
    def get_media(self):
        return self.mymedia
    def get_length_s(self):
        return str((datetime(2000,1,1)+timedelta(seconds=int(self.length))).time())
    def get_tipo(self):
        return self.type        
    def get_datetdone(self):
        return self.emission_done
    def get_isfuture(self):
        return self.future(datetime.now(tz=None))

    djobj=property(get_djobj)
    title=property(get_title)
    datet=property(get_datet)
    media=property(get_media)
    length_s=property(get_length_s)
    tipo=property(get_tipo)
    datetdone=property(get_datetdone)
    isfuture=property(get_isfuture)

    
class schedules(list):
    """
    multiple schedule object
    """
    def __init__(self, *args, **kwargs):
        super(schedules, self).__init__(*args, **kwargs)
        self.districatimes=0
        
        
    def districa(self):
        '''
        english:
        try to extricate from an schedules ensemble
        the more easy operation is to delete jingles inside programs and spots
        italiano: cerca di districarsi tra un insieme di schedule
        la prima operazione da fare e' togliere i jingle che coincidono con programmi e pubblicita'

        return True if need other call to self to manage new modification

        '''
        logging.debug("execute districa")

        needrecompute=False
        recomputedtimes=0
        self.districatimes += 0
        
        #Spots
        #v=0
        for v,schedulej in enumerate(self):

            # add the default adjustedlength  !!! Attention
            schedulej.adjustedlength= schedulej.length

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
                    halfscheduledatetime=scheduledatetime+timedelta(seconds=int(length/2))

                    if (type == "spot" or type == "playlist" or type == "jingle" ): continue

                    # here we have spot versus programs

                    #starting in the firth half of program
                    if ( scheduledatetime < scheduledatetimej and scheduledatetimej < halfscheduledatetime ): 
                        logging.debug( "anticipate this spot overlapped start time in the firth half %s", str(self[v]))

                        ##we have to anticipate a epsilon to be shure to go before 
                        #self[v].scheduledatetime=scheduledatetime-timedelta(seconds=30)

                        #we have to anticipate start program - spot length
                        self[v].scheduledatetime=scheduledatetime-timedelta(seconds=lengthj)

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)


                    #ending in the firth half of program
                    if ( endscheduledatetimej > scheduledatetime and endscheduledatetimej < halfscheduledatetime ): 
                        logging.debug( "anticipate this spot overlapped end time in the firth half %s", str(self[v]))

                        #we have to anticipate start program - spot length
                        self[v].scheduledatetime=scheduledatetime-timedelta(seconds=lengthj)

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)

                    #start in the second half of program
                    if ( scheduledatetimej >= halfscheduledatetime and scheduledatetimej < endscheduledatetime ):
                        logging.debug( "postpone this spot overlapped in the second half %s", str(self[v]))

                        #we have to postpone start program - spot length
                        self[v].scheduledatetime=endscheduledatetime

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)

                    # this case is not so simple
                    # after moving spots we have spots overlapped
                    # this is possible when we have programs without time interval for spots like more enclosure in one episode
                    # here is more simple to simulate one enclosure more long to include spots length
                    # recompute programs length overlapped with spots
                    if ( scheduledatetime < scheduledatetimej and scheduledatetimej < endscheduledatetime ): 
                        logging.debug( "adding time to program; this spot overlapped %s", str(self[v]))
                        schedule.adjustedlength=schedule.length+lengthj
                        needrecompute=True

            #v += 1


        #now we can have programs overlapped bt programs
        for v,schedulej in enumerate(self):

            scheduledatetimej=schedulej.scheduledatetime
            if ( scheduledatetimej == None ): continue

            lengthj=schedulej.adjustedlength
            typej=schedulej.type
            endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
            #print "elaborate          ",typej,scheduledatetimej,endscheduledatetimej

            if (typej == "program"):

                for vv,schedule in enumerate(self):

                    #do not compare with itself
                    if schedule == schedulej and str(schedule) == str(schedulej): continue

                    scheduledatetime=schedule.scheduledatetime
                    if ( scheduledatetime== None ): continue

                    length=schedule.adjustedlength
                    type=schedule.type
                    endscheduledatetime=scheduledatetime+timedelta(seconds=length)
                    halfscheduledatetime=scheduledatetime+timedelta(seconds=int(length/2))

                    if (type == "spot" or type == "playlist" or type == "jingle" ): continue

                    # here we have program versus programs

                    #starting in the firth half of program
                    if ( scheduledatetime <= scheduledatetimej and scheduledatetimej < halfscheduledatetime ): 
                        logging.debug( "postpone this program overlapped start time in the firth half")
                        logging.debug( "postpone %s, over %s", str(self[v]),str(self[vv]))

                        #we have to postpone start program - spot length
                        self[v].scheduledatetime=endscheduledatetime

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
                        needrecompute=True


                    #ending in the firth half of program
                    if ( endscheduledatetimej > scheduledatetime and endscheduledatetimej < halfscheduledatetime ): 
                        logging.debug( "anticipate this program overlapped end time in the firth half")
                        logging.debug( "anticipate %s, over %s", str(self[v]),str(self[vv]))

                        #we have to anticipate start program - spot length
                        self[v].scheduledatetime=scheduledatetime-timedelta(seconds=lengthj)

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
                        needrecompute=True

                    #start in the second half of program
                    if ( scheduledatetimej >= halfscheduledatetime and scheduledatetimej < endscheduledatetime ):
                        logging.debug( "postpone this program overlapped in the second half")
                        logging.debug( "postpone %s, over %s", str(self[v]),str(self[vv]))

                        #we have to postpone
                        self[v].scheduledatetime=endscheduledatetime

                        #recompute 
                        scheduledatetimej=self[v].scheduledatetime
                        endscheduledatetimej=scheduledatetimej+timedelta(seconds=lengthj)
                        needrecompute=True


    #Jingles
    # remove jingles overlapped with programs and spots

        #v=0
        for v,schedulej in enumerate(self):

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
                    # here we have jingle versus programs and spot

                    if (( scheduledatetime < scheduledatetimej and scheduledatetimej < endscheduledatetime )\
                            or \
                        ( scheduledatetime < endscheduledatetimej and endscheduledatetimej < endscheduledatetime )):
                        logging.debug( "remove this jingle overlapped %s", str(self[v]))
                        self[v].scheduledatetime=None

            #v += 1
        return needrecompute


    def purge(self):

        
        reverse_enumerate = lambda l: zip(range(len(l)-1, -1, -1), reversed(l))

        for ind,schedula in reverse_enumerate(self):
            if not schedula.filter():
                logging.debug( "purge %s", str(schedula))
                del self[ind]

    def get_all(self,now=None,genfile=True):

        # time constants

        #this is the first and last time that I set the current time
        if now is None : now=datetime.now(tz=None)

        if (multi_channel):
            spots=gest_spot_channel(now,minelab,playlistdir)
        else:
            spots=gest_spot(now,minelab,playlistdir)
            
        for fascia in spots.get_fasce(genfile):

            media = spots.ar_url
            filename = spots.ar_filename
            scheduledatetime=spots.ar_scheduledatetime
            length=spots.ar_length
            emission_done=spots.ar_emission_done
            number=spots.ar_spots_in_fascia
            #print scheduledatetime,media,length,number,emission_done
            if (number != 0 ):
                self.append(schedule(fascia,scheduledatetime,media,filename,length,"spot",emission_done,title=str(fascia)))


        programs=gest_program(now,minelab)

        for programma in programs.get_program():

            media = programma.ar_url
            filename = programma.ar_filename
            scheduledatetime=programma.ar_scheduledatetime
            length=programma.ar_length
            emission_done=programma.ar_emission_done
            title=programma.ar_title

            #print scheduledatetime,media,length,emission_done
            self.append(schedule(programma,scheduledatetime,media,filename,length,"program",\
                                     emission_done,title=title))


        playlists=gest_playlist(now,minelab)

        for playlist in playlists.get_playlist():

            media = playlist.ar_url
            filename = playlist.ar_filename
            scheduledatetime=playlist.ar_scheduledatetime
            length=playlist.ar_length
            maxlength=playlist.length
            emission_done=playlist.ar_emission_done
            shuffle=playlist.ar_shuffle
            #print scheduledatetime,media,length,emission_done
            self.append(schedule(playlist,scheduledatetime,media,filename,length,"playlist",\
                                     emission_done,shuffle,maxlength,title=str(playlist)))


        jingles=gest_jingle(now,minelab)

        for jingle in jingles.get_jingle():

            media = jingle.ar_url
            filename = jingle.ar_filename
            scheduledatetime=jingle.ar_scheduledatetime
            length=jingle.ar_length
            emission_done=jingle.ar_emission_done

            #print scheduledatetime,media,length,emission_done
            self.append(schedule(jingle,scheduledatetime,media,filename,length,"jingle",\
                                     emission_done,title=str(jingle)))


        #return self


    def get_all_refine(self,now=None,genfile=True):


        self.get_all(now,genfile)
        while self.districa():
            if (self.districatimes >= 20 ):
                logging.error("districa do not converge: too many programs in few time")
                break
        self.purge()
        self.sort()
        
        #return self



class palimpsest(object):
    
    
    def __init__ (self,title=None,datetime_start=None,datetime_end=None,
                  code=None,type=None,subtype=None,production=None,note=None):
        """
        init of palimpsest object
        """
        self.title=title
        self.datetime_start=datetime_start
        self.datetime_end=datetime_end
        self.code=code
        self.type=type
        self.subtype=subtype
        self.production=production
        self.note=note

    def __lt__(self,b):

        #check start datetime

        if self.datetime_start is None and b.datetime_start is None :
            return False
    
        if self.datetime_start is None :
            return True
    
        if b.datetime_start is None :
            return False
    

        if  self.datetime_start == b.datetime_start :

            #check end datetime
            if self.datetime_end is None and b.datetime_end is None :
                return False
    
            if self.datetime_end is None :
                return Frue
    
            if b.datetime_end is None :
                return False
            
            if  self.datetime_end == b.datetime_end :
                return False
            elif   self.datetime_end < b.datetime_end :
                return True
            elif   self.datetime_end > b.datetime_end :
                return False


        elif   self.datetime_start < b.datetime_start :
            return True
        elif   self.datetime_start > b.datetime_start :
            return False


        
        
    def __cmp__ (self, b):

        
        #check start datetime

        if self.datetime_start is None and b.datetime_start is None :
            return 0
    
        if self.datetime_start is None :
            return -1
    
        if b.datetime_start is None :
            return 1
    

        if  self.datetime_start == b.datetime_start :

            #check end datetime
            if self.datetime_end is None and b.datetime_end is None :
                return 0
    
            if self.datetime_end is None :
                return -1
    
            if b.datetime_end is None :
                return 1
            
            if  self.datetime_end == b.datetime_end :
                return 0
            elif   self.datetime_end < b.datetime_end :
                return -1
            elif   self.datetime_end > b.datetime_end :
                return 1


        elif   self.datetime_start < b.datetime_start :
            return -1
        elif   self.datetime_start > b.datetime_start :
            return 1



    def __str__ (self):

        return self.title+" "+str(self.datetime_start)+" "+\
            str(self.datetime_end)+" "+str(self.type)+" "+\
            str(self.subtype)+" "+str(self.production)+" "+str(self.note)

    
    def __iter__(self):
        '''
        return a list
        '''
        self.index=0
        return self

    def __next__(self):
        self.index+=1
        if (self.index==1):
            return self.title
        if (self.index==2):
            return self.datetime_start
        if (self.index==3):
            return self.datetime_end
        if (self.index==4):
            return self.code
        if (self.index==5):
            return self.type
        if (self.index==6):
            return self.subtype
        if (self.index==7):
            return self.production
        if (self.index==8):
            return self.note
        raise StopIteration

class dates(object):

    def __init__(self,datetime_start, datetime_end,step):

        self.step=step
        self.datetime_start=datetime_start
        self.datetime_end=datetime_end


    def __iter__(self):

        return self


    def __next__(self):

        self.datetime_start=self.datetime_start+self.step
        if self.datetime_start <= self.datetime_end:
            return self.datetime_start
        else:
            raise StopIteration
            #return


class palimpsests(list):


    def get_palimpsest(self,datetime_start,datetime_end):

        step=timedelta(minutes=minelab*2) 


        for datetimeelab in dates(datetime_start, datetime_end, step):

            pro=gest_palimpsest(datetimeelab,minelab)

            for program in pro.get_program():

                length=program.show.length
                if length is None:
                    logging.warning("get_palimpsest: %s legth is None; setting default to 3600 sec",str(program))
                    length = 3600
                pdatetime_start=program.ar_scheduledatetime
                title=str(program)
                pdatetime_end=program.ar_scheduledatetime+timedelta(seconds=length)
                code=program.show.type.code
                type=program.show.type.type
                subtype=program.show.type.subtype
                production=program.show.production
                note=program.show.description

                if pdatetime_start >= datetime_start and pdatetime_end < datetime_end :

                    self.append(palimpsest(title,pdatetime_start,pdatetime_end,
                                           code,type,subtype,production,note))


        self.sort()

        #print ("prima:")
        #for program in self:
        #    print (program)

        # timing adjust:
        #    1) overlay
        #    2) insert music no stop for interval >15 minutes


        musicanostop=palimpsests([])

        for i in range(len(self)-1):
            if self[i].datetime_end > self[i+1].datetime_start:

                self[i].datetime_end=self[i+1].datetime_start

            elif self[i].datetime_end < self[i+1].datetime_start-timedelta(minutes=15):

                musicanostop.append(palimpsest("Musica no stop",self[i].datetime_end,
                                       self[i+1].datetime_start,code="13f",
                                       type="13",subtype="13f",production="autoproduzione",note=None))

        for element in musicanostop:
            self.append(element)

        self.sort()

        for i in range(len(self)-1):
        #    3) chain little interval

            if self[i].datetime_end != self[i+1].datetime_start:

                dtmean=self[i].datetime_end+((self[i+1].datetime_start-self[i].datetime_end)/2)

                self[i].datetime_end=dtmean
                self[i+1].datetime_start=dtmean

        # add head and tail:
        #    chain little interval
        if len(self) > 0 :

            if self[0].datetime_start != datetime_start :

                self.insert(0,palimpsest("Musica no stop",datetime_start,
                                       self[0].datetime_start,code="13f",
                                       type="13",subtype="13f",production="autoproduzione",note=None))

            if self[len(self)-1].datetime_end != datetime_end :

                self.append(palimpsest("Musica no stop",self[len(self)-1].datetime_end,
                                       datetime_end,code="13f",
                                   type="13",subtype="13f",production="autoproduzione",note=None))



        #print "dopo:"
        #for program in self:
        #    print program


        # Spots

        for datetimeelab in dates(datetime_start, datetime_end, step):

            #print datetimeelab,minelab
            spots=gest_spot(datetimeelab,minelab,playlistdir)

            for fascia in spots.get_fasce(genfile=False):

                length=spots.ar_length
                #pdatetime_start=spots.ar_emission_done
                pdatetime_start=spots.ar_scheduledatetime
                number=spots.ar_spots_in_fascia
                #title=str(fascia)
                title="Pubblicità"
                pdatetime_end=pdatetime_start+timedelta(seconds=length)
                type="5"
                subtype="5a"
                production=""
                note="%d Spot" % number

                #if (number <> 0 and pdatetime_start.date() == dateelab):
                if number != 0 and  pdatetime_start >= datetime_start and pdatetime_end < datetime_end :
                    self.append(palimpsest(title,pdatetime_start,pdatetime_end,
                                           type,subtype,production,note))


        self.sort()

        return self


def main():

    logging.basicConfig(level=logging.INFO,)

#    pali=palimpsests([])

#    print "------- palimpsest --------"
#    for prog in pali.get_palimpsest(datetime.now()-timedelta(days=1),datetime.now()):
#        print "------- program --------"
#
#        print prog
#
#        #for elemento in prog:
#        #    print elemento


    scheds=schedules([])

    # get the schedule of my insterest
    # I do a list
    print("------- schedules --------")
    for sched in scheds.get_all_refine():
    

        print("------- schedule --------")

        for elemento in sched:
            print(elemento)

        print(sched.type)
        print(sched.media)
        print(sched.scheduledatetime)
        print(sched.shuffle)
        print(sched.length)



        
if __name__ == '__main__':
    main()  # (this code was run as script)
    
