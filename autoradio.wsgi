import os
import sys
import autoradio.settings
import autoradio.autoradio_config

os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


## from django 1.4
#import os
#
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
## This application object is used by the development server
## as well as any WSGI server configured to use this file.
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
