'''
Created on Nov 12, 2011

@author: hugosenari
'''

    
ALPHABETICAL = 'Alphabetical'
CREATION_DATE = 'CreationDate'
MODIFIED_DATE = 'ModifiedDate'
LAST_PLAY_DATE = 'LastPlayDate'
USER_DEFINE = 'UserDefined'

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
    
    ALPHABETICAL = ALPHABETICAL
    CREATION_DATE = CREATION_DATE
    MODIFIED_DATE = MODIFIED_DATE
    LAST_PLAY_DATE = LAST_PLAY_DATE
    USER_DEFINE = USER_DEFINE
    VALUES = (ALPHABETICAL,CREATION_DATE,MODIFIED_DATE,LAST_PLAY_DATE,USER_DEFINE)
    
    def __init__(self, ordering, *args, **kw):
        '''
        Constructor
        '''
        self._ordering = ordering
        super(Playlist_Ordering, self).__init__(ordering, *args, **kw)
    
    @property
    def ordering(self):
        return self._ordering
    