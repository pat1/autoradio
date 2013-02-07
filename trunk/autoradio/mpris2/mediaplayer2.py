"""
This is python mprisV2.1 documentation

http://www.mpris.org/2.1/spec/Root_Node.html
"""


from autoradio.pydbusdecorator.dbus_attr import DbusAttr
from autoradio.pydbusdecorator.dbus_interface import DbusInterface
from autoradio.pydbusdecorator.dbus_method import DbusMethod
from autoradio.pydbusdecorator.dbus_signal import DbusSignal

from interfaces import Interfaces


class MediaPlayer2(Interfaces):
    '''
    Interface for MediaPlayer2 (org.mpris.MediaPlayer2)
    '''
    PROPERTIES_CAN_QUIT = 'CanQuit'
    PROPERTIES_CAN_RAISE = 'CanRaise'
    PROPERTIES_HAS_TRACK_LIST = 'HasTrackList'
    PROPERTIES_IDENTITY = 'Identity'
    PROPERTIES_DESKTOP_ENTRY = 'DesktopEntry'
    PROPERTIES_SUPPORTED_URI_SCHEMES = 'SupportedUriSchemes'
    PROPERTIES_SUPPORTED_MINE_TYPES = 'SupportedMimeTypes'
    SIGNALS_PROPERTIES_CHANGED = 'PropertiesChanged'
    
    @DbusInterface(Interfaces.MEDIA_PLAYER, Interfaces.OBJECT_PATH)
    def __init__(self):
        '''Constructor'''
        pass
    
    @DbusMethod
    def Raise(self):
        """
        Brings the media player's user interface to the front using any appropriate mechanism available.
        
        The media player may be unable to control how its user interface is displayed, or it may not have a graphical user interface at all. In this case, the CanRaise property is false and this method does nothing.
        """
        return None
    
    @DbusMethod
    def Quit(self):
        """
        Causes the media player to stop running.
        
        The media player may refuse to allow clients to shut it down. In this case, the CanQuit property is false and this method does nothing.
        
        ..note::
            Media players which can be D-Bus activated, or for which there is no sensibly easy way to terminate a running instance (via the main interface or a notification area icon for example) should allow clients to use this method. Otherwise, it should not be needed.
        
        If the media player does not have a UI, this should be implemented
        """
        pass
    
    @DbusAttr
    def CanQuit(self):
        """
        **Returns**
        
        Read only
            Inject attrs from decorator at new object then return obje
        
        When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        If false, calling Quit will have no effect, and may raise a NotSupported error. If true, calling Quit will cause the media application to attempt to quit (although it may still be prevented from quitting by the user, for example).
        """
        pass
    
    @DbusAttr
    def CanRaise(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        If false, calling Raise will have no effect, and may raise a NotSupported error. If true, calling Raise will cause the media application to attempt to bring its user interface to the front, although it may be prevented from doing so (by the window manager, for example).
        """
        pass
    
    @DbusAttr
    def HasTrackList(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
            
        Indicates whether the /org/mpris/MediaPlayer2 object implements the org.mpris.MediaPlayer2.TrackList interface.
        """
        pass
    
    @DbusAttr
    def Identity(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        A friendly name to identify the media player to users.

        This should usually match the name found in .desktop files

        (eg: "VLC media player").
        """
        pass
    
    @DbusAttr
    def DesktopEntry(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The basename of an installed .desktop file which complies with the Desktop entry specification, with the ".desktop" extension stripped.

        Example: The desktop entry file is "/usr/share/applications/vlc.desktop", and this property contains "vlc"

        This property is optional. Clients should handle its absence gracefully
        """
        pass
    
    @DbusAttr
    def SupportedUriSchemes(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The URI schemes supported by the media player.

        This can be viewed as protocols supported by the player in almost all cases. Almost every media player will include support for the "file" scheme. Other common schemes are "http" and "rtsp".

        Note that URI schemes should be lower-case.

        .. note::
            This is important for clients to know when using the editing capabilities of the Playlist interface, for example.
        """
        pass
    
    @DbusAttr
    def SupportedMimeTypes(self):
        """
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The mime-types supported by the media player.

        Mime-types should be in the standard format (eg: audio/mpeg or application/ogg).

        .. note::
            This is important for clients to know when using the editing capabilities of the Playlist interface, for example.
        """
        pass
    
    @DbusSignal(iface=Interfaces.PROPERTIES)
    def PropertiesChanged(self, *args, **kw):
        """
        **Parameters:**
        
        * args - list
            unnamed parameters passed by dbus signal
        * kw - dict
            named parameters passed by dbus signal
            
        Every time that some property change, signal will be called
        """
        pass

if __name__ == '__main__':
    from mpris2.utils import SomePlayers
    uri = Interfaces.MEDIA_PLAYER + '.' + SomePlayers.GMUSICBROWSER
    mp2 = MediaPlayer2(dbus_interface_info={'dbus_uri': uri})
    print mp2.SupportedUriSchemes
#    
#    
#    from dbus.mainloop.glib import DBusGMainLoop
#    DBusGMainLoop(set_as_default=True)
#    import gobject
#    
#    def another_handler(self, *args, **kw): 
#        print args, '\n', kw
#
#    mloop = gobject.MainLoop()
#    mp2.PropertiesChanged = another_handler
#    mloop.run()
