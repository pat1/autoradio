'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Media_Player.html
'''

from .decorator import DbusAttr
from .decorator import DbusInterface
from .decorator import DbusMethod
from .decorator import DbusSignal
from .interfaces import Interfaces


class MediaPlayer2(Interfaces):
    '''
    Interface for MediaPlayer2 (org.mpris.MediaPlayer2)
    '''
    PROPERTIES_CAN_QUIT = 'CanQuit'
    PROPERTIES_CAN_RAISE = 'Identity'
    PROPERTIES_HAS_TRACK_LIST = 'HasTrackList'
    PROPERTIES_IDENTITY = 'Identity'
    PROPERTIES_DESKTOP_ENTRY = 'DesktopEntry'
    PROPERTIES_SUPPORTED_URI_SCHEMES = 'SupportedUriSchemes'
    PROPERTIES_SUPPORTED_MINE_TYPES = 'SupportedMimeTypes'
    SIGNALS_PROPERTIES_CHANGED = 'PropertiesChanged'
    
    @DbusInterface(Interfaces.MEDIA_PLAYER, Interfaces.OBJECT_PATH)
    def __init__(self):
        '''Constructor'''
    
    @DbusMethod
    def Raise(self):
        '''
        Brings the media player's user interface to the front using any appropriate mechanism available.
        
        The media player may be unable to control how its user interface is displayed, or it may not have a graphical user interface at all. In this case, the Identity property is false and this method does nothing.
        '''
    
    @DbusMethod
    def Quit(self):
        '''
        Causes the media player to stop running.
        
        The media player may refuse to allow clients to shut it down. In this case, the CanQuit property is false and this method does nothing.
        
        ..note::
            Media players which can be D-Bus activated, or for which there is no sensibly easy way to terminate a running instance (via the main interface or a notification area icon for example) should allow clients to use this method. Otherwise, it should not be needed.
        
        If the media player does not have a UI, this should be implemented
        '''
    
    @DbusAttr
    def CanQuit(self):
        '''
        **Returns**
        
        Read only
            Inject attrs from decorator at new object then return obje
        
        When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        If false, calling Quit will have no effect, and may raise a NotSupported error. If true, calling Quit will cause the media application to attempt to quit (although it may still be prevented from quitting by the user, for example).
        '''

    @DbusAttr
    def Fullscreen(self):
        '''
        **Returns**
        
        Read Write
            Whether the media player is occupying the fullscreen.
            
        This property is optional. Clients should handle its absence gracefully.
        
        When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        This is typically used for videos. A value of true indicates that the media player is taking up the full screen.
        
        Media center software may well have this value fixed to true
        
        If CanSetFullscreen is true, clients may set this property to true to tell the media player to enter fullscreen mode, or to false to return to windowed mode.
        
        If CanSetFullscreen is false, then attempting to set this property should have no effect, and may raise an error. However, even if it is true, the media player may still be unable to fulfil the request, in which case attempting to set this property will have no effect (but should not raise an error).
        
        Added in 2.2.
        '''

    @DbusAttr    
    def CanSetFullscreen(self):
        '''
        **Returns**
        
        Read only
            If false, attempting to set Fullscreen will have no effect, and may raise an error. If true, attempting to set Fullscreen will not raise an error, and (if it is different from the current value) will cause the media player to attempt to enter or exit fullscreen mode.

        This property is optional. Clients should handle its absence gracefully.

        When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Added in 2.2.
        
        ..note::
            Note that the media player may be unable to fulfil the request. In this case, the value will not change. If the media player knows in advance that it will not be able to fulfil the request, however, this property should be false.
        '''

    @DbusAttr
    def CanRaise(self):
        '''
        **Returns**
        
        Read only
            If false, calling Raise will have no effect, and may raise a NotSupported error. If true, calling Raise will cause the media application to attempt to bring its user interface to the front, although it may be prevented from doing so (by the window manager, for example).

        When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        '''
    
    @DbusAttr
    def HasTrackList(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
            
        Indicates whether the /org/mpris/MediaPlayer2 object implements the org.mpris.MediaPlayer2.TrackList interface.
        '''
    
    @DbusAttr
    def DesktopEntry(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The basename of an installed .desktop file which complies with the Desktop entry specification, with the '.desktop' extension stripped.

        Example: The desktop entry file is '/usr/share/applications/vlc.desktop', and this property contains 'vlc'

        This property is optional. Clients should handle its absence gracefully
        '''
    
    @DbusAttr
    def Identity(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        If false, calling Raise will have no effect, and may raise a NotSupported error. If true, calling Raise will cause the media application to attempt to bring its user interface to the front, although it may be prevented from doing so (by the window manager, for example).
        '''
    
    @DbusAttr
    def SupportedUriSchemes(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The URI schemes supported by the media player.

        This can be viewed as protocols supported by the player in almost all cases. Almost every media player will include support for the 'file' scheme. Other common schemes are 'http' and 'rtsp'.

        Note that URI schemes should be lower-case.

        .. note::
            This is important for clients to know when using the editing capabilities of the Playlist interface, for example.
        '''
    
    @DbusAttr
    def SupportedMimeTypes(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The mime-types supported by the media player.

        Mime-types should be in the standard format (eg: audio/mpeg or application/ogg).

        .. note::
            This is important for clients to know when using the editing capabilities of the Playlist interface, for example.
        '''
    
    @DbusSignal(iface=Interfaces.PROPERTIES)
    def PropertiesChanged(self, *args, **kw):
        '''
        **Parameters:**
        
        * args - list
            unnamed parameters passed by dbus signal
        * kw - dict
            named parameters passed by dbus signal
            
        Every time that some property change, signal will be called
        '''


if __name__ == '__main__':
    from .utils import get_players_uri, implements, get_mainloop
    mainloop = get_mainloop()
    # to set signal handler
    # set_default_mainloop
    # need to be called before instance creation
    
    for uri in get_players_uri():
        if implements(uri, Interfaces.PLAYER):
            
            mp2 = MediaPlayer2(dbus_interface_info={
                'dbus_uri': uri
            })
            print(mp2.SupportedUriSchemes)
            
            def another_handler(self, *args, **kw): 
                print(args, '\n', kw)
        
            if mainloop:
                mp2.PropertiesChanged = another_handler
                mainloop.run()
            break
    else:
        print('no player with mediaplayer2 interface found')