'''
Audio Volume
'''
from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div
class Volume(float):
    '''
    Audio volume level
    
    * 0.0 means mute.
    * 1.0 is a sensible maximum volume level (ex: 0dB).
    
    Note that the volume may be higher than 1.0, although generally clients should not attempt to set it above 1.0.
    '''

    MIN = 0.0
    MAX = 1.0
    RANGE = set([old_div(n,10.0) for n in range(11)])
    
    def __init__(self, volume=1.0, *args, **kw):
        super(Volume, self).__init__(volume, *args, **kw)
        self._volume = volume
        
    @property
    def volume(self):
        '''Get volume atrribute'''
        return self._volume
    
if __name__ == "__main__":
    print(Volume(1))