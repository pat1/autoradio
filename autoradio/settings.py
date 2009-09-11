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
configspec['django']['MEDIA_URL']="string(default='/django/media/')"
configspec['django']['ADMIN_MEDIA_PREFIX']="string(default='/django/media/admin/')"

configspec['autoradioweb']={}

configspec['autoradioweb']['logfile']  = "string(default='/tmp/autoradioweb.log')"
configspec['autoradioweb']['errfile']  = "string(default='/tmp/autoradioweb.err')"
configspec['autoradioweb']['lockfile'] = "string(default='/tmp/autoradioweb.lock')"
configspec['autoradioweb']['user']     = "string(default=None)"
configspec['autoradioweb']['group']    = "string(default=None)"


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
MEDIA_URL               = config['django']['MEDIA_URL']
ADMIN_MEDIA_PREFIX      = config['django']['ADMIN_MEDIA_PREFIX']

# section autoradioweb
logfileweb              = config['autoradioweb']['logfile']
errfileweb              = config['autoradioweb']['errfile']
lockfileweb             = config['autoradioweb']['lockfile']
user                    = config['autoradioweb']['user']
group                   = config['autoradioweb']['group']


# section database
DATABASE_USER     = config['database']['DATABASE_USER']        
DATABASE_PASSWORD = config['database']['DATABASE_PASSWORD']    
DATABASE_HOST     = config['database']['DATABASE_HOST']        
DATABASE_PORT     = config['database']['DATABASE_PORT']        
DATABASE_ENGINE   = config['database']['DATABASE_ENGINE']      
DATABASE_NAME     = config['database']['DATABASE_NAME']        


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'autoradio.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'autoradio.programs',
    'autoradio.jingles',
    'autoradio.spots',
    'autoradio.playlists',
)
