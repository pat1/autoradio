from django.conf.urls.defaults import *
#from django.contrib import admin

from models import Program, Schedule

urlpatterns = patterns('',
    (r'^$', 'autoradio.programs.views.index'),
    (r'^xmms/$', 'autoradio.programs.views.stato'),
    (r'^programsbook/$', 'autoradio.programs.views.programsbook'),
#    (r'^/schedule/(?P<schedule_id>\d+)/$', 'views.detail'),
#    (r'^schedule/(?P<schedule_id>\d+)/results/$', 'mysite.polls.views.results'),
#    (r'^schedule/(?P<schedule_id>\d+)/vote/$', 'mysite.polls.views.vote'),

)
