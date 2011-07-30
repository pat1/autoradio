from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('autoradio.doc.views',
    (r'^$', direct_to_template , {'template' : 'doc/index.html'}),
    (r'^(?P<docitem>\w+)/$', direct_to_template , {'template' : 'doc/doc.html'}),
)
