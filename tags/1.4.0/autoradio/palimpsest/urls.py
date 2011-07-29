from django.conf.urls.defaults import *

#from models import Program, Schedule

urlpatterns = patterns('',
    (r'^programsbook/$', 'autoradio.palimpsest.views.programsbook'),

)


