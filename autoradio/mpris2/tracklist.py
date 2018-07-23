"""
This is python mprisV2.1 documentation

http://www.mpris.org/2.1/spec/TrackList_Node.html
"""
from __future__ import print_function
from __future__ import absolute_import
from autoradio.dbusdecorator import DbusAttr
from autoradio.dbusdecorator import DbusInterface
from autoradio.dbusdecorator import DbusMethod
from autoradio.dbusdecorator import DbusSignal
from .interfaces import Interfaces
from .types import Metadata_Map


class TrackList(Interfaces):
    '''
    Interface for TrackList (org.mpris.MediaPlayer2.TrackList)

    Provides access to a short list of tracks which were recently played or will be played shortly. This is intended to provide context to the currently-playing track, rather than giving complete access to the media player's playlist.

    Example use cases are the list of tracks from the same album as the currently playing song or the Rhythmbox play queue.

    Each track in the tracklist has a unique identifier. The intention is that this uniquely identifies the track within the scope of the tracklist. In particular, if a media item (a particular music file, say) occurs twice in the track list, each occurrence should have a different identifier. If a track is removed from the middle of the playlist, it should not affect the track ids of any other tracks in the tracklist.

    As a result, the traditional track identifiers of URLs and position in the playlist cannot be used. Any scheme which satisfies the uniqueness requirements is valid, as clients should not make any assumptions about the value of the track id beyond the fact that it is a unique identifier.

    Note that the (memory and processing) burden of implementing the TrackList interface and maintaining unique track ids for the playlist can be mitigated by only exposing a subset of the playlist when it is very long (the 20 or so tracks around the currently playing track, for example). This is a recommended practice as the tracklist interface is not designed to enable browsing through a large list of tracks, but rather to provide clients with context about the currently playing track.
    '''
    PROPERTIES_TACKS = 'Tracks'
    PROPERTIES_CAN_EDIT_TRACKS = 'CanEditTracks'
    SIGNALS_TRACK_LIST_REPLACED = 'TrackListReplaced'
    SIGNALS_TRACK_ADDED = 'TrackAdded'
    SIGNALS_TRACK_REMOVED = 'TrackRemoved'
    SIGNALS_TRACK_METADATA_CHANGED = 'TrackMetadataChanged'
    SIGNALS_PROPERTIES_CHANGED = 'PropertiesChanged'


    @DbusInterface(Interfaces.TRACK_LIST, Interfaces.OBJECT_PATH)
    def __init__(self):
        '''Constructor'''
        pass
    
    @DbusMethod(produces=lambda map_list:\
                [Metadata_Map(metadata_map) for metadata_map in map_list])
    def GetTracksMetadata(self, TrackIds):
        '''
        **Parameters:**
        
        * TrackIds - ao (Track_Id_List)
            The list of track ids for which metadata is requested.
            
        **Returns**
        
        * Metadata - aa{sv} (Metadata_Map_List)
            Metadata of the set of tracks given as input.
            
        See the type documentation for more details.
        
        Gets all the metadata available for a set of tracks.
        
        Each set of metadata must have a "mpris:trackid" entry at the very least, which contains a string that uniquely identifies this track within the scope of the tracklist.
        '''
        pass
    
    @DbusMethod
    def AddTrack(self, Uri, AfterTrack='', SetAsCurrent=False):
        '''

        **Parameters:**
        
        * Uri - s (Uri)
            The uri of the item to add. Its uri scheme should be an element of the org.mpris.MediaPlayer2.SupportedUriSchemes property and the mime-type should match one of the elements of the org.mpris.MediaPlayer2.SupportedMimeTypes
        * AfterTrack - o (Track_Id)
            The identifier of the track after which the new item should be inserted. An empty string means at the begining of the track list.
        * SetAsCurrent - b
            Whether the newly inserted track should be considered as the current track. Setting this to trye has the same effect as calling GoTo afterwards.
        
        Adds a URI in the TrackList.
        
        If the CanEditTracks property is false, this has no effect.
        
        .. note::
            Clients should not assume that the track has been added at the time when this method returns. They should wait for a TrackAdded (or TrackListReplaced) signal.
        '''
        pass
    
    @DbusMethod
    def RemoveTrack(self, TrackId):
        '''
        
        **Parameters:**
        
        * TrackId - o (TrackId)
            Identifier of the track to be removed.
        
        Removes an item from the TrackList.
        
        If the track is not part of this tracklist, this has no effect.
        
        If the CanEditTracks property is false, this has no effect.
        
        .. note::
            Clients should not assume that the track has been removed at the time when this method returns. They should wait for a TrackRemoved (or TrackListReplaced) signal.
        '''
        pass
    
    @DbusMethod
    def GoTo(self, TrackId):
        '''
        **Parameters:**
        
        * TrackId - o (Track_Id)
            Identifier of the track to skip to.
        
        Skip to the specified TrackId.
        
        If the track is not part of this tracklist, this has no effect.
        
        If this object is not /org/mpris/MediaPlayer2, the current TrackList's tracks should be replaced with the contents of this TrackList, and the TrackListReplaced signal should be fired from /org/mpris/MediaPlayer2.
        '''
    
    @DbusSignal
    def TrackListReplaced(self):
    #def TrackListReplaced(self, Tracks, CurrentTrack):
        '''
        **Parameters:**
        
        * Tracks - ao (Track_Id_List)
            The new content of the tracklist.
        * CurrentTrack - o (Track_Id)
            The identifier of the track to be considered as current.
    
        Indicates that the entire tracklist has been replaced.
        
        It is left up to the implementation to decide when a change to the track list is invasive enough that this signal should be emitted instead of a series of TrackAdded and TrackRemoved signals.
        '''
        pass
    
    @DbusSignal
    def TrackAdded(self, Metadata, AfterTrack=''):
        '''
        **Parameters:**
        
        * Metadata - a{sv} (Metadata_Map)
            The metadata of the newly added item.
            
            This must include a mpris:trackid entry.
            
            See the type documentation for more details.
        * AfterTrack - o (Track_Id)
            The identifier of the track after which the new track was inserted. An empty string means at the begining of the tracklist.

        Indicates that a track has been added to the track list.
        '''
        pass
    
    @DbusSignal
    def TrackRemoved(self, TrackId):
        '''
        **Parameters:**
        
        * TrackId - o (Track_Id)
            The identifier of the track being removed.

        Indicates that a track has been removed from the track list.
        '''
        pass
    
    @DbusSignal
    def TrackMetadataChanged(self, TrackId, Metadata):
        '''
        **Parameters:**
        
        * TrackId - o (Track_Id)
            The id of the track which metadata has changed.
        * Metadata - a{sv} (Metadata_Map)
            The new track metadata.    

            This must include a mpris:trackid entry.

            See the type documentation for more details.

        Indicates that the metadata of a track in the tracklist has changed.

        This may indicate that a track has been replaced, in which case the mpris:trackid metadata entry is different from the TrackId argument.
        '''
        pass
    
    @DbusAttr
    def Tracks(self):
        '''
        **Returns:**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted, but the new value is not sent.
        
        An array which contains the identifier of each track in the tracklist, in order.        

        The org.freedesktop.DBus.Properties.PropertiesChanged signal is emited every time this property changes, but the signal message does not contain the new value. Client implementations should rather rely on the TrackAdded, TrackRemoved and TrackListReplaced signals to keep their representation of the tracklist up to date.
        '''
        pass
    
    @DbusAttr
    def CanEditTracks(self):
        '''
        **Returns:**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        If false, calling AddTrack or RemoveTrack will have no effect, and may raise a NotSupported error.
        '''
        pass
    
if __name__ == '__main__':
    from mpris2.utils import SomePlayers
    uri = Interfaces.MEDIA_PLAYER + '.' + SomePlayers.GMUSICBROWSER
    mp2 = TrackList(dbus_interface_info={'dbus_uri': uri}) #some one know any player that support it?
    print(mp2)
