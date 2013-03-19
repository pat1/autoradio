#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

# Authors: Paolo Patruno <p.patruno@iperbole.bologna.it> 
# Based on :
# mpDris2 from Jean-Philippe Braun <eon@patapon.info>,
#              Mantas Mikulėnas <grawity@gmail.com>
# mpDris from: Erik Karlsson <pilo@ayeon.org>
# Some bits taken from quodlibet mpris plugin by <christoph.reiter@gmx.at>

#TODO
# manage signal
# Interface MediaPlayer2.Player
# Signals
# Seeked 	(x: Position)
#
# Interface MediaPlayer2.TrackList
# Signals
# TrackListReplaced 	(ao: Tracks, o: CurrentTrack) 	
# TrackAdded 	(a{sv}: Metadata, o: AfterTrack) 	
# TrackRemoved 	(o: TrackId) 	
# TrackMetadataChanged 	(o: TrackId, a{sv}: Metadata) 	

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
import signal

IDENTITY = "Auto Player"
STATUS_PLAYLIST="autoplayer.xspf"

# python dbus bindings don't include annotations and properties
MPRIS2_INTROSPECTION = """<node name="/org/mpris/MediaPlayer2">
  <interface name="org.freedesktop.DBus.Introspectable">
    <method name="Introspect">
      <arg direction="out" name="xml_data" type="s"/>
    </method>
  </interface>
  <interface name="org.freedesktop.DBus.Properties">
    <method name="Get">
      <arg direction="in" name="interface_name" type="s"/>
      <arg direction="in" name="property_name" type="s"/>
      <arg direction="out" name="value" type="v"/>
    </method>
    <method name="GetAll">
      <arg direction="in" name="interface_name" type="s"/>
      <arg direction="out" name="properties" type="a{sv}"/>
    </method>
    <method name="Set">
      <arg direction="in" name="interface_name" type="s"/>
      <arg direction="in" name="property_name" type="s"/>
      <arg direction="in" name="value" type="v"/>
    </method>
    <signal name="PropertiesChanged">
      <arg name="interface_name" type="s"/>
      <arg name="changed_properties" type="a{sv}"/>
      <arg name="invalidated_properties" type="as"/>
    </signal>
  </interface>
  <interface name="org.mpris.MediaPlayer2">
    <method name="Raise"/>
    <method name="Quit"/>
    <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
    <property name="CanQuit" type="b" access="read"/>
    <property name="CanRaise" type="b" access="read"/>
    <property name="HasTrackList" type="b" access="read"/>
    <property name="Identity" type="s" access="read"/>
    <property name="DesktopEntry" type="s" access="read"/>
    <property name="SupportedUriSchemes" type="as" access="read"/>
    <property name="SupportedMimeTypes" type="as" access="read"/>
    <property name="CanSetFullscreen" type="b" access="read"/>
  </interface>
  <interface name="org.mpris.MediaPlayer2.Player">
    <method name="Next"/>
    <method name="Previous"/>
    <method name="Pause"/>
    <method name="PlayPause"/>
    <method name="Stop"/>
    <method name="Play"/>
    <method name="Seek">
      <arg direction="in" name="Offset" type="x"/>
    </method>
    <method name="SetPosition">
      <arg direction="in" name="TrackId" type="o"/>
      <arg direction="in" name="Position" type="x"/>
    </method>
    <method name="OpenUri">
      <arg direction="in" name="Uri" type="s"/>
    </method>
    <signal name="Seeked">
      <arg name="Position" type="x"/>
    </signal>
    <property name="PlaybackStatus" type="s" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="LoopStatus" type="s" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="Rate" type="d" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="Shuffle" type="b" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="Metadata" type="a{sv}" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="Volume" type="d" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
    </property>
    <property name="Position" type="x" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
    </property>
    <property name="MinimumRate" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="MaximumRate" type="d" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanGoNext" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanGoPrevious" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanPlay" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanPause" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanSeek" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
    </property>
    <property name="CanControl" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
    </property>
  </interface>
  <interface name="org.mpris.MediaPlayer2.TrackList">
    <property access="read" type="b" name="CanEditTracks" />
    <method name="GoTo">
      <arg direction="in"  type="s" name="trackid" />
    </method>
    <property access="read" type="as" name="Tracks" />
    <method name="AddTrack">
      <arg direction="in"  type="s" name="uri" />
      <arg direction="in"  type="s" name="aftertrack" />
      <arg direction="in"  type="b" name="setascurrent" />
    </method>
    <method name="GetTracksMetadata">
      <arg direction="in"  type="as" name="trackids" />
      <arg direction="out" type="aa{sv}" />
    </method>
    <method name="RemoveTrack">
      <arg direction="in"  type="s" name="trackid" />
    </method>
    <signal name="TrackListReplaced">
      <arg type="ao" />
      <arg type="o" />
    </signal>
    <signal name="TrackAdded">
      <arg type="a{sv}" />
      <arg type="o" />
    </signal>
    <signal name="TrackRemoved">
      <arg type="o" />
    </signal>
    <signal name="TrackMetadataChanged">
      <arg type="o" />
      <arg type="a{sv}" />
    </signal>
  </interface>
</node>"""

PLAYER_IFACE="org.mpris.MediaPlayer2.Player"
TRACKLIST_IFACE="org.mpris.MediaPlayer2.TrackList"
IFACE="org.mpris.MediaPlayer2"

class NotSupportedException(dbus.DBusException):
  _dbus_error_name = 'org.mpris.MediaPlayer2.Player.NotSupported'


class AutoPlayer(dbus.service.Object):
    ''' The base object of an MPRIS player '''

    __name = "org.mpris.MediaPlayer2.AutoPlayer"
    __path = "/org/mpris/MediaPlayer2"
    __introspect_interface = "org.freedesktop.DBus.Introspectable"
    __prop_interface = dbus.PROPERTIES_IFACE

    def __init__(self,busaddress=None):

        if busaddress is None:
          self._bus = dbus.SessionBus()
        else:
          self._bus =dbus.bus.BusConnection(busaddress)

        dbus.service.Object.__init__(self, self._bus,
                                     AutoPlayer.__path)


        self._uname = self._bus.get_unique_name()
        self._dbus_obj = self._bus.get_object("org.freedesktop.DBus",
                                              "/org/freedesktop/DBus")
        self._dbus_obj.connect_to_signal("NameOwnerChanged",
                                         self._name_owner_changed_callback,
                                         arg0=self.__name)

        self.acquire_name()

    def _name_owner_changed_callback(self, name, old_owner, new_owner):
        if name == self.__name and old_owner == self._uname and new_owner != "":
            try:
                pid = self._dbus_obj.GetConnectionUnixProcessID(new_owner)
            except:
                pid = None
            logging.info("Replaced by %s (PID %s)" % (new_owner, pid or "unknown"))
            self.player.loop.quit()

    def acquire_name(self):
        self._bus_name = dbus.service.BusName(AutoPlayer.__name,
                                              bus=self._bus,
                                              allow_replacement=True,
                                              replace_existing=True)
    def release_name(self):
        if hasattr(self, "_bus_name"):
            del self._bus_name


    def __PlaybackStatus(self):
        return self.player.playmode

    def __Metadata(self):

      meta=self.GetTracksMetadata((self.player.playlist.current,))
      if len(meta) > 0:
        return dbus.Dictionary(meta[0], signature='sv') 
      else:
        return dbus.Dictionary({}, signature='sv') 

      #return {"mpris:trackid":self.player.playlist.current,}

    def __Position(self):
      position = self.player.position()
      if position is None:
        return dbus.Int64(0)
      else:
        return dbus.Int64(position)

    def __CanPlay(self):
        if self.player.playlist.current is None :
            return False
        else:
            return True

    def __Tracks(self):

        tracks=dbus.Array([], signature='s')
        for track in self.player.playlist:
            tracks.append(track)
        return tracks


    __root_interface = IFACE
    __root_props = {
        "CanQuit": (True, None),
        "CanRaise": (False, None),
        "DesktopEntry": ("AutoPlayer", None),
        "HasTrackList": (True, None),
        "Identity": (IDENTITY, None),
        "SupportedUriSchemes": (dbus.Array(signature="s"), None),
        "SupportedMimeTypes": (dbus.Array(signature="s"), None),
        "CanSetFullscreen": (False, None),
    }

    __player_interface = PLAYER_IFACE
    __player_props = {
        "PlaybackStatus": (__PlaybackStatus, None),
        "LoopStatus": (False, None),
        "Rate": (1.0, None),
        "Shuffle": (False, None),
        "Metadata": (__Metadata, None),
        "Volume": (1.0, None),
        "Position": (__Position, None),
        "MinimumRate": (1.0, None),
        "MaximumRate": (1.0, None),
        "CanGoNext": (True, None),
        "CanGoPrevious": (True, None),
        "CanPlay": (__CanPlay, None),
        "CanPause": (True, None),
        "CanSeek": (True, None),
        "CanControl": (True, None),
    }

    __tracklist_interface = TRACKLIST_IFACE
    __tracklist_props = {
        "CanEditTracks": (True, None),
        "Tracks": (__Tracks, None),
}

    __prop_mapping = {
        __player_interface: __player_props,
        __root_interface: __root_props,
        __tracklist_interface: __tracklist_props,
    }


    @dbus.service.method(__introspect_interface)
    def Introspect(self):
        return MPRIS2_INTROSPECTION

    @dbus.service.signal(__prop_interface, signature="sa{sv}as")
    def PropertiesChanged(self, interface, changed_properties,
                          invalidated_properties):
        pass

    @dbus.service.method(__prop_interface,
                         in_signature="ss", out_signature="v")
    def Get(self, interface, prop):
        getter, setter = self.__prop_mapping[interface][prop]
        if callable(getter):
            return getter(self)
        return getter

    @dbus.service.method(__prop_interface,
                         in_signature="ssv", out_signature="")
    def Set(self, interface, prop, value):
        getter, setter = self.__prop_mapping[interface][prop]
        if setter is not None:
            setter(self,value)

    @dbus.service.method(__prop_interface,
                         in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        read_props = {}
        props = self.__prop_mapping[interface]
        for key, (getter, setter) in props.iteritems():
            if callable(getter):
                getter = getter(self)
            read_props[key] = getter
        return read_props

    def update_property(self, interface, prop):
        getter, setter = self.__prop_mapping[interface][prop]
        if callable(getter):
            value = getter(self)
        else:
            value = getter
        logging.debug('Updated property: %s = %s' % (prop, value))
        self.PropertiesChanged(interface, {prop: value}, [])
        return value


    def attach_player(self,player):
        self.player=player


    @dbus.service.signal(PLAYER_IFACE,signature='x')
    def Seeked(self, position):
      logging.debug("Seeked to %i" % position)
      return float(position)

    # TrackAdded 	(a{sv}: Metadata, o: AfterTrack) 	
    @dbus.service.signal(TRACKLIST_IFACE,signature='a{sv}o')
    def TrackAdded(self, metadata,aftertrack):
      logging.debug("TrackAdded to %s" % aftertrack)
      pass

    # TrackRemoved 	(o: TrackId) 	
    @dbus.service.signal(TRACKLIST_IFACE,signature='o')
    def TrackRemoved(self,trackid):
      logging.debug("TrackRemoved %s" % trackid)

# here seem pydbus bug 
# disabled for now

#process 22558: arguments to dbus_message_iter_append_basic() were incorrect, assertion "_dbus_check_is_valid_path (*string_p)" failed in file dbus-message.c line 2531.
#This is normally a bug in some application using the D-Bus library.
#  D-Bus not built with -rdynamic so unable to print a backtrace
#Annullato (core dumped)

      try:
        obp=dbus.ObjectPath("/org/mpris/MediaPlayer2/TrackList/"+trackid)
      except:
        logging.error("building ObjectPath to return in TrackRemoved %s" % trackid)
        obp=dbus.ObjectPath("/org/mpris/MediaPlayer2/TrackList/NoTrack")

      return obp 

    @dbus.service.method(IFACE)
    def Raise(self):
      pass

    @dbus.service.method(IFACE)
    def Quit(self):
      self.player.exit()
      self.release_name()

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

      logging.info( "Play")

      self.player.loaduri()
      self.player.play()

    @dbus.service.method(PLAYER_IFACE,in_signature='x')
    def Seek(self,offset):
      position=self.player.seek(offset)
      if position is not None: self.Seeked(position)

    @dbus.service.method(PLAYER_IFACE,in_signature='sx')
    def SetPosition(self,trackid,position):
      self.player.setposition(trackid,position)
      self.Seeked(position)

    @dbus.service.method(PLAYER_IFACE,in_signature='s')
    def OpenUri(self,uri):
      self.player.addtrack(uri,setascurrent=True)
      self.Stop()
      self.Play()

      #TODO
      #self.TrackAdded()
      #self.update_property(TRACKLIST_IFACE,'TrackListReplaced')

      # If the media player implements the TrackList interface, then the opened 
      # track should be made part of the tracklist, the 
      # org.mpris.MediaPlayer2.TrackList.TrackAdded
      # or 
      # org.mpris.MediaPlayer2.TrackList.TrackListReplaced
      # signal should be fired, as well as the
      # org.freedesktop.DBus.Properties.PropertiesChanged
      # signal on the tracklist interface. 


#tracklist

    @dbus.service.method(TRACKLIST_IFACE,in_signature='ssb', out_signature='')
    def AddTrack(self,uri, aftertrack, setascurrent):
        self.player.addtrack(uri, aftertrack, setascurrent)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='s', out_signature='')
    def RemoveTrack(self, trackid):
      if self.player.playlist.current == trackid:
        self.Next()
      self.player.removetrack(trackid)
      #disable for a bug in pydbus ??
      #self.TrackRemoved(trackid)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='s', out_signature='')
    def GoTo(self, trackid):
        self.player.goto(trackid)

    @dbus.service.method(TRACKLIST_IFACE,in_signature='as', out_signature='aa{sv}')
    def GetTracksMetadata(self,trackids):
        metadata=dbus.Array([], signature='aa{sv}')

        for id in trackids:
          if id is not None:
            meta={}
            for key,attr in ("mpris:trackid","id"),("mpris:length","time"),("xesam:title","title"),("xesam:artist","artist"),("xesam:url","path"):
                myattr= getattr(self.player.playlist[id],attr,None)
                if myattr is not None:
                  if key == "mpris:length":
                    myattr=long(round(myattr/1000.))
                  meta[key]=myattr
                    
            metadata.append(dbus.Dictionary(meta, signature='sv'))

        return metadata

    def updateinfo(self):
      if self.player.statuschanged:
        self.update_property(PLAYER_IFACE,"PlaybackStatus")
        self.player.statuschanged=False
      self.update_property(PLAYER_IFACE,"Position")
      return True


# Handle signals more gracefully
    def handle_sigint(self,signum, frame):
      logging.debug('Caught SIGINT, exiting.')
      self.Quit()


class Player:
	
  def __init__(self,myplaylist=None,loop=None,starttoplay=False,myaudiosink=None):
    self.playlist=myplaylist
    self.player = gst.element_factory_make("playbin2", "playbin2")
    self.playmode = "Stopped"
    self.recoverplaymode = "Stopped"
    self.statuschanged = False
    self.starttoplay=starttoplay
    self.loop=loop

    if self.player is None:
        logging.error( "creating player")

    fakesink = gst.element_factory_make("fakesink", "fakesink")
    self.player.set_property("video-sink", fakesink)

    ##icecast
    #print "Icecast selected"
    #bin = gst.Bin("my-bin")

    #audioconvert = gst.element_factory_make("audioconvert")
    #bin.add(audioconvert)
    #pad = audioconvert.get_pad("sink")
    #ghostpad = gst.GhostPad("sink", pad)
    #bin.add_pad(ghostpad)

    #audioresample = gst.element_factory_make("audioresample")
    #audioresample.set_property("quality", 0)
    #bin.add(audioresample)
    #capsfilter = gst.element_factory_make('capsfilter')
    #capsfilter.set_property('caps', gst.caps_from_string('audio/x-raw,rate=44100,channels=2'))
    ##bin.add(capsfilter)
    #vorbisenc = gst.element_factory_make("vorbisenc")
    #vorbisenc.set_property("quality", 0)
    #bin.add(vorbisenc)
    #oggmux = gst.element_factory_make("oggmux")
    #bin.add(oggmux)

    #streamsink = gst.element_factory_make("shout2send", "streamsink")
    #streamsink.set_property("ip", "localhost")
    ##streamsink.set_property("username", "source")
    #streamsink.set_property("password", "ackme")
    #streamsink.set_property("port", 8000)
    #streamsink.set_property("mount", "/myradio.ogg")
    #bin.add(streamsink)

    ### Link the elements
    #queue = gst.element_factory_make("queue", "queue")
    ##queue.link(audioresample, capsfilter)
    #bin.add(queue)

    #gst.element_link_many(audioconvert,audioresample,queue,vorbisenc,oggmux,streamsink)
    #self.player.set_property("audio-sink", bin)


    #audiosink = gst.element_factory_make("autoaudiosink")
    #audiosink = gst.element_factory_make("jackaudiosink")

    if myaudiosink is None: myaudiosink = "autoaudiosink"
    audiosink = gst.element_factory_make(myaudiosink)
    self.player.set_property("audio-sink", audiosink)

#
#    self.player.set_property("audio-sink", streamsink)

    bus = self.player.get_bus()
    bus.add_signal_watch()
#    bus.connect("message",                self.on_message)
    bus.connect('message::eos',           self.on_message_eos)
    bus.connect('message::error',         self.on_message_error)
    bus.connect("message::state-changed", self.on_message_state_changed)

#  def on_message(self,bus, message):
#    logging.debug('gst-bus: %s' % str(message))
#    # log all error messages
#    if message.type == gst.MESSAGE_ERROR:
#      error, debug = map(str, message.parse_error())
#      logging.error('gstreamer_autoplayer: %s'%error)
#      logging.debug('gstreamer_autoplayer: %s'%debug)

  def on_message_eos(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 

    logging.info( "fine file")
    #self.player.set_state(gst.STATE_NULL)      
    #self.playmode = "Stopped"
    #self.statuschanged = True
    self.next()

  def on_message_error(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 

    self.player.set_state(gst.STATE_NULL)
    err, debug = message.parse_error()
    logging.error( " %s: %s " % (err, debug))

    logging.warning("restart to play after an ERROR skipping current media")
    self.playmode= self.recoverplaymode
    self.next()
    
#    if err.domain == gst.RESOURCE_ERROR :
#      logging.warning("restart to play after an RESOURCE_ERROR")
#      self.playmode= self.recoverplaymode
#      self.next()
#    else:
#      logging.warning("stop to play after an ERROR")
#      self.stop()
#      self.playmode = "Stopped"
#      self.statuschanged = True


  def on_message_state_changed(self, bus, message):

    t = message.type
    logging.debug("Message type %s received; source %s" % (t,type(message.src))) 
    
    if isinstance(message.src, gst.Pipeline):
      old_state, new_state, pending_state = message.parse_state_changed()

      # gst.STATE_NULL	    the NULL state or initial state of an element
      # gst.STATE_PAUSED    the element is PAUSED
      # gst.STATE_PLAYING   the element is PLAYING
      # gst.STATE_READY	    the element is ready to go to PAUSED
      # gst.STATE_VOID_PENDING    no pending state

      if pending_state == gst.STATE_VOID_PENDING:

        logging.debug("Pipeline state changed from %s to %s. Pendig: %s"%
                     (gst.element_state_get_name(old_state),
                      gst.element_state_get_name (new_state),
                      gst.element_state_get_name (pending_state)))
        
        if new_state == gst.STATE_READY :
          self.playmode = "Stopped"
          self.statuschanged = True
        elif new_state == gst.STATE_PAUSED:
          self.playmode = "Paused"
          self.statuschanged = True
        elif new_state == gst.STATE_PLAYING :
          self.playmode = "Playing"
          self.statuschanged = True

  def next(self):
      logging.info( "next")
      self.playlist.next()
      if self.playlist.current is None:
          logging.info( "end playlist")
          self.stop()
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
      pos_int =pos_int/1000 + t
      logging.info("seek %s" % str(pos_int))
      self.setposition(self.playlist.current,pos_int)
      return pos_int
    except:
      logging.error( "in seek")
      return None

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
        logging.debug("set position to: %s; len: %s" % (str(t),str(pos_int)))

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

    if self.playlist.current is None:
      if len(self.playlist.keys()) > 0:
        self.playlist.set_current(self.playlist.keys()[0])

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
        logging.error( "Unable to set the pipeline to the PLAYING state.")
        self.recoverplaymode = "Playing"

    #else:
    #  print self.player.get_state(timeout=gst.CLOCK_TIME_NONE)

  def pause(self):
    logging.info( "pause")
    ret = self.player.set_state(gst.STATE_PAUSED)
    if ret == gst.STATE_CHANGE_FAILURE:
        logging.error( "Unable to set the pipeline to the PAUSED state.")
        self.recoverplaymode = "Paused"
    #else:
    #  print self.player.get_state(timeout=gst.CLOCK_TIME_NONE)

  def playpause(self):

    if self.playmode == "Playing":
      self.pause()

    elif self.playmode == "Stopped":
        self.loaduri()
        self.play()

    elif self.playmode == "Paused":
        self.play()


  def stop(self):
    logging.info( "stop")

    #self.loaduri()
    ret = self.player.set_state(gst.STATE_READY)
    if ret == gst.STATE_CHANGE_FAILURE:
      logging.error( "Unable to set the pipeline to the READY state.")
      self.recoverplaymode = "Stopped"

    #else:
    #  print self.player.get_state(timeout=gst.CLOCK_TIME_NONE)

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
      logging.error( "error saving playlist")
      raise
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
    logging.info ( "recover last status from disk: position %s" % self.playlist.position)
    if self.playlist.position is not None:
      logging.info ( "set current %s and position %s " % (self.playlist.current,int(round(self.playlist.position/1000.))))
      self.setposition(self.playlist.current,int(round(self.playlist.position/1000.)))
    if self.starttoplay:
      time.sleep(1)
      self.play()

    return False

  def addtrack(self,uri, aftertrack=None, setascurrent=False):

    if aftertrack == "/org/mpris/MediaPlayer2/TrackList/NoTrack":
      aftertrack=None

    current = self.playlist.current
    self.playlist=self.playlist.addtrack(uri,aftertrack,setascurrent)

    if setascurrent:
      playmode=self.playmode
      if self.playlist.current != current:
        self.stop()
        self.loaduri()
        if playmode == "Playing":
          self.play()
        elif playmode == "Paused":
          self.pause()
          
  def removetrack(self,trackid):
    self.playlist=self.playlist.removetrack(trackid)
    #print "indice: ",str(self.playlist.keys().index(trackid))
    #for id,track in enumerate(self.playlist):
    #  print id,track

  def goto(self,trackid):
    self.playlist.set_current(trackid)
    self.stop()
    self.loaduri()
    self.play()

  def exit(self):
    logging.info("save playlist: %s" % STATUS_PLAYLIST )
    self.save_playlist(STATUS_PLAYLIST)
    self.stop()
    self.loop.quit()


def main(busaddress=None,myaudiosink=None):  

  # Use logging for ouput at different *levels*.
  #
  logging.getLogger().setLevel(logging.INFO)
  log = logging.getLogger("autoplayer")
  handler = logging.StreamHandler(sys.stderr)
  log.addHandler(handler)
 
#  logging.basicConfig(level=logging.INFO,)

#  try:
#    os.chdir(cwd)
#  except:
#    pass


  pl=playlist.Playlist()
  pl.read("autoplayer.xspf")
  #plmpris=playlist.Playlist_mpris2(pl,pl.current,pl.position)
  plmpris=playlist.Playlist_mpris2(pl)

  if len(sys.argv) >= 2:
    #if you come from autoplayerd argv[1] is run/start/stop ...
    for media in sys.argv[2:]:
      logging.info( "add media: %s" %media)
      # mmm here seems not work ... the new plmpris is not good !!!
      plmpris=plmpris.addtrack(media,setascurrent=True)

  try:  
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    loop = gobject.MainLoop()
    mp = Player(plmpris,loop=loop,starttoplay=True,myaudiosink=myaudiosink)

    # Export our DBUS service
    #if not dbus_service:
    #dbus_service = MPRIS2Interface()
    #else:
    # Add our service to the session bus
    #  dbus_service.acquire_name()

    ap = AutoPlayer(busaddress=busaddress)
    ap.attach_player(mp)
      
    gobject.timeout_add(  100,ap.player.initialize)
    gobject.timeout_add(  200,ap.player.recoverstatus)
    gobject.timeout_add(  500,ap.updateinfo)
    gobject.timeout_add(60000,ap.player.save_playlist,"autoplayer.xspf")
    #gobject.timeout_add( 1000,ap.player.printinfo)

    signal.signal(signal.SIGINT, ap.handle_sigint)

    loop.run()

    # Clean up
    logging.debug('Exiting')


  except KeyboardInterrupt :
    # Clean up
    logging.debug('Keyboard Exiting')
    ap.Quit()

#  thread.start_new_thread(mp.loop, ())
#  object.threads_init()
#  context = loop.get_context()
#  gobject.MainLoop().run()
#  while True:
#    context.iteration(True) 

if __name__ == '__main__':

  main()# (this code was run as script)

