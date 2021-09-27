'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/2.2/Playlists_Interface.html#Enum:Playlist_Ordering
'''


class Playlist_Ordering(str):
    '''
    Specifies the ordering of returned playlists.

    * Alphabetical (Alphabetical)
        Alphabetical ordering by name, ascending.
    * CreationDate (Created)
        Ordering by creation date, oldest first.
    * ModifiedDate (Modified)
        Ordering by last modified date, oldest first.
    * LastPlayDate (Played)
        Ordering by date of last playback, oldest first.
    * UserDefined (User)
        A user-defined ordering.
    '''

    ALPHABETICAL = 'Alphabetical'
    CREATION_DATE = 'CreationDate'
    MODIFIED_DATE = 'ModifiedDate'
    LAST_PLAY_DATE = 'LastPlayDate'
    USER_DEFINE = 'UserDefined'    
    VALUES = (ALPHABETICAL,CREATION_DATE,MODIFIED_DATE,LAST_PLAY_DATE,USER_DEFINE)
    
    def __init__(self, ordering):
        self._ordering = ordering

    def __str__(self):
        return self._ordering


if __name__ == '__main__':
    po = Playlist_Ordering('Alphabetical')
    assert po == 'Alphabetical'
    assert po == Playlist_Ordering.ALPHABETICAL
    assert po != Playlist_Ordering.CREATION_DATE
