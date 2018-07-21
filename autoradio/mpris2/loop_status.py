from __future__ import print_function
NONE = 'None'
TRACK = 'Track'
PLAYLIST = 'Playlist'

class Loop_Status(str):
    '''
    
    A repeat / loop status
    
    * None (None)
        The playback will stop when there are no more tracks to play
    * Track (Track)
        The current track will start again from the begining once it has finished playing
    * Playlist (Playlist)
        The playback loops through a list of tracks
    '''
    VALUES = (NONE, TRACK, PLAYLIST)
    def __init__(self, status, *args, **kw):
        super(Loop_Status, self).__init__(status, *args, **kw)
        self._status = status
    
    def __int__(self, *args, **kwargs):
        return int(Loop_Status.VALUES.index(self._status), *args, **kwargs)
    
Loop_Status.NONE = Loop_Status(NONE)
Loop_Status.TRACK = Loop_Status(TRACK)
Loop_Status.PLAYLIST = Loop_Status(PLAYLIST)

if  __name__ == "__main__":
    print(Loop_Status.PLAYLIST)
    print(type(Loop_Status.PLAYLIST))
    print(Loop_Status.PLAYLIST == NONE) 
    print(Loop_Status.PLAYLIST == PLAYLIST)