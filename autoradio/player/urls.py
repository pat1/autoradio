from django.conf.urls import *


urlpatterns = patterns('autoradio.player.views',

    # Episode detail of one show
    url(r'^nohtml5/(?P<media>(.*))', view='playernohtml5cmd'),
    url(r'^(?P<media>(.*))', view='playercmd'),

)
