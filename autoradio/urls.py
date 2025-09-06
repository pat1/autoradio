from django.conf.urls import *
from . import settings
from django.conf.urls.static import static
from django.urls import re_path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles import views

urlpatterns = [
    # Example:
    # (r'^autoradio/', include('autoradio.foo.urls')),

#    (r'^xmms/', include('programs.urls')),
#    (r'^$', include('spots.urls')),
#    (r'^$', include('jingles.urls')),

#    Uncomment the next line to enable admin documentation:
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^', include('autoradio.programs.urls')),
#    re_path(r'^', include('autoradio.palimpsest.urls')),
    re_path(r'^podcasts/', include('autoradio.programs.urls_podcast')),
    re_path(r'^player/', include('autoradio.player.urls')),
    re_path(r'^doc/', include('autoradio.doc.urls')),
]

if ( settings.SERVE_STATIC ):
    #serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
