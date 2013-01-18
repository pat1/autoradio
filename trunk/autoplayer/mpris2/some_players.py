class Some_Players(object):
    '''
    Not defined in documentation
    
    Maybe this player (and other) implement mpris2
    
     **Some players**
    
    * AUDACIOUS
        "audacious"
    * AUTOPLAYER
        "AutoPlayer"
    * BANSHEE 
        "banshee"
    * BEATBOX
        "beatbox"
    * BMP
        "bmp"
    * CLEMENTINE
        "clementine"
    * DRAGONPLAYER
        "dragonplayer"
    * EXAILE
        "exaile"
    * GMUSICBROWSER
        "gmusicbrowser"
    * GMPC
        "gmpc"
    * GUAYADEQUE
        "guayadeque"
    * MOPIDY
        "mopidy"
    * MPDRIS
        "mpDris"
    * QUODLIBET
        "quodlibet"
    * RAVEND
        "ravend"
    * RHYTHMBOX
        "rhythmbox"
    * SPOTIFY
        "spotify"
    * VLC
        "vlc"
    * XBMC
        "xbmc"
    * XMMS2
        "xmms2"
    * XNOISE
        "xnoise"
    '''
    #Some players
    AUDACIOUS = "audacious"
    AUTOPLAYER = "AutoPlayer"
    BANSHEE = "banshee"
    BEATBOX = "beatbox"
    BMP = "bmp"
    CLEMENTINE = "clementine"
    DRAGONPLAYER = "dragonplayer"
    EXAILE = "exaile"
    GMUSICBROWSER = "gmusicbrowser"
    GMPC = "gmpc"
    GUAYADEQUE = "guayadeque"
    MOPIDY = "mopidy"
    MPDRIS = "mpDris"
    QUODLIBET = "quodlibet"
    RAVEND = "ravend"
    RHYTHMBOX = "rhythmbox"
    SPOTIFY = "spotify"
    VLC = "vlc"
    XBMC = "xbmc"
    XMMS2 = "xmms2"
    XNOISE = "xnoise"
    
    @staticmethod
    def get_dict():
        result  = {}
        for key in dir(Some_Players):
            if key[0] not in ('_', 'g'):
                result[key] = getattr(Some_Players, key)
        return result
