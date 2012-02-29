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
configspec['django']['MEDIA_ROOT']="string(default='media/')"
configspec['django']['MEDIA_SITE_ROOT']="string(default='media/')"
configspec['django']['TEMPLATE_DIRS']="list(default=list('templates',))"
configspec['django']['BASE_URL']="string(default='/django/')"
configspec['django']['ADMIN_MEDIA_PREFIX']="string(default='/django/media/admin/')"
configspec['django']['MEDIA_PREFIX']="string(default='/media/')"
configspec['django']['SITE_MEDIA_PREFIX']="string(default='/media/sito/')"
configspec['django']['SERVE_STATIC']="boolean(default=True)"


configspec['autoradioweb']={}

configspec['autoradioweb']['logfile']  = "string(default='/tmp/autoradioweb.log')"
configspec['autoradioweb']['errfile']  = "string(default='/tmp/autoradioweb.err')"
configspec['autoradioweb']['lockfile'] = "string(default='/tmp/autoradioweb.lock')"
configspec['autoradioweb']['user']     = "string(default=None)"
configspec['autoradioweb']['group']    = "string(default=None)"
configspec['autoradioweb']['port']    = "string(default='8080')"


configspec['database']={}

configspec['database']['DATABASE_USER']="string(default='')"
configspec['database']['DATABASE_PASSWORD']="string(default='')"
configspec['database']['DATABASE_HOST']="string(default='localhost')"
configspec['database']['DATABASE_PORT']="integer(default=3306)"
configspec['database']['DATABASE_ENGINE']="string(default='sqlite3')"
configspec['database']['DATABASE_NAME']="string(default='%s/autoradio.sqlite3')" % os.getcwd()


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
MEDIA_SITE_ROOT         = config['django']['MEDIA_SITE_ROOT']
TEMPLATE_DIRS           = config['django']['TEMPLATE_DIRS']
BASE_URL                = config['django']['BASE_URL']
ADMIN_MEDIA_PREFIX      = config['django']['ADMIN_MEDIA_PREFIX']
MEDIA_PREFIX            = config['django']['MEDIA_PREFIX']
SITE_MEDIA_PREFIX       = config['django']['SITE_MEDIA_PREFIX']
SERVE_STATIC            = config['django']['SERVE_STATIC']
MEDIA_URL               = BASE_URL+MEDIA_PREFIX
SITE_MEDIA_URL          = BASE_URL+SITE_MEDIA_PREFIX



# section autoradioweb
logfileweb              = config['autoradioweb']['logfile']
errfileweb              = config['autoradioweb']['errfile']
lockfileweb             = config['autoradioweb']['lockfile']
userweb                 = config['autoradioweb']['user']
groupweb                = config['autoradioweb']['group']
port                    = config['autoradioweb']['port']

# section database
DATABASE_USER     = config['database']['DATABASE_USER']        
DATABASE_PASSWORD = config['database']['DATABASE_PASSWORD']    
DATABASE_HOST     = config['database']['DATABASE_HOST']        
DATABASE_PORT     = config['database']['DATABASE_PORT']        
DATABASE_ENGINE   = config['database']['DATABASE_ENGINE']      
DATABASE_NAME     = config['database']['DATABASE_NAME']        


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
    'autoradio.programs',
    'autoradio.jingles',
    'autoradio.spots',
    'autoradio.playlists',
    'autoradio.doc',
)

try:
    import django_extensions
    INSTALLED_APPS += 'django_extensions',
except ImportError:
    print "django_extensions is not installed; I do not use it"
    pass
