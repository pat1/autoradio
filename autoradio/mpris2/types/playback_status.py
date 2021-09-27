'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html#Enum:Playback_Status
'''


class Playback_Status(str):
    '''
    A playback state.
    
    * Playing (Playing)
        A track is currently playing.
    * Paused (Paused)
        A track is currently paused.
    * Stopped (Stopped)
        There is no track currently playing.
        
    '''

    PLAYING = 'Playing'
    PAUSED = 'Paused'
    STOPPED = 'Stopped'
    VALUES = (PLAYING, PAUSED, STOPPED)
    
    def __init__(self, status):
        self._status = status
    
    def __int__(self):
        return Playback_Status.VALUES.index(self._status)
    
    def __str__(self):
        return self._status


if __name__ == '__main__':
    assert Playback_Status.PLAYING == 'Playing'
    assert Playback_Status.PAUSED == 'Paused'
    assert Playback_Status.STOPPED == 'Stopped'
    assert Playback_Status.STOPPED != 'Playing'
