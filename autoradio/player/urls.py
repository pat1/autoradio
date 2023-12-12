from django.conf.urls import *
from . import views

urlpatterns = [
    # Episode detail of one show
    url(r'^nohtml5/(?P<media>(.*))', views.playernohtml5cmd),
    url(r'^(?P<media>(.*))', views.playercmd),

]
