from django.conf.urls.defaults import *
#from django.contrib import admin

#from models import Program, Schedule

urlpatterns = patterns('autoradio.programs.views',
    (r'^$', 'index'),
    (r'^xmms/$', 'stato'),
    (r'^programsbook/$', 'programsbook'),
)
