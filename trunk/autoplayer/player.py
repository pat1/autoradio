#!/usr/bin/env python

import sys, os, time, thread
import glib, gobject
import pygst
pygst.require("0.10")
import gst


class Player:
	
  def __init__(self):
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
      self.playmode = False
      print "fine file"
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
#      print >> sys.stderr, "Unexpected message received.\n"
#      self.playmode = False


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
	
  def start(self):
    for uri in sys.argv[1:]:
      self.player.set_property("uri", uri)
      ret = self.player.set_state(gst.STATE_PLAYING)
      if ret == gst.STATE_CHANGE_FAILURE:
        print >> sys.stderr, "Unable to set the pipeline to the playing state."
        self.playmode = False
      else:
        self.playmode = True

      while self.playmode:
        try:
          pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
          dur_int = self.player.query_duration(gst.FORMAT_TIME, None)[0]
          if dur_int == -1:
            continue
#          print self.convert_ns(pos_int)+"//"+self.convert_ns(dur_int)
#                        self.forward_callback(5)
        except:
          print "error calculating position" 
			    
          time.sleep(1)

    loop.quit()

mainclass = Player()
thread.start_new_thread(mainclass.start, ())
gobject.threads_init()
loop = glib.MainLoop()
loop.run()
