'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/2.2/Playlists_Interface.html#Struct:Playlist
'''

from dbus import Struct


class Playlist(Struct):
    '''
    A data structure describing a playlist.
    
    * Id - o (Playlist_Id)
        A unique identifier for the playlist.
        
        This should remain the same if the playlist is renamed.
    * Name - s
        The name of the playlist, typically given by the user.
    * Icon - s (Uri)
        The URI of an (optional) icon.
        
    '''
    def __init__(self, playlist):
        Struct.__init__(
           self,
           iter(playlist),
           signature=playlist.signature,
           variant_level=playlist.variant_level
        )
    
    @property
    def Id(self):
        return self[0]
    
    @property
    def Name(self):
        return self[1]
    
    @property
    def Icon(self):
        return self[2]


class Maybe_Playlist(Struct):
    '''
    * Valid - b
        Whether this structure refers to a valid playlist.
    * Playlist - (oss) (Playlist)
        The playlist, providing Valid is true, otherwise undefined.
        
    When constructing this type, it should be noted that the playlist ID must 
    be a valid object path, or D-Bus implementations may reject it. This is
    true even when Valid is false. It is suggested that '/' is used as the
    playlist ID in this case.
    '''
    
    def __init__(self, maybe_playlist=None):
        Struct.__init__(
           self,
           (maybe_playlist[0], maybe_playlist[1]),
           signature=maybe_playlist.signature,
           variant_level=maybe_playlist.variant_level
        )

    @property
    def Valid(self):
        return self[0]
    
    @property
    def Playlist(self):
        return Playlist(self[1])
    
    def __nonzero__(self):
        return bool(self.Valid)
    
    def __bool__(self):
        return self.__nonzero__()


if __name__ == '__main__':
    expect = Struct((1, 'My Playlist', None), signature='iss')
    p = Playlist(expect)
    assert p.Id == 1
    assert p.Name == 'My Playlist'
    assert p.Icon == None
    m_expect = Struct((False, p))
    mp = Maybe_Playlist(m_expect)
    assert not mp.Valid
    assert not mp
