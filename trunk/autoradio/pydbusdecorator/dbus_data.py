#'''
#Created on Nov 5, 2011
#
#@author: hugosenari
#'''
#from functools import wraps
#class DbusData(object):
#    '''
#    Wrapps class as data
#    '''
#
#    def __init__(self, *args, **kw):
#        '''
#        Constructor
#        '''
#
#    def __call__(self, meth, *args, **kw):
#        '''
#            wrap function
#        '''
#        @wraps(meth)
#        def dbusWrapedData(*args, **kw):
#            return meth(*args, **kw)
#        return dbusWrapedData
#    
#    def __get__(self, obj, objtype=None):
#        return obj if obj else self 