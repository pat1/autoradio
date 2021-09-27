'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html#Enum:Loop_Status
'''


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
    NONE = 'None'
    TRACK = 'Track'
    PLAYLIST = 'Playlist'
    VALUES = (NONE, TRACK, PLAYLIST)
    def __init__(self, status):
        self._status = status
    
    def __int__(self):
        return Loop_Status.VALUES.index(self._status)
    
    def __str__(self):
        return self._status


if  __name__ == '__main__':
    assert Loop_Status.PLAYLIST != 'None'
    assert Loop_Status.PLAYLIST == 'Playlist'
    assert Loop_Status.TRACK == 'Track'
    assert Loop_Status.NONE == 'None'
