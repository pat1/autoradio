#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2012 Paolo Patruno.

import sys, time, thread
import glib, gobject
import pygst
pygst.require("0.10")
import gst
import playlist
import gobject

import dbus
import dbus.service
import dbus.mainloop.glib
import logging

PLAYER_IFACE="org.mpris.MediaPlayer2.Player"
TRACKLIST_IFACE="org.mpris.MediaPlayer2.TrackList"
IFACE="org.mpris.MediaPlayer2"


#
# Use logging for ouput at different *levels*.
#
logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger("mkplaylist")
handler = logging.StreamHandler(sys.stderr)
log.addHandler(handler)


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
        self.player.playlist.write("autoplayer.xspf")
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
        return None

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def Rate(self):
        return 1.0

    @dbus.service.property(PLAYER_IFACE, signature="b")
    def Shuffle(self):
        #raise
        return None

    @dbus.service.property(PLAYER_IFACE, signature="a{sv}")
    def Metadata(self):
        #raise
        return {"mpris:trackid":self.player.playlist.current,}

    @dbus.service.property(PLAYER_IFACE, signature="d")
    def Volume(self):
        #raise
        return None

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
        if current is None :
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
        #todo
        metadata=[]
        for id in trackids:
            metadata.append({"mpris:trackid":id,
                             "mpris:length":self.player.playlist[id].time,
                             "xesam:title":self.player.playlist[id].title,
                             "xesam:artist":self.player.playlist[id].artist,
                             "xesam:url":self.player.playlist[id].path})
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

        self.player=self.player.playlist.addtrack(uri,aftertrack,setascurrent)

    def removetrack(self,uri, trackid):
        self.player.playlist.removetrack(self.player.playlist.index(trackid))

    def goto(self,trackid):
        self.playlist.set_current(self.player.playlist.index(trackid))
        self.stop()
        self.play()

class Player:
	
  def __init__(self,myplaylist=None):
    self.playlist=myplaylist
    self.player = gst.element_factory_make("playbin2", "player")
    self.playmode = "Stopped"
    if self.player is None:
      print "Error: creating player"
    fakesink = gst.element_factory_make("fakesink", "fakesink")
    self.player.set_property("video-sink", fakesink)
    bus = self.player.get_bus()
    bus.add_signal_watch()
    bus.connect("message", self.on_message)

  def on_message(self, bus, message):

    t = message.type
    if t == gst.MESSAGE_EOS:
      self.player.set_state(gst.STATE_NULL)
      print "fine file"
      self.playlist.next()
      if self.playlist.current is None:
        self.playmode = "Stopped"
        print "fine playlist"
      else:
        self.play()

    elif t == gst.MESSAGE_ERROR:
      self.player.set_state(gst.STATE_NULL)
      err, debug = message.parse_error()
      print "Error: %s" % err, debug
      self.playmode = "Stopped"

    elif t == gst.MESSAGE_STATE_CHANGED:
      if isinstance(message.src, gst.Pipeline):
        old_state, new_state, pending_state = message.parse_state_changed()
        print ("Pipeline state changed from %s to %s."%
               (gst.element_state_get_name(old_state), gst.element_state_get_name (new_state)))
#    else:
#      print >> sys.stderr," Unexpected message received.\n"
##      self.playmode = False


  def next(self):
      print "next"
      self.playlist.next()
      if self.playlist.current is None:
          self.playmode = "Stopped"
          print "fine playlist"
      else:
          self.stop()
          self.play()

  def previous(self):
      print "previous"
      self.playlist.previous()
      if self.playlist.current is None:
          self.playmode = "Stopped"
          print "fine playlist"
      else:
          self.stop()
          self.play()


  def convert_ns(self, t):
    s,ns = divmod(t, 1000000000)
    m,s = divmod(s, 60)
    
    if m < 60:
      return "%02i:%02i" %(m,s)
    else:
      h,m = divmod(m, 60)
    return "%i:%02i:%02i" %(h,m,s)


  def seek(self,t):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, pos_int + t )
    except:
      print "error in seek"


  def setposition(self,trackid,t):
    try:
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        if t >= 0 and t <= pos_int : 
            self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, t)
    except:
        print "error in setposition"
	
  def play(self):
    print "play"
    if self.playlist.get_current() is None:
      self.playmode = "Stopped"
    else:
        uri = self.playlist.get_current().path
        if uri is not None:
            self.player.set_property("uri", uri)
            ret = self.player.set_state(gst.STATE_PLAYING)
            if ret == gst.STATE_CHANGE_FAILURE:
                print >> sys.stderr, "Unable to set the pipeline to the playing state."
            else:
                self.playmode = "Playing"
        else:
            self.playmode = "Stopped"

    return True


  def pause(self):

    uri = self.playlist.get_current()
    if uri is not None:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_PAUSED)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the pause state."
      else:
        self.playmode = "Paused"
    else:
      self.playmode = "Stopped"
    return True


  def stop(self):

    uri = self.playlist.get_current()
    if uri is not None:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_READY)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the stop state."
      else:
        self.playmode = "Stopped"
    else:
      self.playmode = "Stopped"
    return True

  def loop(self):
    while self.playmode == "Playing":
      try:
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
        if dur_int == -1:
          continue
        print self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)
        #          self.forward_callback(60)
      except gst.QueryError:
        print "error calculating position" 
			    
      time.sleep(2)

    print "end player"
    loop.quit()



  def position(self):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]

    except(gst.QueryError):
      pass
			    
    return pos_int


  def printinfo(self):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
#      if dur_int == -1:
#        print "bho"
      print self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)
      #          self.forward_callback(60)

    except(gst.QueryError):
        print "error printinfo"

    return True

  def save_playlist(self,path):
      try:
          self.playlist.write(path)
      except:
          print "errore saving playlist"

      print "playlist saved",path
      return True

if __name__ == '__main__':
  # (this code was run as script)

  logging.basicConfig(level=logging.DEBUG,)

  pl=playlist.Playlist()
  pl.read("autoplayer.xspf")
  plmpris=playlist.Playlist_mpris2(pl)

  for media in sys.argv[1:]:
      print "add media:",media
      plmpris=plmpris.addtrack(media,setascurrent=True)

  mp = Player(plmpris)
  mp.play()
#  thread.start_new_thread(mp.loop, ())

  try:
  
      dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

      gobject.threads_init()
      loop = gobject.MainLoop()
#  context = loop.get_context()

      session_bus = dbus.SessionBus()
      name = dbus.service.BusName('org.mpris.MediaPlayer2.AutoPlayer', session_bus)
      ap = AutoPlayer(session_bus, '/org/mpris/MediaPlayer2')
      ap.attach_player(mp)
      
#  gobject.MainLoop().run()

      gobject.timeout_add( 1000,ap.player.printinfo)
      gobject.timeout_add(60000,ap.player.save_playlist,"autoplayer.xspf")

#  while True:
#    context.iteration(True) 

      loop.run()

  except KeyboardInterrupt :
      ap.player.playlist.write("autoplayer.xspf")
      loop.quit()
