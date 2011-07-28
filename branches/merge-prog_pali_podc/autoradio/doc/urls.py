from django.conf.urls.defaults import *

urlpatterns = patterns('autoradio.doc.views',
    (r'^$', 'index'),
    (r'^([^/]*)/$', 'doc_reader'),
)
