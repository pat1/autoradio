'''
utils functions not defined in espec
Created on Nov 6, 2011

@author: hugosenari
'''
from __future__ import print_function
from __future__ import absolute_import

import dbus, re
from .some_players import Some_Players as SomePlayers
from .interfaces import Interfaces

def _match_players_uri(name, pattern='.+'):
    '''
        Filter logic for get_players and get_player_uri
        @param name: string name to test
        @param pattern=None:  string regexp to test
        @return: boolean
    '''
    return \
        re.match('org.mpris.MediaPlayer2', name)\
            and re.match(pattern, name)

def get_session(busaddress=None):
    '''
        @return: dbus.SessionBus.get_session()
    '''

    if busaddress is None:
        return dbus.SessionBus.get_session()
    else:
        return dbus.bus.BusConnection(busaddress)



def get_players_uri(pattern='.',busaddress=None):
    """
        Return string of player bus name
        @param pattern=None: string regex that filter response
        @return: array string of players bus name
    """
    return [item
        for item in get_session(busaddress).list_names()
            if _match_players_uri(item, pattern)]

def get_player_id_from_uri(uri):
    """
        Returns player mpris2 id from uri
        @param uri: string mpris2 player dbus uri
        @return: string mrpis2 id
    """
    print(uri)
    mateched = re.match(Interfaces.MEDIA_PLAYER + '\.(.+)', uri or '')
    return mateched.groups()[0]\
        if mateched\
        else ''

def get_players_id(pattern=None):
    """
        Return string of player mpris2 id
        @param pattern=None: string regex that filter response
        @return: array string of players bus name
    """
    for item in get_session().list_names():
        if _match_players_uri(item, pattern):
            yield get_player_id_from_uri(item)
    
def get_intances_of(what_to_instantiate, pattern):
    """
        Return new instance of what_to_instantiate
        @param what_to_instantiate: class or function with dbus_uri only param
        @param pattern=None: string regexo that filter response
        @return: array string of players bus name
    """
    return [what_to_instantiate(dbus_uri=item)
        for item in get_session().list_names()
            if _match_players_uri(item, pattern)]
    
def unix_path_to_uri():
    pass

if __name__ == '__main__':
    print(get_players_uri())
    print(SomePlayers.get_dict())
    print(get_player_id_from_uri('org.mpris.MediaPlayer2.banshee'))
