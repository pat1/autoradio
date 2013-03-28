# Django settings for autoradio project.

import os
from configobj import ConfigObj,flatten_errors
from validate import Validator

configspec={}

configspec['django']={}

configspec['django']['DEBUG']="boolean(default=True)"
configspec['django']['TEMPLATE_DEBUG']="boolean(default=True)"
configspec['django']['FILE_UPLOAD_PERMISSIONS']="integer(default=420)"
configspec['django']['SECRET_KEY']="string(default='random-string-of-ascii')"
configspec['django']['SESSION_COOKIE_DOMAIN']="string(default=None)"
configspec['django']['SERVER_EMAIL']="string(default='localhost')"
configspec['django']['EMAIL_HOST']="string(default='localhost')"
configspec['django']['TIME_ZONE']="string(default='Europe/Rome')"
configspec['django']['LANGUAGE_CODE']="string(default='en-us')"
configspec['django']['SITE_ID']="integer(default=1)"
configspec['django']['USE_I18N']="boolean(default=True)"
configspec['django']['LOCALE_PATHS']="list(default=list('locale',))"
configspec['django']['ADMINS']="list(default=list('',))"
configspec['django']['MANAGERS']="list(default=list('',))"                  
configspec['django']['MEDIA_ROOT']="string(default='%s/media/')" % os.getcwd()
configspec['django']['MEDIA_SITE_ROOT']="string(default='%s/media/')" % os.getcwd()
configspec['django']['TEMPLATE_DIRS']="list(default=list('templates',))"
configspec['django']['BASE_URL']="string(default='/django/')"
configspec['django']['ADMIN_MEDIA_PREFIX']="string(default='/django/media/admin/')"
configspec['django']['STATIC_URL']="string(default='/django/media/')"
configspec['django']['STATIC_ROOT'] = "string(default='/usr/lib/python2.7/site-packages/django/contrib/admin/static/admin/')"
configspec['django']['MEDIA_PREFIX']="string(default='/media/')"
configspec['django']['MEDIA_SITE_PREFIX']="string(default='/media/sito/')"
configspec['django']['SERVE_STATIC']="boolean(default=True)"


configspec['autoradioweb']={}

configspec['autoradioweb']['logfile']  = "string(default='/tmp/autoradioweb.log')"
configspec['autoradioweb']['errfile']  = "string(default='/tmp/autoradioweb.err')"
configspec['autoradioweb']['lockfile'] = "string(default='/tmp/autoradioweb.lock')"
configspec['autoradioweb']['user']     = "string(default=None)"
configspec['autoradioweb']['group']    = "string(default=None)"
configspec['autoradioweb']['port']    = "string(default='8080')"
configspec['autoradioweb']['permit_no_playable_files'] = "boolean(default=False)"
configspec['autoradioweb']['require_tags_in_enclosure'] = "boolean(default=False)"


configspec['database']={}

configspec['database']['DATABASE_USER']="string(default='')"
configspec['database']['DATABASE_PASSWORD']="string(default='')"
configspec['database']['DATABASE_HOST']="string(default='localhost')"
configspec['database']['DATABASE_PORT']="integer(default=3306)"
configspec['database']['DATABASE_ENGINE']="string(default='sqlite3')"
configspec['database']['DATABASE_NAME']="string(default='%s/autoradio.sqlite3')" % os.getcwd()


configspec['autoplayer']={}

configspec['autoplayer']['logfile']  = "string(default='/tmp/autoplayer.log')"
configspec['autoplayer']['errfile']  = "string(default='/tmp/autoplayer.err')"
configspec['autoplayer']['lockfile'] = "string(default='/tmp/autoplayer.lock')"
configspec['autoplayer']['user']     = "string(default=None)"
configspec['autoplayer']['group']    = "string(default=None)"
configspec['autoplayer']['busaddress']    = "string(default=None)"
configspec['autoplayer']['audiosink']    = "string(default=None)"

configspec['autoradiodbus']={}

configspec['autoradiodbus']['logfile']  = "string(default='/tmp/autoradiodbus.log')"
configspec['autoradiodbus']['errfile']  = "string(default='/tmp/autoradiodbus.err')"
configspec['autoradiodbus']['lockfile'] = "string(default='/tmp/autoradiodbus.lock')"
configspec['autoradiodbus']['conffile'] = "string(default='dbus-autoradio.conf')"
configspec['autoradiodbus']['user']     = "string(default=None)"
configspec['autoradiodbus']['group']    = "string(default=None)"


configspec['jackdaemon']={}

configspec['jackdaemon']['logfile']  = "string(default='/tmp/jackdaemon.log')"
configspec['jackdaemon']['errfile']  = "string(default='/tmp/jackdaemon.err')"
configspec['jackdaemon']['lockfile'] = "string(default='/tmp/jackdaemon.lock')"
configspec['jackdaemon']['user']     = "string(default=None)"
configspec['jackdaemon']['group']    = "string(default=None)"


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

# section django
DEBUG                   = config['django']['DEBUG']                     
TEMPLATE_DEBUG          = config['django']['TEMPLATE_DEBUG']            
FILE_UPLOAD_PERMISSIONS = config['django']['FILE_UPLOAD_PERMISSIONS']   
SECRET_KEY              = config['django']['SECRET_KEY']                
SESSION_COOKIE_DOMAIN   = config['django']['SESSION_COOKIE_DOMAIN']     
SERVER_EMAIL            = config['django']['SERVER_EMAIL']              
EMAIL_HOST              = config['django']['EMAIL_HOST']                
TIME_ZONE               = config['django']['TIME_ZONE']                 
LANGUAGE_CODE           = config['django']['LANGUAGE_CODE']             
SITE_ID                 = config['django']['SITE_ID']                   
USE_I18N                = config['django']['USE_I18N']                  
LOCALE_PATHS            = config['django']['LOCALE_PATHS']              
ADMINS                  = config['django']['ADMINS']                    
MANAGERS                = config['django']['MANAGERS']                  
MEDIA_ROOT              = config['django']['MEDIA_ROOT']
if "%s" in MEDIA_ROOT:
    MEDIA_ROOT = MEDIA_ROOT  % os.getcwd()
MEDIA_SITE_ROOT         = config['django']['MEDIA_SITE_ROOT']
if "%s" in MEDIA_SITE_ROOT:
    MEDIA_SITE_ROOT = MEDIA_SITE_ROOT  % os.getcwd()
TEMPLATE_DIRS           = config['django']['TEMPLATE_DIRS']
BASE_URL                = config['django']['BASE_URL']
ADMIN_MEDIA_PREFIX      = config['django']['ADMIN_MEDIA_PREFIX']
STATIC_URL              = config['django']['STATIC_URL']
STATIC_ROOT             = config['django']['STATIC_ROOT']
MEDIA_PREFIX            = config['django']['MEDIA_PREFIX']
MEDIA_SITE_PREFIX       = config['django']['MEDIA_SITE_PREFIX']
SERVE_STATIC            = config['django']['SERVE_STATIC']
MEDIA_URL               = BASE_URL+MEDIA_PREFIX
SITE_MEDIA_URL          = BASE_URL+MEDIA_SITE_PREFIX



# section autoradioweb
logfileweb              = config['autoradioweb']['logfile']
errfileweb              = config['autoradioweb']['errfile']
lockfileweb             = config['autoradioweb']['lockfile']
userweb                 = config['autoradioweb']['user']
groupweb                = config['autoradioweb']['group']
port                    = config['autoradioweb']['port']
permit_no_playable_files= config['autoradioweb']['permit_no_playable_files']
require_tags_in_enclosure= config['autoradioweb']['require_tags_in_enclosure']

# section database
DATABASE_USER     = config['database']['DATABASE_USER']        
DATABASE_PASSWORD = config['database']['DATABASE_PASSWORD']    
DATABASE_HOST     = config['database']['DATABASE_HOST']        
DATABASE_PORT     = config['database']['DATABASE_PORT']        
DATABASE_ENGINE   = config['database']['DATABASE_ENGINE']      
DATABASE_NAME     = config['database']['DATABASE_NAME']        

# section autoplayer
logfileplayer              = config['autoplayer']['logfile']
errfileplayer              = config['autoplayer']['errfile']
lockfileplayer             = config['autoplayer']['lockfile']
userplayer                 = config['autoplayer']['user']
groupplayer                = config['autoplayer']['group']
busaddressplayer           = config['autoplayer']['busaddress']
audiosinkplayer            = config['autoplayer']['audiosink']

# section autoradiodbus
logfiledbus              = config['autoradiodbus']['logfile']
errfiledbus              = config['autoradiodbus']['errfile']
lockfiledbus             = config['autoradiodbus']['lockfile']
conffiledbus             = config['autoradiodbus']['conffile']
userdbus                 = config['autoradiodbus']['user']
groupdbus                = config['autoradiodbus']['group']

# section jackdaemon
logfilejack              = config['jackdaemon']['logfile']
errfilejack              = config['jackdaemon']['errfile']
lockfilejack             = config['jackdaemon']['lockfile']
userjack                 = config['jackdaemon']['user']
groupjack                = config['jackdaemon']['group']


if DATABASE_ENGINE == "mysql":
    # Recommended for MySQL. See http://code.djangoproject.com/ticket/13906 
    # to avoid "Lost connection to MySQL server at 'reading authorization packet', system error: 0"
    # connect_timeout=30
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.'+DATABASE_ENGINE,
            'NAME':    DATABASE_NAME,
            'USER':    DATABASE_USER,
            'PASSWORD':DATABASE_PASSWORD,
            'HOST':    DATABASE_HOST,
            'PORT':    DATABASE_PORT,
            'OPTIONS': {'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
                        'connect_timeout':60}, 
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.'+DATABASE_ENGINE,
            'NAME':    DATABASE_NAME,
            'USER':    DATABASE_USER,
            'PASSWORD':DATABASE_PASSWORD,
            'HOST':    DATABASE_HOST,
            'PORT':    DATABASE_PORT,
            }
        }
    

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware')

ROOT_URLCONF = 'autoradio.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'autoradio.programs',
    'autoradio.jingles',
    'autoradio.spots',
    'autoradio.playlists',
    'autoradio.doc',
)

# django save the files on memory, but large files are saved in a path.
# The size of "large file" can be defined in settings using 
# FILE_UPLOAD_MAX_MEMORY_SIZE and The FILE_UPLOAD_HANDLERS by default are:
#("django.core.files.uploadhandler.MemoryFileUploadHandler",
# "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

# remove MemoryFileUploadHandler
FILE_UPLOAD_HANDLERS = (
"django.core.files.uploadhandler.TemporaryFileUploadHandler",)

try:
    import django_extensions
    INSTALLED_APPS += 'django_extensions',
except ImportError:
    print "django_extensions is not installed; I do not use it"
    pass
