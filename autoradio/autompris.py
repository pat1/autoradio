#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

# ------- dbus mpris 1 interface ---------
# note that this work for audacious only
# mpris version 1 do not provide interface to insert media
# at specified position in playlist
# so we have to wait players to implement mpris2 specification to generalize this interface.
# Audacious provide non standard interface to do this
# ----------------------------------------

import dbus
import time
import datetime
import os
import logging
import dbus


class mediaplayer:


    def __init__(self,player="audacious",session=0):

        self.mediaplayer=player
        self.session=session

        try:
            self.bus = dbus.SessionBus()

            # -----------------------------------------------------------
            root_obj      = self.bus.get_object("org.mpris."+player, '/')
            player_obj    = self.bus.get_object("org.mpris."+player, '/Player')
            tracklist_obj = self.bus.get_object("org.mpris."+player, '/TrackList')

            self.root      = dbus.Interface(root_obj,      dbus_interface='org.freedesktop.MediaPlayer')
            self.player    = dbus.Interface(player_obj,    dbus_interface='org.freedesktop.MediaPlayer')
            self.tracklist = dbus.Interface(tracklist_obj, dbus_interface='org.freedesktop.MediaPlayer')

            if player == "audacious":
                org_obj       = self.bus.get_object("org.mpris.audacious", '/org/atheme/audacious')
                self.org      = dbus.Interface(org_obj,       dbus_interface='org.atheme.audacious')

            # -----------------------------------------------------------

        except:
            raise


        if player == "audacious":

            from distutils.version import LooseVersion
            reqversion=LooseVersion("1.5")
            version=LooseVersion("0.0")

            try:
                # aud.root.Identity()
                version=LooseVersion(self.org.Version())
                logging.info("mediaplayer: audacious version: %s" % str(version))

            except:
                logging.error("mediaplayer: eror gettin audacious version")
   
            if ( version < reqversion ):
                logging.error("mediaplayer: audacious %s version is wrong (>=1.5) " % version )
                raise Exception


    def __str__(self):
        return "mpris 1 interface"
    

    def play_ifnot(self):
        '''
        start playng if not.
        
        GetStatus Return the status of "Media Player" as a struct of 4 ints:

        First integer: 0 = Playing, 1 = Paused, 2 = Stopped.
        Second interger: 0 = Playing linearly , 1 = Playing randomly.
        Third integer: 0 = Go to the next element once the current has finished playing , 1 = Repeat the current element
        Fourth integer: 0 = Stop playing once the last element has been played, 1 = Never give up playing 
        '''

        status=self.player.GetStatus()

        if status[0] == 0 :
            pass

        elif   status[0] == 1 :
            self.player.Pause()

        elif   status[0] == 2 :
            self.player.Play()


    def isplaying(self):
        '''
        return true if is playing.
        '''

        status=self.player.GetStatus()

        return status[0] == 0


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

                pos=self.tracklist.GetCurrentTrack()
                metadata=self.tracklist.GetMetadata(pos)
                #print metadata
                mtimelength=metadata["mtime"]
                mtimeposition=self.player.PositionGet()

                timed=datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimelength).seconds)
                toend=timed-datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimeposition).seconds)
                newpos=self.tracklist.GetCurrentTrack()

                if (pos != newpos):
                    #inconsistenza: retry
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

                for prm in range(0,pos-atlast): 
                    self.tracklist.DelTrack(0)

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

            length=self.tracklist.GetLength()

                #elimino il troppo
            if length-pos > atlast :

                for prm in range(length,pos+atlast,-1): 
                    self.tracklist.DelTrack(prm)

            return True

        except:
            return False



    def get_playlist_posauto(self,autopath,securesec=10):
        '''
        get  playlist position skipping file with path equal to  autopath.
        Try to secure that there are some time (securesec) to complete all operations in time:
        if xmms change song during operation will be a big problem
        '''

        try:

            pos=self.get_playlist_securepos(securesec=securesec)
            if pos is None:
                return pos

            pos+=1

            metadata=self.tracklist.GetMetadata(pos)

            try:
                #Fix how older versions of Audacious misreport the URI of the song.
                if metadata is not None:
                    if "URI" in metadata and "location" not in metadata:
                        metadata["location"] = metadata["URI"]

                file=metadata["location"]

            except:
                return pos

            filepath=os.path.dirname(file)

            #print "file://"+autopath
            #print os.path.commonprefix ((filepath,"file://"+autopath))

            # ora controllo se ci sono gia dei file accodati nella playlist da autoradio
            # l'unica possibilita di saperlo e verificare il path del file
            while ( os.path.commonprefix ((filepath,"file://"+autopath)) == "file://"+autopath ):
                pos+=1

                metadata=self.tracklist.GetMetadata(pos)
                try:

                    #Fix how older versions of Audacious misreport the URI of the song.
                    if metadata is not None:
                        if "URI" in metadata and "location" not in metadata:
                            metadata["location"] = metadata["URI"]

                    file=metadata["location"]
                except:
                    return pos

                filepath=os.path.dirname(file)

            # here I have found the first file added by autoradio
            return pos

        except :
            return None


    def get_playlist_len(self):
        "get playlist lenght"
        
        return self.tracklist.GetLength()



    def get_playlist_pos(self):
        "get current position"
        
        return self.tracklist.GetCurrentTrack()



    def get_metadata(self,pos):
        "get metadata for position"

        metadata=self.tracklist.GetMetadata(pos)
    
        try:
            file=metadata["location"]
        except:
            file=None
        try:
            title=metadata["title"]
            if title=="":
                title=None
        except:
            title=None

        try:
            artist=metadata["artist"]
            if artist=="":
                artist=None
        except:
            artist=None

        try:
            mtimelength=metadata["mtime"]
        except:
            mtimelength=0
        try:
            mtimeposition=self.player.PositionGet()
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

        if self.mediaplayer == "audacious":

            self.org.PlaylistInsUrlString(media,pos)
            return None
        else:
            logging.error("playlist_add_atpos: mpris interface cannot add media where I want for player "+self.mediaplayer )
            raise Exception
            

def main():

    mp=mediaplayer(player="audacious")
    mp.play_ifnot()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
