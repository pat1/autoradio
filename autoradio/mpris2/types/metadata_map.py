'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html#Mapping:Metadata_Map
'''


class Metadata_Map(dict):
    '''
    A mapping from metadata attribute names to values.
    
    The mpris:trackid attribute must always be present. This contains a string that uniquely identifies the track within the scope of the playlist.
    
    If the length of the track is known, it should be provided in the metadata property with the 'mpris:length' key. The length must be given in microseconds, and be represented as a signed 64-bit integer.
    
    If there is an image associated with the track, a URL for it may be provided using the 'mpris:artUrl' key. For other metadata, fields defined by the Xesam ontology should be used, prefixed by 'xesam:'. See http://wiki.xmms2.xmms.se/wiki/MPRIS_Metadata for a list of common fields.
    
    Lists of strings should be passed using the array-of-string ('as') D-Bus type. Dates should be passed as strings using the ISO 8601 extended format (eg: 2007-04-29T14:35:51). If the timezone is known, RFC 3339's internet profile should be used (eg: 2007-04-29T14:35:51+02:00).
    
    * Attribute - s
        The name of the attribute; see http://wiki.xmms2.xmms.se/wiki/MPRIS_Metadata for guidelines on names to use.
    * Value - v
        The value of the attribute, in the most appropriate format.
    '''
    ART_URI = 'mpris:artUrl'
    TRACKID = 'mpris:trackid'
    LENGTH = 'mpris:length'
    ALBUM = 'xesam:album'
    ALBUM_ARTIST = 'xesam:albumArtist'
    ARTIST = 'xesam:artist'
    AS_TEXT = 'xesam:asText'
    AUDIO_BPM = 'xesam:audioBPM'
    AUTO_RATING = 'xesam:autoRating'
    COMMENT = 'xesam:comment'
    COMPOSER = 'xesam:composer'
    CONTENT_CREATED = 'xesam:contentCreated'
    DISC_NUMBER = 'xesam:discNumber'
    FIRST_USED = 'xesam:firstUsed'
    GENRE = 'xesam:genre'
    LAST_USED = 'xesam:lastUsed'
    LYRICIST = 'xesam:lyricist'
    TITLE = 'xesam:title'
    TRACK_NUMBER = 'xesam:trackNumber'
    URL = 'xesam:url'
    USE_COUNT = 'xesam:useCount'
    USER_RATING = 'xesam:userRating'

    def __init__(self, metadata):
        super(Metadata_Map, self).__init__(**metadata)


if __name__ == '__main__':
    mdm = Metadata_Map({Metadata_Map.ALBUM : 'Marcelo Nova Ao Vivo'})
    assert mdm[Metadata_Map.ALBUM] == 'Marcelo Nova Ao Vivo'
