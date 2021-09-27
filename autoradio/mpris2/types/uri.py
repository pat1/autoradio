'''
From mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/2.2/Playlists_Interface.html#Simple-Type:Uri
'''


class Uri(str):
    '''A unique resource identifier.'''

    def __init__(self, uri):
        self._uri = uri
    
    def __str__(self):
        return str(self._uri)
    
if __name__ == '__main__':
    assert Uri('http://www.com.br') == 'http://www.com.br'
