#!/usr/bin/env python
# GPL. (C) 2007-2012 Paolo Patruno.

import logging
import dbus
import autompris
from datetime import *
from threading import *
import os
import autoradio_config


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings


class PlayerError(Exception):

   def __str__(self):
      return repr(self.args[0])


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

    def __init__ (self,player,session,schedule):
        "init schedule"
        
        self.deltasec=secondi( schedule.scheduledatetime - datetime.now())
        # round to nearest future
        if self.deltasec < 5 : self.deltasec = 5
        self.player=player
        self.session=session
        self.function=ManagePlayer
        self.schedule=schedule
        self.timer = Timer(self.deltasec, self.function,[self.player,self.session,self.schedule])

    def start (self):
        "start of programmed schedule"
        
        self.timer.start()


def ManagePlayer (player,session,schedule):
   "Manage player to do operation on media"
    
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
         raise PlayerError("Managempris: type not supported: %s"% schedule.type)

      if operation == "loadPlaylist":
         media=shuffle_playlist(schedule.filename,schedule.shuffle,relative_path=False,length=schedule.maxlength)
      else:
         media=schedule.filename

      aud=autompris.mediaplayer(player=player,session=session)

      # Regione critica
      lock.acquire()
      try:
         if not aud.playlist_clear_up(atlast=10):
            raise PlayerError("Managempris: ERROR in playlist_clear_up")

         #print settings.MEDIA_ROOT
         pos=aud.get_playlist_posauto(autopath=settings.MEDIA_ROOT,securesec=10)
         curpos=aud.get_playlist_pos()

         # inserisco il file nella playlist
         if pos is None:
            raise PlayerError("Managempris: ERROR in xmms.control.get_playlist_posauto")

         logging.info( "ManageXmms: insert media: %s at position %d",media,pos)
         aud.playlist_add_atpos("file://"+media,pos)
                
         # recheck for consistency
         newpos=aud.get_playlist_pos()
         if curpos != newpos:
            raise PlayerError("Managempris: strange ERROR: consinstency problem; pos: %d , newpos: %d"% (curpos,newpos))

         if not aud.playlist_clear_down(atlast=500):
            raise PlayerError("Managempris: ERROR in playlist_clear_down")

      finally:
         #signal.alarm(0)
         lock.release()

         # here we have a problem ... sometime the player is not ready when the file is deleted !
         # so we comment it out
#         if schedule.shuffle:
#            os.remove(media)

      logging.info( "Managempris: write   in django: %s",schedule.djobj)
      ar_emitted(schedule.djobj)
      logging.info( "Managempris: written in django: %s",schedule.djobj)

      aud.play_ifnot()

   except PlayerError, e:
      logging.error(e)
      
   return



def secondi(delta):
    secondi=float(delta.seconds)
    secondi=secondi+(delta.microseconds/100000.)

    if delta.days < 0 :
        secondi = secondi + (3600*24*delta.days)
    return secondi


class dummy_programma:

    def __init__(self):
        pass
    
    def save(self):
        #print "masquerade as we save it"
        pass
    

def player_watchdog(player,session):

   logging.debug( "player_watchdog: test if player is running" )

   try:
      aud=autompris.mediaplayer(player=player,session=session)

   except:
      logging.error("player_watchdog: player do not communicate on d-bus")
      import subprocess
      try:
         logging.info("player_watchdog: try launching player")
         subprocess.Popen(player , shell=True)
      except:
         logging.error("player_watchdog: error launching "+player)
         try:
            logging.info("player_watchdog: try launching "+player+"2")
            subprocess.Popen(player+"2" , shell=True)
         except:
            logging.error("player_watchdog: error launching "+player+"2")

      import time
      time.sleep(5)
      logging.info("player_watchdog: player executed")

      try:
         aud=autompris.mediaplayer(player=player,session=session)

      except:
         logging.error("player_watchdog serious problem: player do not comunicate on d-bus")
         raise

   aud.play_ifnot()
   logging.debug("player_watchdog: start playing if not")

   return True


def save_status(session):
   """
   Do nothing
   """

   logging.debug ( "DUMMY xmms.saveCurrentPlaylist")
   return True


def main():

    import autoradio_core

    player="audacious"
    session=0
    logging.getLogger('').setLevel(logging.DEBUG)

    programma=dummy_programma()
    player_watchdog(player=player,session=session)
    shuffle=False
    maxlength=None

    type="program"
    media = "/home/pat1/svn/autoradio/trunk/media/pippo.mp3"
    #media = "/home/pat1/Musica/STOP AL PANICO/ISOLA POSSE STOP AL PANICO.mp3"
    #media = "/home/autoradio/django/media/playlist/tappeto_musicale.m3u"
    #media = raw_input("dammi il media? ")

    scheduledatetime=datetime.now()+timedelta(seconds=5)
    sched=autoradio_core.schedule(programma,scheduledatetime,media,filename=media,type=type,shuffle=shuffle,maxlength=maxlength)

    threadschedule=ScheduleProgram(player,session,sched)
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
    
