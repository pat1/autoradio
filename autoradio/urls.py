from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^autoradio/', include('autoradio.foo.urls')),

#    (r'^xmms/', include('programs.urls')),
#    (r'^$', include('spots.urls')),
#    (r'^$', include('jingles.urls')),

#    Uncomment the next line to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^django/media/sito/(.*)', 'django.views.static.serve', {'document_root': '/usr/share/autoradio/media/sito', 'show_indexes': True}),
    (r'^django/media/(.*)', 'django.views.static.serve', {'document_root': 'media', 'show_indexes': True}),
    (r'^', include('autoradio.programs.urls')),


)
