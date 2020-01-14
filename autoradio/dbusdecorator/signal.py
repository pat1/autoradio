from .base import Decorator, ATTR_KEY


class DbusSignal(Decorator):
    '''
    https://docs.python.org/2/howto/descriptor.html#properties
    '''

    def __init__(self, meth=None, iface=None):
        self.attr = meth
        self.handler = None
        self.iface = iface
        self._update_me(meth)

    def __call__(self, meth):
        self.attr = meth
        self._update_me(meth)
        return self
    
    def __get__(self, obj, objtype=None):
        if obj:
            return self.handler

        #static call
        return self 

    def __set__(self, obj, value):
        if obj:
            _dbus = getattr(obj, ATTR_KEY)
            interface = _dbus.interface
            def handle(*args, **kwds):
                h = self.handler
                h and h(*args, **kwds)

            if not self.handler:
                interface.connect_to_signal(self.attr.__name__, handle,
                                    dbus_interface=self.iface)
            self.handler = value
        else: #static call
            self.attr = value

    def __delete__(self, obj):
        self.handler = None


if __name__ == '__main__':
    from .interface import DbusInterface
    from .utils import get_mainloop
    mainloop = get_mainloop()
    print('mainloop', mainloop)
    
    @DbusInterface('org.mpris.MediaPlayer2.player',
                   '/org/mpris/MediaPlayer2')
    class Example(object):
        
        @DbusSignal
        def Seeked(self):
            pass


    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.mpris.MediaPlayer2.gmusicbrowser'})
    
    def handler(self, *args):
        print(args)
    
    d.Seeked = handler
    mainloop and mainloop.run()
