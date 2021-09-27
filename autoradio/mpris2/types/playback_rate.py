'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html#Simple-Type:Playback_Rate
'''


class Playback_Rate(float):
    '''
    A playback rate
    
    This is a multiplier,
    so a value of 0.5 indicates that playback is happening at half speed,
    while 1.5 means that 1.5 seconds of 'track time' is consumed every second.
    '''

    def __init__(self, rate=1.0):
        self._rate = rate
    
    def __float__(self):
        return self._rate
    
    def __str__(self):
        return str(self._rate)

    
if __name__ == '__main__':
    pr = Playback_Rate(1.2)
    assert pr == 1.2
