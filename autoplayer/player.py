#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

import sys, time, thread
import gobject
import pygst
pygst.require("0.10")
import gst
import playlist
import dbus
import dbus.service
import dbus.mainloop.glib
import logging

PLAYER_IFACE="org.mpris.MediaPlayer2.Player"
TRACKLIST_IFACE="org.mpris.MediaPlayer2.TrackList"
IFACE="org.mpris.MediaPlayer2"
STATUS_PLAYLIST="autoplayer.xspf"

#def _get_uri(self):
#        uri = self.filename
#        if not uri:
#            return
#        if uri.split(':')[0] not in (
#                'http', 'https', 'file', 'udp', 'rtp', 'rtsp'):
#            uri = 'file:' + pathname2url(path.realpath(uri))
#        return uri

class NotSupportedException(dbus.DBusException):
  _dbus_error_name = 'org.mpris.MediaPlayer2.Player.NotSupported'

class AutoPlayer(dbus.service.Object, dbus.service.PropertiesInterface):

    def attach_player(self,player):
        self.player=player

    @dbus.service.method(IFACE)
    def Raise(self):
        pass

    @dbus.service.method(IFACE)
    def Quit(self):
        logging.info("save playlist: %s" % STATUS_PLAYLIST )
        self.player.save_playlist(STATUS_PLAYLIST)
        loop.quit()

    @dbus.service.property(IFACE, signature="b")
    def CanQuit(self):
        return True

    @dbus.service.property(IFACE, signature="b")
    def CanSetFullscreen(self):
        return False

    @dbus.service.property(IFACE, signature="b")
    def CanRaise(self):
        return False

    @dbus.service.property(IFACE, signature="b")
    def HasTrackList(self):
        return True

    @dbus.service.property(IFACE, signature="b")
    def Identity(self):
        return "Autoradio Player"

    # TODO:
    #DesktopEntry 	         s 	Read only 		
    #SupportedUriSchemes 	as 	Read only 		
    #SupportedMimeTypes 	as 	Read only 		

    @dbus.service.property(PLAYER_IFACE, signature="s")
    def PlaybackStatus(self):
        return self.player.playmode

    @dbus.service.property(PLAYER_IFACE, signature="s")
    def LoopStatus(self):
        #raise
        return "None"

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def Rate(self):
        return 1.0

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def Shuffle(self):
        #raise
        return False

    @dbus.service.property(PLAYER_IFACE, signature="a{sv}")
    def Metadata(self):
        #raise
        return {"mpris:trackid":self.player.playlist.current,}

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def Volume(self):
        #raise
        return 1.0

    @dbus.service.property(PLAYER_IFACE, signature="x")
    def Position(self):
        return self.player.position()

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def MinimumRate(self):
        return 1.0

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def MaximumRate(self):
        return 1.0

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanGoNext(self):
        return True

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanGoPrevious(self):
        return True

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanSeek(self):
        return True

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanControl(self):
        return True

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanPlay(self):
        if self.player.playlist.current is None :
            return False
        else:
            return True

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def CanPause(self):
        return True

    @dbus.service.method(PLAYER_IFACE)
    def Next(self):
      self.player.next()

    @dbus.service.method(PLAYER_IFACE)
    def Previous(self):
      self.player.previous()

    @dbus.service.method(PLAYER_IFACE)
    def Pause(self):
      self.player.pause()

    @dbus.service.method(PLAYER_IFACE)
    def PlayPause(self):
      self.player.playpause()

    @dbus.service.method(PLAYER_IFACE)
    def Stop(self):
      self.player.stop()

    @dbus.service.method(PLAYER_IFACE)
    def Play(self):
      self.player.loaduri()
      self.player.play()

    @dbus.service.method(PLAYER_IFACE,in_signature='x')
    def Seek(self,offset):
      self.player.seek(offset)

    @dbus.service.method(PLAYER_IFACE,in_signature='sx')
    def SetPosition(self,trackid,position):
      self.player.setposition(trackid,position)

    @dbus.service.method(PLAYER_IFACE,in_signature='s')
    def OpenUri(self,uri):
      self.player.openuri(uri)

#tracklist

    @dbus.service.method(TRACKLIST_IFACE,in_signature='ssb', out_signature='')
    def AddTrack(self,uri, aftertrack, setascurrent):
        self.addtrack(uri, aftertrack, setascurrent)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='s', out_signature='')
    def RemoveTrack(self, trackid):
        self.removetrack(trackid)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='s', out_signature='')
    def GoTo(self, trackid):
        self.goto(trackid)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='as', out_signature='aa{sv}')
    def GetTracksMetadata(self,trackids):
        metadata=[]
        for id in trackids:
            meta={}
            for key,attr in ("mpris:trackid","id"),("mpris:length","time"),("xesam:title","title"),("xesam:artist","artist"),("xesam:url","path"):
                myattr= getattr(self.player.playlist[id],attr,None)
                if myattr is not None:
                  if key == "mpris:length":
                    myattr=long(round(myattr/1000.))
                  meta[key]=myattr
                    
            metadata.append(meta)

        return metadata

    @dbus.service.property(TRACKLIST_IFACE, signature="as")
    def Tracks(self):
        tracks=[]
        for track in self.player.playlist:
            tracks.append(track)
        return tracks


    @dbus.service.property(TRACKLIST_IFACE, signature="b")
    def CanEditTracks(self):
        return True


    def addtrack(self,uri, aftertrack, setascurrent):

        if aftertrack == "/org/mpris/MediaPlayer2/TrackList/NoTrack":
            aftertrack=None

        self.player.playlist=self.player.playlist.addtrack(uri,aftertrack,setascurrent)

    def removetrack(self,uri, trackid):
        self.player.playlist.removetrack(self.player.playlist.index(trackid))

    def goto(self,trackid):
        self.playlist.set_current(self.player.playlist.index(trackid))
        self.stop()
        self.loaduri()
        self.play()

class Player:
	
  def __init__(self,myplaylist=None):
    self.playlist=myplaylist
    self.player = gst.element_factory_make("playbin2", "playbin2")
    self.playmode = "Stopped"

    if self.player is None:
        logging.error( "creating player")

    fakesink = gst.element_factory_make("fakesink", "fakesink")
    self.player.set_property("video-sink", fakesink)
    bus = self.player.get_bus()
    bus.add_signal_watch()
    #bus.connect("message", self.on_message)
    bus.connect('message::eos',           self.on_message_eos)
    bus.connect('message::error',         self.on_message_error)
    bus.connect("message::state-changed", self.on_message_state_changed)

  def on_message(self,bus, message):
    logging.debug('gst-bus: %s' % str(message))
    # log all error messages
    if message.type == gst.MESSAGE_ERROR:
      error, debug = map(str, message.parse_error())
      logging.error('gstreamer_autoplayer: %s'%error)
      logging.debug('gstreamer_autoplayer: %s'%debug)

  def on_message_eos(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 

    logging.info( "fine file")
    self.player.set_state(gst.STATE_NULL)      
    self.next()


  def on_message_error(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 

    self.player.set_state(gst.STATE_NULL)
    err, debug = message.parse_error()
    logging.error( " %s: %s " % (err, debug))
    self.playmode = "Stopped"


  def on_message_state_changed(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 
    
    if isinstance(message.src, gst.Pipeline):
      old_state, new_state, pending_state = message.parse_state_changed()

      # gst.STATE_NULL	    the NULL state or initial state of an element
      # gst.STATE_PAUSED	    the element is PAUSED
      # gst.STATE_PLAYING	    the element is PLAYING
      # gst.STATE_READY	    the element is ready to go to PAUSED
      # gst.STATE_VOID_PENDING    no pending state

      if pending_state == gst.STATE_VOID_PENDING:

        logging.info("Pipeline state changed from %s to %s. Pendig: %s"%
                     (gst.element_state_get_name(old_state),
                      gst.element_state_get_name (new_state),
                      gst.element_state_get_name (pending_state)))
        
        if new_state == gst.STATE_NULL :
          self.playmode = "Stopped"
        elif new_state == gst.STATE_PAUSED:
          self.playmode = "Paused"
        elif new_state == gst.STATE_PLAYING :
          self.playmode = "Playing"


  def on_message_old(self, bus, message):

    t = message.type
    logging.info("Message type %s received; source %s" % (t,type(message.src))) 

    if t == gst.MESSAGE_EOS:
      logging.info( "fine file")
      self.player.set_state(gst.STATE_NULL)      
      self.next()

    elif t == gst.MESSAGE_ERROR:
      self.player.set_state(gst.STATE_NULL)
      err, debug = message.parse_error()
      logging.error( " %s: %s " % (err, debug))
      self.playmode = "Stopped"

    elif t == gst.MESSAGE_STATE_CHANGED:
      if isinstance(message.src, gst.Pipeline):
        old_state, new_state, pending_state = message.parse_state_changed()

        # gst.STATE_NULL	    the NULL state or initial state of an element
        # gst.STATE_PAUSED	    the element is PAUSED
        # gst.STATE_PLAYING	    the element is PLAYING
        # gst.STATE_READY	    the element is ready to go to PAUSED
        # gst.STATE_VOID_PENDING    no pending state

        if pending_state == gst.STATE_VOID_PENDING:

          logging.info("Pipeline state changed from %s to %s. Pendig: %s"%
                       (gst.element_state_get_name(old_state),
                        gst.element_state_get_name (new_state),
                        gst.element_state_get_name (pending_state)))

          if new_state == gst.STATE_NULL :
            self.playmode = "Stopped"
          elif new_state == gst.STATE_PAUSED:
            self.playmode = "Paused"
          elif new_state == gst.STATE_PLAYING :
            self.playmode = "Playing"

#        elif new_state == gst.STATE_READY :
#            self.playmode = "Stopped"
#        elif new_state == gst.STATE_VOID_PENDING:
#            self.playmode = "Stopped"
#      else:
#        old_state, new_state, pending_state = message.parse_state_changed()
#        logging.info("Non cagato state changed from %s to %s. Pendig: %s"%
#               (gst.element_state_get_name(old_state), gst.element_state_get_name (new_state),gst.element_state_get_name (pending_state)))


#    elif t == gst.MESSAGE_STREAM_STATUS:
#        logging.info("Message type %s received: %s" % (t,message)) 
  
#    else:
#        logging.info("Message type %s received" % t) 
#        logging.debug("Message type %s received: %s" % (t,message)) 
##      print >> sys.stderr," Unexpected message received.\n"
##      self.playmode = False


  def next(self):
      logging.info( "next")
      self.playlist.next()
      if self.playlist.current is None:
          logging.info( "end playlist")
          self.stop()
          self.playmode = "Stopped"
      else:
        playmode=self.playmode
        self.stop()
        self.loaduri()
        if playmode == "Playing":
          self.play()
        elif playmode == "Paused":
          self.pause()

  def previous(self):
      logging.info( "previous")
      self.playlist.previous()
      if self.playlist.current is None:
          logging.info( "head playlist")
          self.stop()
          self.playmode = "Stopped"
      else:
        playmode=self.playmode
        self.stop()
        self.loaduri()
        if playmode == "Playing":
          self.play()
        elif playmode == "Paused":
          self.pause()

  def convert_ns(self, t):
    s,ns = divmod(t, 1000000000)
    m,s = divmod(s, 60)
    
    if m < 60:
      return "%02i:%02i" %(m,s)
    else:
      h,m = divmod(m, 60)
    return "%i:%02i:%02i" %(h,m,s)


  def seek(self,t):
    """
    t in microseconds
    """

    logging.info("seek")
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      pos_int +=t
      logging.info("seek %s" % str(pos_int))
      self.setposition(self.playlist.current,pos_int)

    except:
      logging.error( "in seek")


  def setposition(self,trackid,t):
    """
    t in microseconds
    """

    if trackid != self.playlist.current:
        logging.warning( "setposition trackid is not current trackid")

    try:
      logging.info("set position")
      pos_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
      tnano=t*1000

      if tnano >= 0 and tnano <= pos_int : 
        logging.info("set position to: %s; len: %s" % (str(t),str(pos_int)))

        #if wait: self.playbin.get_state(timeout=50*gst.MSECOND)
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
                gst.SEEK_FLAG_FLUSH|gst.SEEK_FLAG_ACCURATE,
                gst.SEEK_TYPE_SET, tnano, gst.SEEK_TYPE_NONE, 0)
        res = self.player.send_event(event)
        if res:
          self.player.set_new_stream_time(0L)
        #if wait: self.playbin.get_state(timeout=50*gst.MSECOND)

        # this cause a doble seek with playbin2
        #self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, t)

    except:
        logging.error( "in setposition")

  def loaduri(self):
    logging.info( "loaduri")

    if self.playlist.get_current() is not None:
        uri = self.playlist.get_current().path
        if uri is not None:
            self.player.set_property("uri", uri)

    ret = self.player.set_state(gst.STATE_READY)
    if ret == gst.STATE_CHANGE_FAILURE:
        logging.error( "Unable to set the pipeline to the READY state.")


  def play(self):
    logging.info( "play")
    ret = self.player.set_state(gst.STATE_PLAYING)
    if ret == gst.STATE_CHANGE_FAILURE:
        logging.error( "Unable to set the pipeline to the playing state.")


  def pause(self):

    ret = self.player.set_state(gst.STATE_PAUSED)
    if ret == gst.STATE_CHANGE_FAILURE:
        logging.error( "Unable to set the pipeline to the pause state.")


  def playpause(self):

    if self.playmode == "Playing":
        self.pause()

    elif self.playmode == "Stopped":
        self.play()

    elif self.playmode == "Paused":
        self.play()


  def stop(self):

    #self.loaduri()
    ret = self.player.set_state(gst.STATE_NULL)
    if ret == gst.STATE_CHANGE_FAILURE:
      logging.error( "Unable to set the pipeline to the NULL state.")


#  def loop(self):
#    while self.playmode == "Playing":
#      try:
#        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
#        dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
#        if dur_int == -1:
#          continue
#        print self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)
#        #          self.forward_callback(60)
#      except gst.QueryError:
#        print "error calculating position" 
#			    
#      time.sleep(2)
#
#    print "end player"
#    loop.quit()



  def position(self):
    """
    return microseconds
    """
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]

    except(gst.QueryError):
      logging.warning( "gst.QueryError in query_position" )
      return None
			    
    return int(round(pos_int/1000.))


  def printinfo(self):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
#      if dur_int == -1:
#        print "bho"
      print self.playmode,self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)

    except(gst.QueryError):
        #print "error printinfo"
        pass

    return True

  def save_playlist(self,path):

    position=self.position()
    if position is None:
      self.playlist.position=position
    else:
      self.playlist.position=self.position()*1000

    try:
      self.playlist.write(path)
    except:
      logging.error( "errore saving playlist")

    logging.info ( "playlist saved %s" % path)
    return True


  def initialize(self):
    self.loaduri()
    self.pause()
    return False

  def recoverstatus(self):

    if self.playmode != "Paused":
      logging.info ( "wait for player going paused: %s" % self.playmode)
      return True

    time.sleep(1)
    logging.info ( "recover last status from disk")
    if self.playlist.position is not None:
      self.setposition(self.playlist.current,int(round(self.playlist.position/1000.)))
    time.sleep(1)
    self.play()

    return False

if __name__ == '__main__':
  # (this code was run as script)

  # Use logging for ouput at different *levels*.
  #
  logging.getLogger().setLevel(logging.INFO)
  log = logging.getLogger("autoplayer")
  handler = logging.StreamHandler(sys.stderr)
  log.addHandler(handler)
 
  logging.basicConfig(level=logging.INFO,)

  pl=playlist.Playlist()
  pl.read("autoplayer.xspf")
  plmpris=playlist.Playlist_mpris2(pl,pl.current,pl.position)

  for media in sys.argv[1:]:
      logging.info( "add media: %s" %media)
      plmpris=plmpris.addtrack(media,setascurrent=True)

  mp = Player(plmpris)

  try:  
      dbus_loop=dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
      session_bus = dbus.SessionBus(mainloop=dbus_loop)

      name = dbus.service.BusName('org.mpris.MediaPlayer2.AutoPlayer', session_bus)
      ap = AutoPlayer(session_bus, '/org/mpris/MediaPlayer2')
      ap.attach_player(mp)
      
      gobject.timeout_add(  100,ap.player.initialize)
      gobject.timeout_add(  200,ap.player.recoverstatus)
      gobject.timeout_add( 1000,ap.player.printinfo)
      gobject.timeout_add(60000,ap.player.save_playlist,"autoplayer.xspf")

      loop = gobject.MainLoop()
      loop.run()


#  thread.start_new_thread(mp.loop, ())
#  object.threads_init()
#  context = loop.get_context()
#  gobject.MainLoop().run()
#  while True:
#    context.iteration(True) 


  except KeyboardInterrupt :
      logging.info("save playlist: %s" % STATUS_PLAYLIST )
      ap.player.save_playlist(STATUS_PLAYLIST)
      loop.quit()
