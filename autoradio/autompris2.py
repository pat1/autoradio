#!/usr/bin/env python
# GPL. (C) 2007-2012 Paolo Patruno.

from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import dbus
import time
import datetime
import os,sys
from gi.repository import GObject as gobject

from . import settings
from dbus.mainloop.glib import DBusGMainLoop
from .mpris2.mediaplayer2 import MediaPlayer2
from .mpris2.player import Player
from .mpris2.tracklist import TrackList
from .mpris2.interfaces import Interfaces
from .mpris2.some_players import Some_Players
from .mpris2.utils import get_players_uri
from .mpris2.utils import get_session

# ------- dbus mpris2 interface ---------
# http://specifications.freedesktop.org/mpris-spec/latest/index.html
# this is only a draft becouse when I try in fedora 16 
# audacious do not have mpris2 interface
# audacious 3.2.2 have mpris2 plugin but do not implement the optional
# org.mpris.MediaPlayer2.TrackList and org.mpris.MediaPlayer2.Playlists interfaces
# amarok 2.5.0 have mpris2 interface but do not implement the optional
# org.mpris.MediaPlayer2.TrackList and org.mpris.MediaPlayer2.Playlists interfaces
# vlc-1.1.13 do not have mpris2 interface; we need vlc >= 2.0 (http://wiki.videolan.org/Twoflower)
# that is available from pat1 repo for Fedora 16

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
#Provides access to a short list of tracks which were recently played or will be played shortly. This is intended to provide context to the
#currently-playing track, rather than giving complete access to the media player's playlist.
#
#Those interfaces, if I am right, are not implemented in mpris2 plugin.
#-----------------------------------------------------------------------


class mediaplayer(object):

    def __init__(self,player="AutoPlayer",session=0, busaddress=settings.busaddressplayer):

#qdbus --literal org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get org.mpris.MediaPlayer2.TrackList Tracks
#            import gobject
#            gobject.threads_init()
#            
#            from dbus import glib
#            glib.init_threads()

        DBusGMainLoop(set_as_default=True)

        uris = list(get_players_uri(pattern=".*"+player+"$",busaddress=busaddress))

        if len(uris) >0 :
            uri=uris[0]
            if busaddress is None:
                self.bus = dbus.SessionBus()
            else:
                self.bus = dbus.bus.BusConnection(busaddress)

            self.mp2 = MediaPlayer2(dbus_interface_info={'dbus_uri': uri,'dbus_session':self.bus})
            self.play = Player(dbus_interface_info={'dbus_uri': uri,'dbus_session':self.bus})
        else:
            print("No players availables")
            return

        if self.mp2.HasTrackList:
            self.tl = TrackList(dbus_interface_info={'dbus_uri': uri,'dbus_session':self.bus})
        else:
            self.tl = None

    def __str__(self):
        return self.play.PlaybackStatus
    

    def play_ifnot(self):
        '''
        start playing if not.
        '''
        # I check if mediaplayer is playing .... otherside I try to play

        if (not self.isplaying()):
            self.play.Play()

    def isplaying(self):
        '''
        return true if is playing.
        '''

        return self.play.PlaybackStatus == "Playing"



    def get_playlist_securepos(self,securesec=20):
        '''
        Try to secure that there are some time (securesec) to complete all operations in time:
        if the player change song during operation will be a big problem
        '''
        try:
 
            self.play_ifnot()   #force to play

            mintimed=datetime.timedelta(seconds=securesec)
            toend=datetime.timedelta(seconds=0)
            volte=0

            while ( toend < mintimed ):
                # take the current position

                pos=self.get_playlist_pos()
                metadata=self.get_metadata(pos)

                mtimelength=metadata["mtimelength"]
                mtimeposition=metadata["mtimeposition"]

                timed=datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimelength).seconds)
                toend=timed-datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimeposition).seconds)

                newpos=self.get_playlist_pos()

                if (pos != newpos):
                    #inconsistenza: retry
                    #print "retry"
                    toend=datetime.timedelta(seconds=0)

                if ( toend < mintimed ):
                    volte +=1
                    if volte > 10 :
                        break                       # timeout , I have to play
                    time.sleep(securesec+1)
            return pos

        except :
            return None


    def playlist_clear_up(self,atlast=10):
        '''
        clear playlist starting from current position up.
        "atlast" numer of song are retained
        '''
        try:
            self.play_ifnot()   #force to play

            # take the current position (if error set pos=0)
            pos=self.get_playlist_securepos()
            if pos is None:
                return False

                # delete the old ones
            if pos > atlast :

                op=self.get_playlist()

                for prm in range(0,pos-atlast): 
                    #print "remove up: ",op[prm]
                    self.tl.RemoveTrack( str(op[prm]))

            time.sleep(1)
            return True

        except:
            return False



    def playlist_clear_down(self,atlast=500):
        '''
        clear playlist starting from current position + atlast doen.
        "atlast" numer of song are retained for future play
        '''
        try:
            self.play_ifnot()   #force to play

           # take the current position (if error set pos=0)
            pos=self.get_playlist_securepos()
            if pos is None:
                return False

            length=self.get_playlist_len()

                #elimino il troppo
            if length-pos > atlast :

                op=self.get_playlist()

                for prm in range(length-1,pos+atlast,-1): 
                    #print "remove down: ",op[prm]
                    self.tl.RemoveTrack( str(op[prm]) )

            time.sleep(1)
            return True

        except:
            return False



    def get_playlist_posauto(self,autopath,securesec=10):
        '''
        get  playlist position skipping file with path equal to  autopath.
        Try to secure that there are some time (securesec) to complete all operations in time:
        if player change song during operation will be a big problem
        '''

        try:

            pos=self.get_playlist_securepos(securesec=securesec)
            if pos is None or pos+1 == self.get_playlist_len():
                return pos

            pos+=1

            metadata=self.get_metadata(pos)

            try:
                file=metadata["file"]

            except:
                return pos

            filepath=os.path.dirname(file)

            #print "file://"+autopath
            #print os.path.commonprefix ((filepath,"file://"+autopath))

            # ora controllo se ci sono gia dei file accodati nella playlist da autoradio
            # l'unica possibilita di saperlo e verificare il path del file
            while ( os.path.commonprefix ((filepath,"file://"+autopath)) == "file://"+autopath 
                    and
                    pos+1 < self.get_playlist_len()):
                pos+=1

                metadata=self.get_metadata(pos)
                try:
                    file=metadata["file"]
                except:
                    return pos

                filepath=os.path.dirname(file)

            # here I have found the first file added by autoradio
            return pos-1

        except :
            return None



    def get_playlist(self):
        "get playlist"

        if self.tl is not None:
            return self.tl.Tracks
        else:
            raise Error

    def get_playlist_len(self):
        "get playlist lenght"
        
        if self.tl is not None:
            return len(self.tl.Tracks)
        else:
            return None


    def get_playlist_pos(self):
        "get current position"
        
        try:
            current=self.play.Metadata["mpris:trackid"]
        except:
            return None

        metadatas=self.tl.GetTracksMetadata(self.get_playlist())
        
        id=0
        for metadata in metadatas:
            if metadata["mpris:trackid"] == current:
                return id
            id +=1

        return None

    def get_metadata(self,pos=None):
        "get metadata for position"

        if pos is None:
            return None

        metadatas=self.tl.GetTracksMetadata(self.get_playlist())
        metadata=metadatas[pos]

        try:
            file=metadata["xesam:url"]
        except:
            file=None
        try:
            title=metadata["xesam:title"]
            if title=="":
                title=None
        except:
            title=None

        try:
            artist=metadata["xesam:artist"]
            if artist=="":
                artist=None
        except:
            artist=None

        try:
            mtimelength=metadata["mpris:length"]
        except:
            mtimelength=0

        try:
            # get current truck
            current=self.play.Metadata["mpris:trackid"]
            if metadata["mpris:trackid"] == current :
                mtimeposition=self.play.Position
            else:
                mtimeposition=0
        except:
            mtimeposition=0


        mymeta={
            "file": file,
            "title": title,
            "artist": artist,
            "mtimelength": int(round(old_div(mtimelength,1000.))),
            "mtimeposition": int(round(old_div(mtimeposition,1000.)))
            }

        return mymeta


    def playlist_add_atpos(self,media,pos):
        "add media at pos postion in the playlist"

        if pos is not None:
            self.tl.AddTrack(media,self.get_playlist()[pos],False)
        else:
            # the playlist is empty
            self.tl.AddTrack(media,"/org/mpris/MediaPlayer2/TrackList/NoTrack",False)

        time.sleep(1)
        return None

# old style syntax:
#
#    def trackremoved_callback(self,op):
#        print "removed:",op
#            
#    def trackadded_callback(self,diz,op):
#        print "added:",diz
#        print "added:",op
#            
#    def connect(self):
#        self.tracklist.connect_to_signal('TrackRemoved', self.trackremoved_callback)
#        self.tracklist.connect_to_signal('TrackAdded', self.trackadded_callback)

    def loop(self):
        '''start the main loop'''
        mainloop = gobject.MainLoop()
        mainloop.run()

def main():

#    must be done before connecting to DBus
#    DBusGMainLoop(set_as_default=True,

    mp=mediaplayer(player="AutoPlayer")
    print("status",mp)
#    mp.play_ifnot()
#    print mp

#    for id  in xrange(mp.get_playlist_len()):
#        print mp.get_metadata(id)

    #mp.connect()
    #print "connected"
    #mp.loop()
    print("pos",mp.get_playlist_pos())
    print("securepos")
    print(mp.get_playlist_securepos())
    print("clear_up")
    print(mp.playlist_clear_up(atlast=2))
    print("clear_down")
    print(mp.playlist_clear_down(atlast=3))
    print("playlist")
    print(mp.get_playlist())
    posauto=mp.get_playlist_posauto(autopath="/casa")
    print("posauto",posauto)
    print("add_atpos")
    mp.playlist_add_atpos("file:///home",posauto)
    ##mp.playlist_add_atpos("file:///home",3)

if __name__ == '__main__':
    main()  # (this code was run as script)
    
