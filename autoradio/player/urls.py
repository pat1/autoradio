from django.conf.urls import *
from . import views
from django.urls import re_path

urlpatterns = [
    # Episode detail of one show
    re_path(r'^nohtml5/(?P<media>(.*))', views.playernohtml5cmd),
    re_path(r'^(?P<media>(.*))', views.playercmd),

]
