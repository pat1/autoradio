#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

#Connect to player
from autoradio.mpris2.mediaplayer2 import MediaPlayer2
from autoradio.mpris2.player import Player
from autoradio.mpris2.tracklist import TrackList
from autoradio.mpris2.interfaces import Interfaces
from autoradio.mpris2.some_players import Some_Players
from autoradio.mpris2.utils import get_players_uri
from autoradio.mpris2.utils import get_session
from dbus.mainloop.glib import DBusGMainLoop
import dbus

def playhandler( *args, **kw): 
    #print args, kw
    playbackstatus = args[2].get("PlaybackStatus",None)
    position = args[2].get("Position",None)
    if playbackstatus is not None:
        print "PlaybackStatus",playbackstatus
    if position is not None:
        print "Position", position


def trackhandler( *args, **kw): 
    print args, kw


DBusGMainLoop(set_as_default=True)
import gobject    
#busaddress='tcp:host=localhost,port=1234'
busaddress=None

mloop = gobject.MainLoop()

uris = get_players_uri(pattern=".",busaddress=busaddress)

if len(uris) >0 :
    uri=uris[0]
    #uri = Interfaces.MEDIA_PLAYER + '.' + Some_Players.AUDACIOUS
    #uri = Interfaces.MEDIA_PLAYER + '.' + Some_Players.AUTOPLAYER
    #uri = Interfaces.MEDIA_PLAYER + '.' +'AutoPlayer'

    print uri

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
    print play.PlaybackStatus

    play.PropertiesChanged = playhandler

    try: 
        if mp2.HasTrackList:
            tl = TrackList(dbus_interface_info={'dbus_uri': uri})
        # attributes and methods together
            for track in  tl.GetTracksMetadata( tl.Tracks):
                print  track.get(u'mpris:trackid',None),track.get(u'mpris:length',None),track.get(u'xesam:artist',None), track.get(u'xesam:title',None)
                tl.PropertiesChanged = trackhandler
    except:
        print "mmm audacious mpris2 interface is buggy"

    mloop.run()

else:
    print "No players availables"
    

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

