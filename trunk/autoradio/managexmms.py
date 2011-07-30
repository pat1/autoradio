#!/usr/bin/env python
# GPL. (C) 2007 Paolo Patruno.

import logging
import xmms,autoxmms
from datetime import *
from threading import *
from django.conf import settings
import os
import autoradio_config
#import signal

class XmmsError(Exception):
   pass


def shuffle_playlist(infile,shuffle=False,relative_path=False,length=None):

    import mkplaylist
    import os,random,tempfile,codecs

    media_files=list(mkplaylist.read_playlist(infile, not relative_path))
    
    if shuffle:
        random.shuffle(media_files)
#    else:
#        media_files.sort()

    fd,outfile=tempfile.mkstemp(".m3u")
    #ffoutfile = os.fdopen(fd,"w")
    foutfile = codecs.open(outfile, "w", encoding="UTF-8")

    
    mkplaylist.write_extm3u(media_files, foutfile,length)
    foutfile.close()
    os.close(fd)

    return outfile


lock = Lock()

def ar_emitted(self):
    '''
    Save in django datatime when emission is done
    '''

    self.emission_done=datetime.now()
    self.save()


class ScheduleProgram:
    '''
    activate a schedule setting it for a time in the future
    '''

    def __init__ (self,session,schedule):
        #session,function,operation,
        #media,scheduledatetime,programma,shuffle=None,length=None):
        "init schedule"
        
        #self.function=function
        #self.operation=operation
 
        #self.schedule=schedule
        #self.media=media
        #self.scheduledatetime=scheduledatetime
        #self.programma=programma
        #self.shuffle=shuffle
        #self.length=length

        #scheduledatetime
        #print "difference ",datetime.now(),self.scheduledatetime

        #self.deltasec=max(secondi( schedule.scheduledatetime - datetime.now()),1)
        self.deltasec=secondi( schedule.scheduledatetime - datetime.now())

        self.session=session
        self.function=ManageXmms
        self.schedule=schedule
        self.timer = Timer(self.deltasec, self.function,[self.session,self.schedule])
        #              [self.session,self.operation,self.chedule
        #               self.media,self.programma,self.shuffle,self.length])

    def start (self):
        "start of programmed schedule"
        
        self.timer.start()


def ManageXmms (session,schedule):
   "Manage xmms to do operation on media"
    
   try:

      if ( schedule.type == "spot" ): 
         operation="queueMedia"
      elif ( schedule.type == "program" ): 
         operation="queueMedia"
      elif ( schedule.type == "jingle" ):
         operation="queueMedia"
      elif ( schedule.type == "playlist" ):
         operation="loadPlaylist"
      else:
         raise XmmsError("ManageXmms: type not supported: %s"% schedule.type)

      media=schedule.media
      if operation == "loadPlaylist":
         media=shuffle_playlist(schedule.media,schedule.shuffle,relative_path=False,length=schedule.maxlength)

      # Regione critica
      lock.acquire()
      try:
         if not autoxmms.playlist_clear_up(atlast=10,session=session):
            raise XmmsError("ManageXmms: ERROR in xmms.control.playlist_clear_up")

         pos=autoxmms.get_playlist_posauto(autopath=settings.MEDIA_ROOT,securesec=10,session=session)
         curpos=xmms.control.get_playlist_pos(session)

         # inserisco il file nella playlist
         if pos is None:
            raise XmmsError("ManageXmms: ERROR in xmms.control.get_playlist_posauto")

         logging.info( "ManageXmms: insert media: %s at position %d",media,pos)
         xmms.control.playlist_ins_url_string(media,pos,session)
         #error test impossible
                
         # recheck for consistency
         newpos=xmms.control.get_playlist_pos(session)
         if curpos != newpos:
            raise XmmsError("ManageXmms: strange ERROR: consinstency problem; pos: %d , newpos: %d"% (curpos,newpos))

         if not autoxmms.playlist_clear_down(atlast=500,session=session):
            raise XmmsError("ManageXmms: ERROR in xmms.control.playlist_clear_down")

      finally:
         #signal.alarm(0)
         lock.release()
         if schedule.shuffle:
            os.remove(media)

      logging.info( "ManageXmms: write in django: %s",schedule.djobj)
      ar_emitted(schedule.djobj)
      logging.info( "ManageXmms: write in django: %s",schedule.djobj)

   except XmmsError, e:
      logging.error(e.message)
      
   #except:
   #   logging.error( "ManageXmms: ERRORE type: %s, media: %s",schedule.type,schedule.media)
      
   return autoxmms.play_ifnot(session=session)



def secondi(delta):
    secondi=float(delta.seconds)
    secondi=secondi+(delta.microseconds/100000.)
    # correggo i viaggi che si fa seconds
    if delta.days < 0 :
        secondi = secondi + (3600*24*delta.days)
    return secondi



class dummy_programma:

    def __init__(self):
        pass
    
    def save(self):
        #print "masquerade as we save it"
        pass
    

def xmms_watchdog(session):

    logging.debug( "xmms_watchdog: test if xmms.is running" )

    try:
        ok  = xmms.control.is_running(session)
        logging.debug("xmms_watchdog: xmms.is_running return %s", str(ok))

    except:
        ok=False
        logging.error("xmms_watchdog: error on xmms.is_running")


    if (not ok ):
        logging.error("xmms_watchdog: xmms is not running")

        try:
            xmms.control.enqueue_and_play_launch_if_session_not_started("file",session=session,
                                              stdout_to_dev_null=True, stderr_to_dev_null=True)
            ok=True
            logging.info("xmms_watchdog: pyxmms < 2.07 xmms.control.enqueue_and_play_launch_if_session_not_started")

        except:

           try:
              xmms.control.enqueue_and_play_launch_if_session_not_started("file",session=session)

              ok=True
              logging.info("xmms_watchdog: pyxmms >= 2.07 xmms.control.enqueue_and_play_launch_if_session_not_started")

           except:
              ok=False
              logging.error("xmms_watchdog: error xmms.control.enqueue_and_play_launch_if_session_not_started")

    return ok


def save_status(session):

# file dovra essere prima salvato usando:
#        xmms.get_playlist_length(session) (restituisce il numero di brani nella playlist
#        get_playlist_file(index, session=0) -> absolute filename (string)
#        get_playlist_pos(session=0) -> position (integer)

    logging.debug ( "DUMMY xmms.saveCurrentPlaylist")
    return True


def main():

    import autoradio_core

    programma=dummy_programma()

    session=0
    shuffle=True
    maxlength=None

    type="playlist"
    media = "/home/autoradio/django/media/playlist/playlistmingogozza.m3u"
    #media = "/home/autoradio/django/media/playlist/tappeto_musicale.m3u"
    #media = raw_input("dammi il media? ")

    scheduledatetime=datetime.now()+timedelta(seconds=5)
    sched=autoradio_core.schedule(programma,scheduledatetime,media,type=type,shuffle=shuffle,maxlength=maxlength)

    threadschedule=ScheduleProgram(session,sched)
    threadschedule.start()

#    scheduledatetime=datetime.now()+timedelta(seconds=8)
#    media = "/home/autoradio/django/media/programs/borsellino_giordano.mp3"
#    schedule=ScheduleProgram(session,function,operation,media,scheduledatetime,programma,shuffle)
#    schedule.start()

#    scheduledatetime=datetime.now()+timedelta(seconds=10)
#    media = "/home/autoradio/django/media/programs/mister_follow_follow.mp3"
#    schedule=ScheduleProgram(session,function,operation,media,scheduledatetime,programma,shuffle)
#    schedule.start()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
