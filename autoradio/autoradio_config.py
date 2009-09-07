#!/usr/bin/python
# GPL. (C) 2007-2009 Paolo Patruno.

#####
#import ConfigParser, os
#
#config = ConfigParser.ConfigParser()
#config.readfp(open('/etc/autoradio/autoradio.cfg'))
#config.read(['/etc/autoradio/site.cfg', os.path.expanduser('~/.autoradio.cfg')])
####

# to use the amarok player (osolete)
amarok=False

#directory to put playlists
#playlistdir="playlist"
playlistdir="spots"

# path to working file
logfile='/tmp/autoradio.log'
lockfile = "/tmp/autoradio.lock"
timestampfile = "/tmp/autoradio.timestamp"

# root path where to find media
import os
BASE_PATH=os.getcwd()

# host xmms is running on
XMMSHOST='localhost'

#backward and forward time intervat to check for schedule conflict 
minelab=180

# tollerance time interval to recovery schedule not done ( backward time when start autoradiod )
# to adjust the programming you have to make changes minsched minutes before
minsched=5

####

from django.core.management import setup_environ
import settings
setup_environ(settings)

import locale
locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
