'''
Created on Nov 5, 2011

@author: hugosenari
'''
from __future__ import print_function
class Time_In_Us(int):
    '''Time in microseconds.'''
    
    def __init__(self, time=0, *args, **kw):
        '''constructor'''
        super(Time_In_Us, self).__init__(time, *args, **kw)
        self._time = time
        
    @property
    def time(self):
        '''get time value'''
        return self._time

if __name__ == "__main__":
    print(Time_In_Us(10))