'''
This is not part of specification

Helper class to make it work as python lib
'''

from .base import Decorator, ATTR_KEY


def kw_to_dbus(**kw):
    return kw

def args_to_dbus(*args):
    return args


class DbusMethod(Decorator):

    def __init__(self, meth=None,
                 iface=None,
                 produces=lambda resp: resp,
                 args_to_dbus=args_to_dbus,
                 kw_to_dbus=kw_to_dbus,
                 std_args=(),
                 std_kwds={}):
        self.meth = meth
        self.handler = None
        self.produces = produces
        self.iface = iface
        self.args_to_dbus = args_to_dbus
        self.kw_to_dbus = kw_to_dbus
        self.std_args = std_args
        self.std_kwds = std_kwds
        self.obj = None
        self._update_me(meth)

    def __call__(self, meth=None):
        self.meth = meth
        self._update_me(meth)
        return self

    def __get__(self, obj=None, cls=None):
        if obj is None:
            return self
        self.obj = obj
        return self._call_dbus
    
    def _call_dbus(self, *args, **kwds):
        _dbus = getattr(self.obj, ATTR_KEY)
        if self.iface:
            iface = self.iface
        else:
            iface = _dbus.iface
        bus_obj = _dbus.object
        bus_meth = bus_obj.get_dbus_method(self.meth.__name__, iface)
        _args = self.merge_args(args, self.std_args)
        args = self.convert_args_to_dbus_args(*_args)
        _kwds = self.std_kwds.copy()
        _kwds.update(kwds)
        kwds = self.convert_kw_to_dbus_kw(**_kwds)
        result = bus_meth(*args, **kwds)
        return self.produces(result)
    
    @classmethod
    def merge_args(cls, args, std_args):
        _len = len(std_args) - len(args)
        return args + std_args[-_len:] if _len > 0 else args
    
    @classmethod
    def merge_kwds(cls, kwds, std_kwds):
        _kwds = std_kwds.copy()
        _kwds.update(kwds)
        return _kwds
    
    def convert_args_to_dbus_args(self, *args):
        args_to_dbus = self.args_to_dbus
        if callable(args_to_dbus):
            return args_to_dbus(*args)
        
        #iterate over args
        result = []
        for arg in args:
            i = args.index(arg)
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
            for key, val in kw.items():
                make = kw_to_dbus.get(key, lambda v: v)
                kw[key] = make(val)
        return kw


if __name__ == '__main__':
    # examples
    from .interface import DbusInterface
    @DbusInterface('org.freedesktop.DBus', '/')
    class Example(object):
        
        @DbusMethod
        def GetId(self):
            pass
        
        @DbusMethod
        def GetNameOwner(self, name):
            pass

    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.freedesktop.DBus'})
    assert d.GetId()
    assert d.GetNameOwner('org.freedesktop.DBus') == 'org.freedesktop.DBus'
