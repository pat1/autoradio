PLAYING = 'Playing'
PAUSED = 'Paused'
STOPPED = 'Stopped'

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
    VALUES = (PLAYING, PAUSED, STOPPED)
    
    def __init__(self, status):
        super(Playback_Status, self).__init__()
        self._status = status
    
    @property
    def status(self):
        return self._status

Playback_Status.PLAYING = PLAYING
Playback_Status.PAUSED = PAUSED
Playback_Status.STOPPED = STOPPED
