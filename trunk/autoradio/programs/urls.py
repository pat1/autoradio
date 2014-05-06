from django.conf.urls import *
#from django.contrib import admin

#from models import Program, Schedule

urlpatterns = patterns('autoradio.programs.views',
    (r'^$', 'index'),
    (r'^xmms/$', 'dbusstato'),
    (r'^programsbook/$', 'programsbook'),
)
