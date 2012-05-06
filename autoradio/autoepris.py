#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import dbus
import time
import datetime
import os

# ------- dbus epris player interface ---------

import dbus

class mediaplayer:


    def __init__(self,session=0):

        try:
            self.bus = dbus.SessionBus()

            # -----------------------------------------------------------
            mediaplayer_obj      = self.bus.get_object("org.mpris.epris", '/org/mpris/epris')
            current_obj      = self.bus.get_object("org.mpris.epris", '/org/mpris/epris/lists/current')

            self.player    = dbus.Interface(mediaplayer_obj, dbus_interface='org.mpris.EprisPlayer')
            self.tracklist = dbus.Interface(current_obj, dbus_interface='org.mpris.EprisTrackList')
            # -----------------------------------------------------------

        except:
            raise


    def __str__(self):
        return self.player.Identity
    

    def play_ifnot(self):
        '''
        start playing if not.
        '''
        # I check if mediaplayer is playing .... otherside I try to play

        print self.tracklist.ListTracks()
        print self.tracklist.Current

#        if (not self.player.PlaybackStatus == "Playing"):

#        self.player.Play()



    def get_playlist_securepos(self,securesec=10):
# DO NOT WORK

        '''
        Try to secure that there are some time (securesec) to complete all operations in time:
        if mediaplayer change song during operation will be a big problem
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
# DO NOT WORK
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

                for prm in xrange(0,pos-atlast): 
                    self.tracklist.DelTrack(0)

            return True

        except:
            return False



    def playlist_clear_down(self,atlast=500):
# DO NOT WORK
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

                for prm in xrange(length,pos+atlast,-1): 
                    self.tracklist.DelTrack(prm)

            return True

        except:
            return False



    def get_playlist_posauto(self,autopath,securesec=10):
# DO NOT WORK
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
                file=metadata["URI"]
            except:
                return pos

            filepath=os.path.dirname(file)

            # ora controllo se ci sono gia dei file accodati nella playlist da autoradio
            # l'unica possibilita di saperlo e verificare il path del file
            while ( os.path.commonprefix ((filepath,"file://"+autopath)) == "file://"+autopath ):
                pos+=1

                metadata=self.tracklist.GetMetadata(pos)
                try:
                    file=metadata["URI"]
                except:
                    return pos

                filepath=os.path.dirname(file)

            # here I have found the first file added by autoradio
            return pos

        except :
            return None



    def get_playlist_pos(self):
# DO NOT WORK
        "get current position"
        
        return self.tracklist.GetCurrentTrack()


def main():

    mp=mediaplayer()
    print mp
    mp.play_ifnot()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
