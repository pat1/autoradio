'''
This is not part of specification

Helper class to make it work as python lib
'''

import dbus
from functools import wraps
from .base import Decorator, ARG_KEY, I_PROP, ATTR_KEY


class _DbusInfoProperty(object):
    def __init__(self, iface=None, path=None, 
                 uri=None, dbus_object=None, session=None, wrapped=None):
        self.iface = iface
        self.path = path
        self.uri = uri
        self.object = dbus_object
        self.session = session
        self.wrapped = wrapped
        self.interface = None
        self.properties = None
        
        if not self.object:
            bus = self.session = self.session or dbus.SessionBus()
            self.object = bus.get_object(self.uri, self.path)
        if not self.interface:
            self.interface = dbus.Interface(self.object,
                                            dbus_interface=self.iface)
        if not self.properties:
            self.properties = dbus.Interface(self.object, I_PROP)

    def reconnect(self, session=None):
        '''
        Required if you need update session/proxy object/interfaces
        '''
        
        session = session or self.session
        if session == self.session:
            self.session.close()
            session = self.session = dbus.SessionBus()
        self.object = session.get_object(self.uri, self.path)
        self.interface = dbus.Interface(self.object, dbus_interface=self.iface)
        self.properties = dbus.Interface(self.object, I_PROP)


class DbusInterface(Decorator):

    def __init__(self, iface=None, path=None, 
                 uri=None, dbus_object=None, session=None):
        self.iface = iface
        self.path = path
        self.uri = uri
        self.object = dbus_object
        self.session = session
        self.wrapped = None

    def __call__(self, meth):
        ''' Called when any decorated class is loaded'''
        self.wrapped = meth
        self._update_me(meth)
        
        @wraps(meth)
        def dbusWrapedInterface(*args, **kw):
            _args = kw.get(ARG_KEY, {})
            info_property = _DbusInfoProperty(
                iface=_args.get('dbus_iface', self.iface),
                path=_args.get('dbus_path', self.path),
                uri=_args.get('dbus_uri', self.uri),
                dbus_object =_args.get('dbus_object', self.object),
                session =_args.get('dbus_session', self.session),
                wrapped=self.wrapped
            )
            if ARG_KEY in kw: 
                del kw[ARG_KEY]
                
            return self.dbusWrapedInterface(info_property, *args, **kw)
        
        return dbusWrapedInterface
    
    def dbusWrapedInterface(self, info_property, *args, **kw):
        ''' Called when some decoreted class was called
        Inject attrs from decorator at new object then return object
        
        @param *args: list of args to call constructor
        @param **kw: dict of keywords, can redefine class default parameters
        @return: instance of decoreted class, with new attributes
        @see: mpris2.mediaplayer2 to see some examples
        '''
        #call decorated class constructor
        new_obj = self.wrapped(*args, **kw)
        if new_obj:
            setattr(new_obj, ATTR_KEY, info_property)
        elif len(args) > 0:
            setattr(args[0], ATTR_KEY, info_property)
        
        return new_obj


if __name__ == '__main__':
    # examples
    @DbusInterface('org.freedesktop.DBus', '/')
    class Example(object):
        pass


    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.freedesktop.DBus'})
    assert d._dbus_interface_info.iface == 'org.freedesktop.DBus'
    assert d._dbus_interface_info.path == '/'
    assert d._dbus_interface_info.uri == 'org.freedesktop.DBus'

    class ExempleToo(object):
        @DbusInterface('org.freedesktop.DBus', '/')
        def __init__(self):
            pass

    dd = ExempleToo(
        dbus_interface_info={
            'dbus_uri': 'org.freedesktop.DBus'})
        
    assert dd._dbus_interface_info.iface == 'org.freedesktop.DBus'
    assert dd._dbus_interface_info.path == '/'
    assert dd._dbus_interface_info.uri == 'org.freedesktop.DBus'
