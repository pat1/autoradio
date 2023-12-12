#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

#Connect to player
from mpris2.mediaplayer2 import MediaPlayer2
from mpris2.player import Player
from mpris2.tracklist import TrackList
from mpris2.interfaces import Interfaces
from mpris2.some_players import Some_Players
from mpris2.utils import get_players_uri
from mpris2.utils import get_session
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import dbus

def playhandler( *args, **kw): 
    #print args, kw
    playbackstatus = args[1].get("PlaybackStatus",None)
    position = args[1].get("Position",None)
    if playbackstatus is not None:
        print("PlaybackStatus",playbackstatus)
    if position is not None:
        print("Position", position)


def trackhandler( *args, **kw):
    print("forse track list replaced")
    print(args, kw)


DBusGMainLoop(set_as_default=True)
#import gobject
from gi.repository import GObject as gobject
#busaddress='tcp:host=localhost,port=1234'
busaddress=None

#mloop = gobject.MainLoop()
mloop = GLib.MainLoop ()

uris = get_players_uri(pattern=".",busaddress=busaddress)

for uri in uris:
    #uri = Interfaces.MEDIA_PLAYER + '.' + Some_Players.AUDACIOUS
    #uri = Interfaces.MEDIA_PLAYER + '.' + Some_Players.AUTOPLAYER
    #uri = Interfaces.MEDIA_PLAYER + '.' +'AutoPlayer'
    
    print(uri)
    
    if busaddress is None:
        bus = dbus.SessionBus()
    else:
        bus =dbus.bus.BusConnection(busaddress)
        
    mp2 = MediaPlayer2(dbus_interface_info={'dbus_uri': uri,'dbus_session':bus})
    play = Player(dbus_interface_info={'dbus_uri': uri,'dbus_session':bus})

    #Call methods
    #play.Next() # play next media
    
    #Get attributes
    #print play.Metadata #current media data
    print(play.PlaybackStatus)
    
    play.PropertiesChanged = playhandler

    try: 
        if mp2.HasTrackList:
            tl = TrackList(dbus_interface_info={'dbus_uri': uri,'dbus_session':bus})
            tl.PropertiesChanged = trackhandler
            tl.TrackListReplaced = trackhandler
            # attributes and methods together
            for track in  tl.GetTracksMetadata( tl.Tracks):
                print(track.get(u'mpris:trackid',None),track.get(u'mpris:length',None),track.get(u'xesam:artist',None), track.get(u'xesam:title',None))
    except:
        print("mmm audacious mpris2 interface is buggy")

    #play with the first player
    mloop.run()

else:
    print("No players availables")
    

#s = get_session()
#s.add_signal_receiver(handler, 
#                      "PropertiesChanged",
#                      "org.freedesktop.DBus.Properties",
#                      path="/org/mpris/MediaPlayer2")

#    Interfaces.SIGNAL,
#    Interfaces.PROPERTIES,
#    uri,
#    Interfaces.OBJECT_PATH)

#def my_handler(self, Position):
#    print 'handled', Position, type(Position)
#    print 'self handled', self.last_fn_return, type(self.last_fn_return)

