from django.conf.urls.defaults import *


urlpatterns = patterns('autoradio.player.views',

    # Episode detail of one show
    url(r'^(?P<media>(.*))', view='playercmd'),

)
