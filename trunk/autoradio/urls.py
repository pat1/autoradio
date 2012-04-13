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
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('autoradio.programs.urls')),
#    (r'^', include('autoradio.palimpsest.urls')),
    (r'^podcasts/', include('autoradio.programs.urls_podcast')),
    (r'^player/', include('autoradio.player.urls')),
    (r'^doc/', include('autoradio.doc.urls')),
)

if ( settings.SERVE_STATIC ):
#serve local static files
    urlpatterns += patterns('',
                            (r'^'+settings.MEDIA_PREFIX[1:]+'(.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            (r'^'+settings.MEDIA_SITE_PREFIX[1:]+'(.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_SITE_ROOT, 'show_indexes': True}),
                            )
