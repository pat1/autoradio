'''
This is not part of specification

Helper class to make it work as python lib
'''

from .base import Decorator, ATTR_KEY


class DbusAttr(Decorator):
    '''
    https://docs.python.org/2/howto/descriptor.html#properties
    '''

    def __init__(self, meth=None, produces=lambda resp: resp):
        self.attr = meth
        self.produces = produces
        self._update_me(meth)

    def __call__(self, meth):
        self.attr = meth
        self._update_me(meth)
        return self
    
    def __get__(self, obj, objtype=None):
        #static call
        if not obj:
            return self

        _dbus = getattr(obj, ATTR_KEY)
        props = _dbus.properties
        iface = _dbus.iface
        result = props.Get(iface, self.attr.__name__)
        produces = self.produces
        return produces(result)

    def __set__(self, obj, value):
        if obj:
            _dbus = getattr(obj, ATTR_KEY)
            props = _dbus.properties
            iface = _dbus.iface
            props.Set(iface, self.attr.__name__, value)
        else: #static call
            self.attr = value

    def __delete__(self, obj):
        raise AttributeError('can not delete attribute')


if __name__ == '__main__':
    # examples
    from .interface import DbusInterface

    @DbusInterface('org.mpris.MediaPlayer2',
                   '/org/mpris/MediaPlayer2')
    class Example(object):
        @DbusAttr
        def Identity(self):
            pass

    d = Example(
        dbus_interface_info={
            'dbus_uri': 'org.mpris.MediaPlayer2.vlc'})

    assert d.Identity == 'VLC media player'
