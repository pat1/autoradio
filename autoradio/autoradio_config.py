#!/usr/bin/python
# GPL. (C) 2007-2009 Paolo Patruno.

import os
from configobj import ConfigObj,flatten_errors
from validate import Validator

configspec={}

configspec['autoradiod']={}

configspec['autoradiod']['playlistdir']   = "string(default='spots')"
configspec['autoradiod']['logfile']       = "string(default='/tmp/autoradio.log')"
configspec['autoradiod']['lockfile']      = "string(default='/tmp/autoradio.lock')"
configspec['autoradiod']['timestampfile'] = "string(default='/tmp/autoradio.timestamp')"
configspec['autoradiod']['base_path']     = "string(default=%s)" % os.getcwd()
configspec['autoradiod']['xmms_host']     = "string(default='localhost')"
configspec['autoradiod']['minelab']       = "integer(60,360,default=180)"
configspec['autoradiod']['minsched']      = "integer(3,20,default=5)"
configspec['autoradiod']['locale']        = "string(default='it_IT.UTF-8')"
configspec['autoradiod']['user']          = "string(default=None)"
configspec['autoradiod']['group']         = "string(default=None)"
configspec['autoradiod']['display']       = "string(default=':0.0')"

config    = ConfigObj ('/etc/autoradio/autoradio-site.cfg',file_error=False,configspec=configspec)

usrconfig = ConfigObj (os.path.expanduser('~/.autoradio.cfg'),file_error=False)
config.merge(usrconfig)
usrconfig = ConfigObj ('autoradio.cfg',file_error=False)
config.merge(usrconfig)

val = Validator()
test = config.validate(val,preserve_errors=True)
for entry in flatten_errors(config, test):
    # each entry is a tuple
    section_list, key, error = entry
    if key is not None:
       section_list.append(key)
    else:
        section_list.append('[missing section]')
    section_string = ', '.join(section_list)
    if error == False:
        error = 'Missing value or section.'
    print section_string, ' = ', error
    raise error

# to use the amarok player (obsolete)
amarok=False

# section autoradiod
playlistdir   = config['autoradiod']['playlistdir']
logfile       = config['autoradiod']['logfile']
lockfile      = config['autoradiod']['lockfile']
timestampfile = config['autoradiod']['timestampfile']
BASE_PATH     = config['autoradiod']['base_path']
XMMSHOST      = config['autoradiod']['xmms_host']
minelab       = config['autoradiod']['minelab']
minsched      = config['autoradiod']['minsched']
user          = config['autoradiod']['user']
group         = config['autoradiod']['group']

import locale
locale.setlocale(locale.LC_ALL, config['autoradiod']['locale'])


####

from django.core.management import setup_environ
import settings
setup_environ(settings)

