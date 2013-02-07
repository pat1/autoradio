class Playback_Rate(float):
    '''
    A playback rate
    
    This is a multiplier,
    so a value of 0.5 indicates that playback is happening at half speed,
    while 1.5 means that 1.5 seconds of "track time" is consumed every second.
    '''
    def __init__(self, rate=1.0):
        self._rate = rate
        super(Playback_Rate, self).__init__(rate)
        
    @property
    def rate(self):
        return self._rate

    
if __name__ == "__main__":
    pr = Playback_Rate(12)
    print pr == '12'