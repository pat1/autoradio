#!/usr/bin/env python

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

class AutoPlayerException(dbus.DBusException):
    _dbus_error_name = 'com.example.AutoPlayerException'

class AutoPlayer(dbus.service.Object):

    @dbus.service.method("com.example.AutoPlayerInterface")
    def Pause(self):
      pl.pause()

    @dbus.service.method("com.example.AutoPlayerInterface")
    def Stop(self):
      pl.stop()

    @dbus.service.method("com.example.AutoPlayerInterface")
    def Play(self):
      pl.play()

    @dbus.service.method("com.example.AutoPlayerInterface",
                         in_signature='', out_signature='')
    def RaiseException(self):
        raise AutoPlayerException('The RaiseException method does what you might '
                            'expect')

    @dbus.service.method("com.example.AutoPlayerInterface",
                         in_signature='', out_signature='(ss)')
    def GetTuple(self):
        return ("Hello Tuple", " from example-service.py")

    @dbus.service.method("com.example.AutoPlayerInterface",
                         in_signature='', out_signature='a{ss}')
    def GetDict(self):
        return {"first": "Hello Dict", "second": " from example-service.py"}

    @dbus.service.method("com.example.AutoPlayerInterface",
                         in_signature='', out_signature='')
    def Exit(self):
        loop.quit()


class Player:
	
  def __init__(self,myplaylist=None):
    self.playlist=myplaylist
    self.player = gst.element_factory_make("playbin2", "player")
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
      self.playlist.advance()
      if self.playlist.current is None:
        self.playmode = False
        print "fine playlist"
      else:
        self.play()

    elif t == gst.MESSAGE_ERROR:
      self.player.set_state(gst.STATE_NULL)
      err, debug = message.parse_error()
      print "Error: %s" % err, debug
      self.playmode = False

    elif t == gst.MESSAGE_STATE_CHANGED:
      if isinstance(message.src, gst.Pipeline):
        old_state, new_state, pending_state = message.parse_state_changed()
        print ("Pipeline state changed from %s to %s."%
               (gst.element_state_get_name(old_state), gst.element_state_get_name (new_state)))
#    else:
#      print >> sys.stderr," Unexpected message received.\n"
##      self.playmode = False


  def convert_ns(self, t):
    s,ns = divmod(t, 1000000000)
    m,s = divmod(s, 60)
    
    if m < 60:
      return "%02i:%02i" %(m,s)
    else:
      h,m = divmod(m, 60)
    return "%i:%02i:%02i" %(h,m,s)


  def rewind_callback(self,t):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      seek_ns = pos_int - (t * 1000000000)
      self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
    except:
      print "error in seek rewind"

  def forward_callback(self,t):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      seek_ns = pos_int + (t * 1000000000)
      self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)
    except:
      print "error in seek forward"
	
  def play(self):

    uri = self.playlist.get_current()
    if uri is not None:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_PLAYING)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the playing state."
      else:
        self.playmode = True
    else:
      self.playmode = False
    return True


  def pause(self):

    uri = self.playlist.get_current()
    if uri is not None:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_PAUSED)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the pause state."
      else:
        self.playmode = False
    else:
      self.playmode = False
    return True


  def stop(self):

    uri = self.playlist.get_current()
    if uri is not None:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_READY)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the stop state."
      else:
        self.playmode = False
    else:
      self.playmode = False
    return True

  def loop(self):
    while self.playmode:
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

  def printinfo(self):
    try:
      pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
      dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
#      if dur_int == -1:
#        print "bho"
      print self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)
      #          self.forward_callback(60)

    except(gst.QueryError):
      pass
			    
    return True


if __name__ == '__main__':
  # (this code was run as script)
  pl=playlist.Playlist(sys.argv[1:])
#  p=Player(pl)
#  p.start()
  print pl

  pl = Player(pl)
  pl.play()
#  thread.start_new_thread(pl.loop, ())
  
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

  gobject.threads_init()
  loop = gobject.MainLoop()
  context = loop.get_context()

  session_bus = dbus.SessionBus()
  name = dbus.service.BusName('com.example.AutoPlayer', session_bus)
  object = AutoPlayer(session_bus, '/player')

#  gobject.MainLoop().run()

  gobject.timeout_add(1000,pl.printinfo)  
#  gobject.timeout_add(1000,pl.pause)  
#  gobject.timeout_add(1230,pl.play)  
  while True:
    context.iteration(True) 

#  try:
#  except(KeyboardInterrupt):
#    print "vorrei uscire, grazie !"
#    loop.quit()

#  loop.run()

