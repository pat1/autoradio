'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html#Simple-Type:Volume
'''


class Volume(float):
    '''
    Audio volume level
    
    * 0.0 means mute.
    * 1.0 is a sensible maximum volume level (ex: 0dB).
    
    Note that the volume may be higher than 1.0, although generally clients should not attempt to set it above 1.0.
    '''

    MIN = 0.0
    MAX = 1.0
    RANGE = set([n/10.0 for n in range(11)])
    
    def __init__(self, volume=1.0):
        assert volume <= 1
        self._volume = float(volume)
    
    def __float__(self):
        return self._volume
    
    def __str__(self):
        return str(self._volume)


if __name__ == '__main__':
    assert Volume(1) == 1
    assert Volume(0.1) == 0.1
    assert Volume(1) == 1.0
    assert Volume(1.0) == 1
    assert Volume(0.1) != 1.2
    
