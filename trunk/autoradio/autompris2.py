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

import dbus

class mediaplayer:

    def __init__(self,player="vlc",session=0):

#qdbus --literal org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get org.mpris.MediaPlayer2.TrackList Tracks
#            import gobject
#            gobject.threads_init()
#            
#            from dbus import glib
#            glib.init_threads()

        self.bus = dbus.SessionBus()

        # -----------------------------------------------------------
        mediaplayer_obj      = self.bus.get_object("org.mpris.MediaPlayer2."+player, '/org/mpris/MediaPlayer2')

        self.root      = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2')
        self.player    = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.Player')
        self.Properties=dbus.Interface(mediaplayer_obj, "org.freedesktop.DBus.Properties")

        self.HasTrackList=self.Properties.Get("org.mpris.MediaPlayer2" ,"HasTrackList")
        # mmmmm  VLC return 0 !!!
        self.HasTrackList=1
        ###
        if self.HasTrackList == 1:
            self.tracklist = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.TrackList')
        #self.playlists = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.MediaPlayer2.Playlists')
        # -----------------------------------------------------------

    def __str__(self):
        return self.Properties.Get("org.mpris.MediaPlayer2.Player" ,"PlaybackStatus")
    

    def play_ifnot(self):
        '''
        start playing if not.
        '''
        # I check if mediaplayer is playing .... otherside I try to play

        if (not self.isplaying()):
            self.player.Play()

    def isplaying(self):
        '''
        return true if is playing.
        '''

        return self.Properties.Get("org.mpris.MediaPlayer2.Player" ,"PlaybackStatus") == "Playing"



    def get_playlist_securepos(self,securesec=10):
        '''
        Try to secure that there are some time (securesec) to complete all operations in time:
        if audacious change song during operation will be a big problem
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

                timed=datetime.timedelta(seconds=datetime.timedelta(microseconds=mtimelength).seconds)
                toend=timed-datetime.timedelta(seconds=datetime.timedelta(microseconds=mtimeposition).seconds)

                newpos=self.get_playlist_pos()

                print toend

                if (pos != newpos):
                    #inconsistenza: retry
                    print "retry"
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

                for prm in xrange(0,pos-atlast): 
                    self.tracklist.RemoveTrack( op[prm]  )

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

                print length,pos+atlast
                for prm in xrange(length-1,pos+atlast,-1): 
                    self.tracklist.RemoveTrack( op[prm] )

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
            if pos is None:
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
            while ( os.path.commonprefix ((filepath,"file://"+autopath)) == "file://"+autopath ):
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

        if self.HasTrackList == 1:
            return self.Properties.Get("org.mpris.MediaPlayer2.TrackList" ,"Tracks")
        else:
            raise Error

    def get_playlist_len(self):
        "get playlist lenght"
        
        if self.HasTrackList == 1:
            return len(self.Properties.Get("org.mpris.MediaPlayer2.TrackList" ,"Tracks"))
        else:
            return None


    def get_playlist_pos(self):
        "get current position"
        
        current=self.Properties.Get("org.mpris.MediaPlayer2.Player" ,"Metadata")["mpris:trackid"]
        metadatas=self.tracklist.GetTracksMetadata(self.get_playlist())
        
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

        metadatas=self.tracklist.GetTracksMetadata(self.get_playlist())
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
            current=self.Properties.Get("org.mpris.MediaPlayer2.Player" ,"Metadata")["mpris:trackid"]
            if metadata["mpris:trackid"] == current :
                mtimeposition=self.Properties.Get("org.mpris.MediaPlayer2.Player" ,"Position")
            else:
                mtimeposition=0
        except:
            mtimeposition=0


        mymeta={
            "file": file,
            "title": title,
            "artist": artist,
            "mtimelength": mtimelength,
            "mtimeposition": mtimeposition
            }

        return mymeta


    def playlist_add_atpos(self,media,pos):
        "add media at pos postion in the playlist"

        print self.get_playlist()[pos]

        self.tracklist.AddTrack(media,self.get_playlist()[pos],False)
        time.sleep(1)
        return None
            

def main():

    mp=mediaplayer(player="vlc")
    print mp
#    mp.play_ifnot()
#    print mp

#    for id  in xrange(mp.get_playlist_len()):
#        print mp.get_metadata(id)

    print mp.get_playlist_pos()
    print mp.get_playlist_securepos()
    print mp.playlist_clear_up(atlast=2)
    print mp.playlist_clear_down(atlast=5)
    print mp.get_playlist()
    posauto=mp.get_playlist_posauto(autopath="/casa")
    print mp.playlist_add_atpos("file:///home",posauto)

if __name__ == '__main__':
    main()  # (this code was run as script)
    
