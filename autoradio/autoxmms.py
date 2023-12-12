#!/usr/bin/env python
# GPL. (C) 2007-2009 Paolo Patruno.

import xmms
import time
import datetime
import os

def play_ifnot(session=0):
    '''
    start playng if not.
    '''
    # I check if xmms is playng .... otherside I try to play
    # if xmms is in pause any check is impossible 
    try:
        ok=xmms.control.is_playing(session)

        if (not ok):
            ok = xmms.control.play(session)

    except:
        return False



def get_playlist_securepos(session=0,securesec=10):
    '''
    Try to secure that there are some time (securesec) to complete all operations in time:
    if xmms change song during operation will be a big problem
    '''
    try:
 
        play_ifnot(session=session)   #force to play

        mintimed=datetime.timedelta(seconds=securesec)
        toend=datetime.timedelta(seconds=0)
        volte=0

        while ( toend < mintimed ):
            # take the current position
            pos=xmms.control.get_playlist_pos(session)
            timed=datetime.timedelta(seconds=datetime.timedelta(milliseconds=xmms.control.get_playlist_time(pos, session)).seconds)
            toend=timed-datetime.timedelta(seconds=datetime.timedelta(milliseconds=xmms.control.get_output_time(session)).seconds)
            newpos=xmms.control.get_playlist_pos(session)
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


def playlist_clear_up(atlast=10,session=0):
    '''
    clear playlist starting from current position up.
    "atlast" numer of song are retained
    '''
    try:
        play_ifnot(session=session)   #force to play

       # take the current position (if error set pos=0)
        pos=get_playlist_securepos(session)
        if pos is None:
            return False

            # delete the old ones
        if pos > atlast :

            for prm in range(0,pos-atlast): 
                xmms.control.playlist_delete(0,session)

        return True

    except:
        return False



def playlist_clear_down(atlast=500,session=0):
    '''
    clear playlist starting from current position + atlast doen.
    "atlast" numer of song are retained for future play
    '''
    try:
        play_ifnot(session=session)   #force to play

       # take the current position (if error set pos=0)
        pos=get_playlist_securepos(session)
        if pos is None:
            return False

        length=xmms.get_playlist_length(session)

            #elimino il troppo
        if length-pos > atlast :

            for prm in range(length,pos+atlast,-1): 
                xmms.control.playlist_delete(prm,session)

        return True

    except:
        return False



def get_playlist_posauto(autopath,session=0,securesec=10):
    '''
    get  playlist position skipping file with path equal to  autopath.
    Try to secure that there are some time (securesec) to complete all operations in time:
    if xmms change song during operation will be a big problem
    '''
    try:
 
        pos=get_playlist_securepos(session=session,securesec=securesec)
        if pos is None:
            return pos

        pos+=1
        file=xmms.control.get_playlist_file(pos, session)
        if file is  None :
            return pos
        filepath=os.path.dirname(file)

        # ora controllo se ci sono gia dei file accodati nella playlist da autoradio
        # l'unica possibilita di saperlo e verificare il path del file
        while ( os.path.commonprefix ((filepath,autopath)) == autopath ):
            pos+=1

            file=xmms.control.get_playlist_file(pos, session)
            if file is None :
                return pos
            filepath=os.path.dirname(file)

        # here I have found the first file added by autoradio
        return pos

    except :
        return None



#xmms.control.playlist_clear_up=playlist_clear_up
#xmms.control.get_playlist_posauto=get_playlist_posauto
#xmms.control.play_ifnot=play_ifnot

