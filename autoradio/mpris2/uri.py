from __future__ import print_function
class Uri(str):
    '''A unique resource identifier.'''
    def __init__(self, uri, *args, **kw):
        super(Uri, self).__init__(uri, *args, **kw)
        self._uri = uri
    
    @property
    def uri(self):
        return self._uri
    
if __name__ == "__main__":
    print(Uri('http://www.com.br'))