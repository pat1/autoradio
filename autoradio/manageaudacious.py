#!/usr/bin/env python
# GPL. (C) 2007 Paolo Patruno.

import logging
import dbus
import autoaudacious
from datetime import *
from threading import *
from django.conf import settings
import os
import autoradio_config

class AudaciousError(Exception):
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
        "init schedule"
        
        self.deltasec=secondi( schedule.scheduledatetime - datetime.now())
        self.session=session
        self.function=ManageAudacious
        self.schedule=schedule
        self.timer = Timer(self.deltasec, self.function,[self.session,self.schedule])

    def start (self):
        "start of programmed schedule"
        
        self.timer.start()


def ManageAudacious (session,schedule):
   "Manage audacious to do operation on media"
    
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
         raise AudaciousError("ManageAudacious: type not supported: %s"% schedule.type)

      media=schedule.media
      if operation == "loadPlaylist":
         media=shuffle_playlist(schedule.media,schedule.shuffle,relative_path=False,length=schedule.maxlength)

      aud=autoaudacious.audacious()

      # Regione critica
      lock.acquire()
      try:
         if not aud.playlist_clear_up(atlast=10):
            raise AudaciousError("ManageAudacious: ERROR in playlist_clear_up")

         #print settings.MEDIA_ROOT
         #pos=aud.get_playlist_posauto(autopath=settings.MEDIA_ROOT,securesec=10)

         pos=aud.get_playlist_posauto(autopath="/cacca",securesec=10)

         curpos=aud.get_playlist_pos()

         # inserisco il file nella playlist
         if pos is None:
            raise AudaciousError("ManageXmms: ERROR in xmms.control.get_playlist_posauto")

         logging.info( "ManageXmms: insert media: %s at position %d",media,pos)
         aud.org.PlaylistInsUrlString("file:/"+media,pos)
                
         # recheck for consistency
         newpos=aud.get_playlist_pos()
         if curpos != newpos:
            raise AudaciousError("Manageaudacious: strange ERROR: consinstency problem; pos: %d , newpos: %d"% (curpos,newpos))

         if not aud.playlist_clear_down(atlast=500):
            raise AudaciousError("ManageAudacious: ERROR in playlist_clear_down")

      finally:
         #signal.alarm(0)
         lock.release()
         if schedule.shuffle:
            os.remove(media)

      logging.info( "ManageAudacious: write in django: %s",schedule.djobj)
      ar_emitted(schedule.djobj)
      logging.info( "ManageAudacious: write in django: %s",schedule.djobj)

   except AudaciousError, e:
      logging.error(e.message)
      
      
   return  aud.play_ifnot()



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
    

def audacious_watchdog(session):


   from distutils.version import LooseVersion
   reqversion=LooseVersion("1.5")
   version=LooseVersion("0.0")

   logging.debug( "audacious_watchdog: test if audacious is running" )

   try:
      aud=autoaudacious.audacious()

   except:
      logging.error("audacious_watchdog: audacious is not running or error on is_running")
      import subprocess
      subprocess.Popen("audacious" , shell=True)
      import time
      time.sleep(5)
      logging.info("audacious_watchdog: launch_audacious")
      aud=autoaudacious.audacious()

   try:
      # aud.root.Identity()
      version=LooseVersion(aud.org.Version())
      logging.info("audacious_watchdog: audacious version: %s" % str(version))

   except:
      logging.error("audacious_watchdog: eror gettin audacious version")
      return True
   
   if ( version < reqversion ):
      logging.error("audacious_watchdog: audacious %s version is wrong (>=1.5) " % version )
      raise Exception

   aud.play_ifnot()
   logging.debug("audacious_watchdog: audacious start playing if not")

   return True


def save_status(session):
   """
   Do nothing
   """

   logging.debug ( "DUMMY xmms.saveCurrentPlaylist")
   return True


def main():

    import autoradio_core

    programma=dummy_programma()
    audacious_watchdog(0)
    session=0
    shuffle=False
    maxlength=None

    type="program"
    media = "/home/pat1/tmp/pippo.mp3"
    #media = "/home/pat1/Musica/STOP AL PANICO/ISOLA POSSE STOP AL PANICO.mp3"
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
    
