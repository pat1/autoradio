'''
Created on Nov 5, 2011

@author: hugosenari
'''

from pydbusdecorator.dbus_decorator import DbusDecorator
from pydbusdecorator.dbus_interface import DbusInterface

from functools import wraps


def kw_to_dbus(**kw):
    return kw

def args_to_dbus(*args):
    return args

class DbusMethod(DbusDecorator):
    '''
    Wrapps some method calling dbus method
    '''
    DbusMethodId = 0

    def __init__(self, meth=None,
                 iface=None,
                 produces=None,
                 args_to_dbus=args_to_dbus,
                 kw_to_dbus=kw_to_dbus,
                 override_none_return = True, 
                 *args, **kw):
        '''
        Wrapps some method calling dbus method
        @param meth:
            method to be wrapped
        @param produces:
            callable to convert dbus response into other type: produces(dbus_returned)
            if is not callable but iterable try convert params calling list item in same order  
        @param args_to_dbus:
            callable to convert function params into dbus typee: args_to_dbus([array of args])
            if is not callable but dict try convert params calling dicts item whith the same keyword
        @param kw_to_dbus:
            callable to convert function params (received as keywords dict) into dbus types: kw_to_dbus({dict of keywords})   
        @param override_none_return:
            Set if override response of call decorated attr (method) with value of dbus attr response
        '''
        self.uniq = DbusMethod.DbusMethodId
        DbusMethod.DbusMethodId = self.uniq + 1
        super(DbusMethod, self).__init__(*args, **kw)
        self.meth = meth
        self.iface = iface
        self.obj = None
        self.produces = produces
        self.args_to_dbus = args_to_dbus
        self.kw_to_dbus = kw_to_dbus 
        self.override_return = True
        
    def _call_dbus(self, obj, *args, **kw):
#        print self.meth.__name__, args, kw
        bus_obj = DbusInterface.get_bus_obj(obj)
        bus_interface = self.iface if self.iface else\
            DbusInterface.get_bus_iface(obj)           
        bus_meth = bus_obj.get_dbus_method(self.meth.__name__, bus_interface)
        args = self.convert_args_to_dbus_args(*args)
        kw = self.convert_kw_to_dbus_kw(**kw)
        dbus_result = bus_meth(*args, **kw)
        DbusInterface.store_result(obj, dbus_result)
        produces = self.produces
        if produces:
            return produces(dbus_result)
        meth = self.meth
        result = None
        if meth:
            result = meth(obj, *args, **kw)
        if result is None and self.override_return:
            result = dbus_result
        return result
     
    def __call__(self, _meth=None, *args, **kw):
        meth = _meth or self.meth
        if self.meth and self.obj:
            if _meth:
                largs = list(args)
                largs.insert(0, meth)
                args = tuple(largs)
            return self._call_dbus(self.obj, *args, **kw)
        else:
            self.meth = meth
            @wraps(self.meth)
            def dbusWrapedMethod(obj, *args, **kw):                
                return self._call_dbus(obj, *args, **kw)
            return dbusWrapedMethod

    def __get__(self, obj=None, *args, **kw):
        if obj is None:
            return self
        self.obj = obj
        return self.__call__
    
    def convert_args_to_dbus_args(self, *args):
        args_to_dbus = self.args_to_dbus
        if callable(args_to_dbus):
            return args_to_dbus(*args)
        
        result = []
        #iterate over args
        for i in range(len(args)):
            arg = args[i]
            if i < len(args_to_dbus):
                make = args_to_dbus[i]
                if callable(make):
                    arg = make(arg)
            result.append(arg)
        return tuple(result)
    
    def convert_kw_to_dbus_kw(self, **kw):
        kw_to_dbus = self.kw_to_dbus
        if callable(kw_to_dbus):
            return kw_to_dbus(**kw)
        
        if hasattr(self.kw_to_dbus, 'keys'):
            to_dbus_keys = kw_to_dbus.keys()
            for key in kw.keys():
                if key in to_dbus_keys:
                    kw[key] = kw_to_dbus[key](kw[key])
        return kw
    
    @property
    def meth(self):
        return self._meth
    
    @meth.setter
    def meth(self, value):
        self._meth = value
        if hasattr(value, "__doc__"):
            self.__doc__ = value.__doc__
    
    
    