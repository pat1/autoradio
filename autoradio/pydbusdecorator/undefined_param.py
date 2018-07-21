'''
Created on Nov 5, 2011

@author: hugosenari
'''
from __future__ import print_function

from builtins import object
class Undefined(object):
    '''Undefined'''
    def __nonzero__(self=None):
        return False
    
    def __repr__(self=None):
        return "Undefined"

class UndefinedParam(Undefined):
    ''' UndefinedParam '''
    
    def __cmp__(self, other):
        return isinstance(other, Undefined)
    
UNDEFINED = Undefined()
UNDEFINED_PARAM = UndefinedParam()

if __name__ == "__main__":
    print("True" if bool(UNDEFINED_PARAM) else "False")