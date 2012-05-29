#!/usr/bin/env python
# GPL. (C) 2007-2012 Paolo Patruno.

import dbus
import time
import datetime
import os

# ------- dbus mpris2 interface ---------
# http://specifications.freedesktop.org/mpris-spec/latest/index.html
# this is only a draft becouse when I try in fedora 16 
# audacious do not have mpris2 interface
# audacious 3.2.2 have mpris2 plugin but do not implement the optional
# org.mpris.MediaPlayer2.TrackList and org.mpris.MediaPlayer2.Playlists interfaces
# amarok 2.5.0 have mpris2 interface but do not implement the optional
# org.mpris.MediaPlayer2.TrackList and org.mpris.MediaPlayer2.Playlists interfaces
# vlc-1.1.13 do not have mpris2 interface; we need vlc >= 2.0 (http://wiki.videolan.org/Twoflower)
# that I do not have

# About mpris2 and audacious:

#Issue #106 has been updated by John Lindgren.
#
#Status changed from New to Rejected
#
#These interfaces require a different type of playlist structure than that used in Audacious, so they will not be implemented.
#----------------------------------------
#Feature #106: mpris2 plugin do not implement optional org.mpris.MediaPlayer2.TrackList interface and org.mpris.MediaPlayer2.Playlists interface
#http://redmine.audacious-media-player.org/issues/106#change-309
#
#Author: Paolo Patruno
#Status: Rejected
#Priority: Minor
#Assignee: 
#Category: plugins/mpris2
#Target version: 
#Affects version: 3.2.2
#
#
#at http://specifications.freedesktop.org/mpris-spec/latest/index.html 
#
#Interface MediaPlayer2.Playlists
#Provides access to the media player's playlists.
#
#Interface MediaPlayer2.TrackList
#Provides access to a short list of tracks which were recently played or will be played shortly. This is intended to provide context to the c#urrently-playing track, rather than giving complete access to the media player's playlist.
#
#Those interfaces, if I am right, are not implemented in mpris2 plugin.
#-----------------------------------------------------------------------

import dbus

class mediaplayer:

    def __init__(self,player="audacious",session=0):

        try:
            self.bus = dbus.SessionBus()

            # -----------------------------------------------------------
            mediaplayer_obj      = self.bus.get_object("org.mpris.MediaPlayer2."+player, '/org/mpris/MediaPlayer2')

            self.root      = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2')
            self.player    = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.Player')
#            self.tracklist = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.TrackList')
#            self.playlists = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.Playlists')
            # -----------------------------------------------------------

        except:
            raise


    def __str__(self):
        return self.player.PlaybackStatus
    

    def play_ifnot(self):
        '''
        start playing if not.
        '''
        # I check if mediaplayer is playing .... otherside I try to play

        if (not self.player.PlaybackStatus == "Playing"):

            self.player.Play()


# TODO !!!


def main():

    mp=mediaplayer(player="amarok")
    mp.play_ifnot()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
