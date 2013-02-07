'''
Created on Nov 12, 2011

@author: hugosenari
'''

class Playlist_Id(str):
    '''
    Unique playlist identifier.
    '''

    def __init__(self, playlist_id, *args, **kw):
        '''
        Constructor
        '''
        self._playlist_id = playlist_id
        super(Playlist_Id, self).__init__(playlist_id, *args, **kw)
        