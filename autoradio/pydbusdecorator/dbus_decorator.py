'''
Created on Nov 5, 2011

@author: hugosenari
'''

from builtins import object
import dbus

class DbusDecorator(object):
    '''
    Decorator root class
    '''
    dbus_lib = dbus

    def __init__(self, *args, **kw):
        '''
        Constructor
        '''
        pass