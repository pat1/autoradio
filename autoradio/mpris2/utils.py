'''
utils functions not defined in espec
'''

import re

from .interfaces import Interfaces
from .decorator.utils import get_session, get_uri, get_mainloop  # @UnusedImport
from .decorator.utils import list_interfaces as _list_interfaces
from .decorator.utils import implements as _implements

def get_players_uri(pattern=''):
    '''
        Return string of player bus name
        @param pattern=None: string RegEx that filter response
        @return: array string of players bus name
    '''
    return get_uri(Interfaces.MEDIA_PLAYER + '.*' + pattern)


def get_player_id_from_uri(uri):
    '''
        Returns player mpris2 id from uri
        @param uri: string mpris2 player dbus uri
        @return: string mrpis2 id
    '''
    mateched = re.match(Interfaces.MEDIA_PLAYER + '\.(.+)', uri or '')
    return mateched.groups()[0]\
        if mateched\
        else ''

def get_players_id(pattern=None):
    '''
        Return string of player mpris2 id
        @param pattern=None: string RegEx that filter response
        @return: array string of players bus name
    '''
    for item in get_uri(Interfaces.MEDIA_PLAYER + '.*' + pattern):
        yield get_player_id_from_uri(item)

def list_interfaces(uri, path=None, bus=None):
    return _list_interfaces(uri, path or Interfaces.OBJECT_PATH, bus)
        
def implements(uri, interface, path=Interfaces.OBJECT_PATH, bus=None):
    return _implements(uri, interface, path or Interfaces.OBJECT_PATH, bus)


if __name__ == '__main__':
    uris = get_players_uri()
    if not uris:
        print('No running players')
    for uri in uris:
        print(uri, ':')
        for interface in list_interfaces(uri):
            print('\t', interface)
