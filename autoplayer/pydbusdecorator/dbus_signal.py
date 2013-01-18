'''
Created on Nov 5, 2011

@author: hugosenari
'''

from pydbusdecorator.dbus_decorator import DbusDecorator
from pydbusdecorator.dbus_interface import DbusInterface

from functools import wraps

class DbusSignal(DbusDecorator):
    '''
    Wrapps some method as attribute
    '''


    def __init__(self, meth=None, iface=None, *args, **kw):
        '''
        @param meth: function, wrapped
        '''
        super(DbusSignal, self).__init__(*args, **kw)
        self.meth = meth
        self.iface = iface
        self._obj = None
        self._handler = meth
    
    def _watch_dbus(self, obj, *args, **kw):
        '''
        set self._handler to be called when obj fire signal wrapped
        '''
        def handler(*args, **kw):
            if self.meth is not self._handler:
                DbusInterface.store_result(obj, self.meth(obj, *args, **kw))
            return self._handler(self._obj, *args, **kw)
        if self.iface:
            bus_iface = DbusInterface.iface(obj, self.iface)
            bus_iface.connect_to_signal(self.meth.__name__,
                                      handler,
                                      dbus_interface=self.iface,
                                      *args, **kw)
        else:
            bus_obj = DbusInterface.get_bus_obj(obj)
            bus_obj.connect_to_signal(self.meth.__name__,
                                      handler,
                                      dbus_interface=DbusInterface.get_bus_iface(obj),
                                      *args, **kw)
    
    def _remove_watch_dbus(self, obj):
        pass
     
    def __call__(self, __call__meth=None, *args, **kw):
        if self.meth and self._obj:
            if __call__meth:
                largs = list(args)
                largs.insert(0, __call__meth)
                args = tuple(largs)
            return self._watch_dbus(self._obj, *args, **kw)
        else:
            self.meth = __call__meth
            self._handler = __call__meth
            @wraps(self.meth)
            def dbusWrapedMethod(obj, *args, **kw):
                return self._watch_dbus(obj, *args, **kw)
            return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        self._obj = obj
        return self._handler
    
    def __set__(self, obj, handler, *args, **kw):
        self._obj = obj
        self._handler = handler
        self._watch_dbus(obj, *args, **kw)
    
    @property
    def meth(self):
        return self._meth
    
    @meth.setter
    def meth(self, value):
        self._meth = value
        if hasattr(value, "__doc__"):
            self.__doc__ = value.__doc__