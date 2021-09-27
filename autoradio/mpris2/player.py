'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html
'''

from .decorator import DbusAttr
from .decorator import DbusInterface
from .decorator import DbusMethod
from .decorator import DbusSignal
from .interfaces import Interfaces
from .types import Time_In_Us
from .types import Loop_Status
from .types import Playback_Status
from .types import Playback_Rate
from .types import Metadata_Map
from .types import Volume


class Player(Interfaces):
    '''
    This interface implements the methods for querying and providing basic control over what is currently playing.
    '''
    
    @DbusInterface(Interfaces.PLAYER, Interfaces.OBJECT_PATH)
    def __init__(self):
        '''Constructor'''
        
    
    @DbusMethod
    def Next(self):
        '''
        Skips to the next track in the tracklist.

        If there is no next track (and endless playback and track repeat are both off), stop playback.

        If playback is paused or stopped, it remains that way.

        If CanGoNext is false, attempting to call this method should have no effect.
        '''
        
    
    @DbusMethod 
    def Previous(self):
        '''
        Skips to the previous track in the tracklist.

        If there is no previous track (and endless playback and track repeat are both off), stop playback.

        If playback is paused or stopped, it remains that way.

        If CanGoPrevious is false, attempting to call this method should have no effect.
        '''
        
    
    @DbusMethod
    def Pause(self):
        '''
        Pauses playback.

        If playback is already paused, this has no effect.

        Calling Play after this should cause playback to start again from the same position.

        If CanPause is false, attempting to call this method should have no effect.
        '''
        
    
    @DbusMethod
    def PlayPause(self):
        '''
        Pauses playback.

        If playback is already paused, resumes playback.

        If playback is stopped, starts playback.

        If CanPause is false, attempting to call this method should have no effect and raise an error.
        '''
        
    
    @DbusMethod
    def Stop(self):
        '''
        Stops playback.

        If playback is already stopped, this has no effect.

        Calling Play after this should cause playback to start again from the beginning of the track.

        If CanControl is false, attempting to call this method should have no effect and raise an error.
        '''
        
    
    @DbusMethod
    def Play(self):
        '''
        Starts or resumes playback.

        If already playing, this has no effect.

        If there is no track to play, this has no effect.

        If CanPlay is false, attempting to call this method should have no effect.
        '''
        
    
    @DbusMethod
    def Seek(self, Offet):
        '''
        **Parameters:**

        * Offset - x (Time_In_Us)
            The number of microseconds to seek forward.
            
        Seeks forward in the current track by the specified number of microseconds.

        A negative value seeks back. If this would mean seeking back further than the start of the track, the position is set to 0.

        If the value passed in would mean seeking beyond the end of the track, acts like a call to Next.

        If the CanSeek property is false, this has no effect.
        '''
        
    
    @DbusMethod
    def SetPosition(self, TrackId, Position):
        '''
        **Parameters**
        
        * TrackId - o (Track_Id)
            The currently playing track's identifier.

            If this does not match the id of the currently-playing track, the call is ignored as 'stale'.
        * Position - x (Time_In_Us)
            Track position in microseconds.

            This must be between 0 and <track_length>.
            
        Sets the current track position in microseconds.

        If the Position argument is less than 0, do nothing.

        If the Position argument is greater than the track length, do nothing.

        If the CanSeek property is false, this has no effect.
        '''
        
    
    @DbusMethod
    def OpenUri(self, Uri):
        '''
        **Parameters:**
        
        * Uri - s (Uri)
            Uri of the track to load. Its uri scheme should be an element of the org.mpris.MediaPlayer2.SupportedUriSchemes property and the mime-type should match one of the elements of the org.mpris.MediaPlayer2.SupportedMimeTypes.
        
        Opens the Uri given as an argument

        If the playback is stopped, starts playing

        If the uri scheme or the mime-type of the uri to open is not supported, this method does nothing and may raise an error. In particular, if the list of available uri schemes is empty, this method may not be implemented.

        Clients should not assume that the Uri has been opened as soon as this method returns. They should wait until the mpris:trackid field in the Metadata property changes.

        If the media player implements the TrackList interface, then the opened track should be made part of the tracklist, the org.mpris.MediaPlayer2.TrackList.TrackAdded or org.mpris.MediaPlayer2.TrackList.TrackListReplaced signal should be fired, as well as the org.freedesktop.DBus.Properties.PropertiesChanged signal on the tracklist interface.
        '''
        
    
    @DbusSignal
    def Seeked(self, Position):
        '''
        **Parameters:**
        
        * Position - x (Time_In_Us)
            The new position, in microseconds.

        Indicates that the track position has changed in a way that is inconsistant with the current playing state.

        When this signal is not received, clients should assume that:

        * When playing, the position progresses according to the rate property.
        * When paused, it remains constant.

        This signal does not need to be emitted when playback starts or when the track changes, unless the track is starting at an unexpected position. An expected position would be the last known one when going from Paused to Playing, and 0 when going from Stopped to Playing.
        '''
        return Time_In_Us(Position)

    @DbusSignal(iface=Interfaces.PROPERTIES)
    def PropertiesChanged(self, *args, **kw):
        '''
        **Parameters**
        
        * args - list
            unnamed parameters passed by dbus signal
        * kw - dict
            named parameters passed by dbus signal
            
        Every time that some property change, signal will be called
        '''
        
    
    @DbusAttr(produces=Playback_Status)
    def PlaybackStatus(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
            
        The current playback status.
        
        May be 'Playing', 'Paused' or 'Stopped'.
        '''
        
    
    @DbusAttr(produces=Loop_Status)
    def LoopStatus(self):
        '''
        **Returns**
        
        Read/Write
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.

        The current loop / repeat status
        
        May be:
        
        * 'None' if the playback will stop when there are no more tracks to play
        * 'Track' if the current track will start again from the begining once it has finished playing
        * 'Playlist' if the playback loops through a list of tracks
        
        This property is optional, and clients should deal with NotSupported errors gracefully.
        
        If CanControl is false, attempting to set this property should have no effect and raise an error.
        '''
            

    @DbusAttr(produces=Playback_Rate)
    def Rate(self):
        '''
        **Returns**
        
        Read/Write
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        The current playback rate.
        
        The value must fall in the range described by MinimumRate and MaximumRate, and must not be 0.0. If playback is paused, the PlaybackStatus property should be used to indicate this. A value of 0.0 should not be set by the client. If it is, the media player should act as though Pause was called.
        
        If the media player has no ability to play at speeds other than the normal playback rate, this must still be implemented, and must return 1.0. The MinimumRate and MaximumRate properties must also be set to 1.0.
        
        Not all values may be accepted by the media player. It is left to media player implementations to decide how to deal with values they cannot use; they may either ignore them or pick a 'best fit' value. Clients are recommended to only use sensible fractions or multiples of 1 (eg: 0.5, 0.25, 1.5, 2.0, etc).
        '''
        

    @DbusAttr
    def Shuffle(self):
        '''
        **Returns**
        
        Read/Write
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        A value of false indicates that playback is progressing linearly through a playlist, while true means playback is progressing through a playlist in some other order.
        
        This property is optional, and clients should deal with NotSupported errors gracefully.
        
        If CanControl is false, attempting to set this property should have no effect and raise an error.
        '''
        

    @DbusAttr(produces=Metadata_Map)
    def Metadata(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        The metadata of the current element.
        
        If there is a current track, this must have a 'mpris:trackid' entry at the very least, which contains a string that uniquely identifies this track.
        
        See the type documentation for more details.
        '''
        

    @DbusAttr(produces=Volume)
    def Volume(self):
        '''
        **Returns**
        
        Read/Write
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        The volume level.
        
        When setting, if a negative value is passed, the volume should be set to 0.0.
        
        If CanControl is false, attempting to set this property should have no effect and raise an error.
        '''
        

    @DbusAttr
    def Position(self):
        '''
        **Returns**
        
        Read only
            The org.freedesktop.DBus.Properties.PropertiesChanged signal is not emitted when this property changes.
        
        The current track position in microseconds, between 0 and the 'mpris:length' metadata entry (see Metadata).
        
        .. note::
            If the media player allows it, the current playback position can be changed either the SetPosition method or the Seek method on this interface. If this is not the case, the CanSeek property is false, and setting this property has no effect and can raise an error.
        
        If the playback progresses in a way that is inconstistant with the Rate property, the Seeked signal is emited.
        '''
        

    @DbusAttr
    def MinimumRate(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        The minimum value which the Rate property can take. Clients should not attempt to set the Rate property below this value.
        
        Note that even if this value is 0.0 or negative, clients should not attempt to set the Rate property to 0.0.
        
        This value should always be 1.0 or less.
        '''
        

    @DbusAttr
    def MaximumRate(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        The maximum value which the Rate property can take. Clients should not attempt to set the Rate property above this value.
        
        This value should always be 1.0 or greater.
        '''
        

    @DbusAttr
    def CanGoNext(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Whether the client can call the Next method on this interface and expect the current track to change.
        
        If CanControl is false, this property should also be false.
        '''
        
    
    @DbusAttr
    def CanGoPrevious(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Whether the client can call the Previous method on this interface and expect the current track to change.
        
        If CanControl is false, this property should also be false.
        '''
        
    
    @DbusAttr
    def CanPlay(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Whether playback can be started using Play or PlayPause.
        
        Note that this is related to whether there is a 'current track': the value should not depend on whether the track is currently paused or playing. In fact, if a track is currently playing CanControl is true), this should be true.
        
        If CanControl is false, this property should also be false.
        '''
        
        
    @DbusAttr
    def CanPause(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Whether playback can be paused using Pause or PlayPause.
        
        Note that this is an intrinsic property of the current track: its value should not depend on whether the track is currently paused or playing. In fact, if playback is currently paused (and CanControl is true), this should be true.
        
        If CanControl is false, this property should also be false.
        '''
    
    @DbusAttr
    def CanSeek(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
        
        Whether the client can control the playback position using Seek and SetPosition. This may be different for different tracks.
        
        If CanControl is false, this property should also be false.
        '''
    
    @DbusAttr
    def CanControl(self):
        '''
        **Returns**
        
        Read only
            The org.freedesktop.DBus.Properties.PropertiesChanged signal is not emitted when this property changes.
        
        Whether the media player may be controlled over this interface.
        
        This property is not expected to change, as it describes an intrinsic capability of the implementation.
        
        If this is false, clients should assume that all properties on this interface are read-only (and will raise errors if writing to them is attempted); all methods are not implemented and all other properties starting with 'Can' are also false.
        '''

    
if __name__ == '__main__':
    from .utils import get_players_uri, implements
    for uri in get_players_uri():
        if implements(uri, Interfaces.PLAYER):
            mp2 = Player(dbus_interface_info={'dbus_uri': uri})
            print( mp2.LoopStatus )
            print( mp2.Shuffle )
            mp2.Shuffle = not mp2.Shuffle
            print( mp2.Shuffle )
            break
    else:
        print('no player with player interface found')