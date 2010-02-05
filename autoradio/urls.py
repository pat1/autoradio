from django.conf.urls.defaults import *
import settings

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
    (r'^'+settings.MEDIA_ROOT+'sito/(.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_SITE_ROOT, 'show_indexes': True}),
    (r'^'+settings.MEDIA_ROOT+'(.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^', include('autoradio.programs.urls')),
    (r'^', include('autoradio.palimpsest.urls')),
    (r'^podcasts/', include('autoradio.podcast.urls')),
    (r'^player/', include('autoradio.player.urls')),
)
