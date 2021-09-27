'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Playlists_Interface.html
'''

from .decorator import DbusAttr
from .decorator import DbusInterface
from .decorator import DbusMethod
from .decorator import DbusSignal
from .interfaces import Interfaces
from .types import Playlist, Maybe_Playlist
from dbus import UInt64


class Playlists(Interfaces):
    '''
    Provides access to the media player's playlists.
    
    Since D-Bus does not provide an easy way to check for what interfaces are exported on an object, clients should attempt to get one of the properties on this interface to see if it is implemented.
    
    '''
    
    @DbusInterface(Interfaces.PLAYLISTS, Interfaces.OBJECT_PATH)
    def __init__(self):
        '''Constructor'''
        pass
    
    @DbusMethod
    def ActivatePlaylist(self, PlaylistId):
        '''
        **Parameters:**
        
        * PlaylistId - o
            The id of the playlist to activate.

        Starts playing the given playlist.
        
        Note that this must be implemented. If the media player does not allow clients to change the playlist, it should not implement this interface at all.
            
        It is up to the media player whether this completely replaces the current tracklist, or whether it is merely inserted into the tracklist and the first track starts. For example, if the media player is operating in a 'jukebox' mode, it may just append the playlist to the list of upcoming tracks, and skip to the first track in the playlist.
        '''
        pass
    
    @DbusMethod(produces=lambda playlist_list: \
                    [Playlist(playlist) for playlist in playlist_list],
                args_to_dbus=[UInt64, UInt64, str, bool])
    def GetPlaylists(self, Index, MaxCount, Order, ReverseOrder=False):
        '''
        **Parameters:**
        
        * Index - u
            The index of the first playlist to be fetched (according to the ordering).
        * MaxCount - u
            The maximum number of playlists to fetch.
        * Order - s (Playlist_Ordering)
            The ordering that should be used.
        * ReverseOrder - b
            Whether the order should be reversed.

        **Returns**
        
        * Playlists - a(oss) (Playlist_List)
            A list of (at most MaxCount) playlists.
    
        Gets a set of playlists.
        '''
        pass
    
    @DbusSignal
    def PlaylistChanged(self, Playlist):
        '''
        **Parameters**
        
        * Playlist - (oss) (Playlist)
            The playlist whose details have changed.
    
        Indicates that the name or icon for a playlist has changed.
        
        Note that, for this signal to operate correctly, the id of the playlist must not change when the name changes.
        '''
        pass
    
    @DbusAttr
    def PlaylistCount(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The number of playlists available.
        '''
        pass
    
    @DbusAttr
    def Orderings(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The avaislable orderings. At least one must be offered.
        '''
        pass
    
    @DbusAttr(produces=Maybe_Playlist)
    def ActivePlaylist(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The currently-active playlist.
        
        If there is no currently-active playlist, the structure's Valid field will be false, and the Playlist details are undefined.
        
        Note that this may not have a value even after ActivatePlaylist is called with a valid playlist id as ActivatePlaylist implementations have the option of simply inserting the contents of the playlist into the current tracklist.
        '''
        pass


if __name__ == '__main__':
    from .utils import get_players_uri, implements
    for uri in get_players_uri():
        if implements(uri, Interfaces.PLAYLISTS):
            mp2 = Playlists(dbus_interface_info={'dbus_uri': uri})
            print( mp2.ActivePlaylist )
            print( 'Active is valid playlist: ', bool(mp2.ActivePlaylist) )
            if mp2.ActivePlaylist:
                print( 'Active playlist name:', mp2.ActivePlaylist.Playlist.Name )
            from mpris2.types import Playlist_Ordering
            print( hasattr('anystring', 'eusequenaotem') )
            print( 'bla', mp2.GetPlaylists(0, 20,
                                           Playlist_Ordering.ALPHABETICAL, False) )
            break
    else:
        print('no player with playlist interface found')
