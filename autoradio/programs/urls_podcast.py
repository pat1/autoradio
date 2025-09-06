from django.conf.urls import *
#from django.contrib import admin
from django.urls import re_path

#from models import Program, Schedule

from .views import show_list, episode_list, show_list_feed, show_list_atom, show_list_media, episode_sitemap, episode_detail


urlpatterns = [
    # Show list of all shows
    re_path(r'^$', view=show_list.as_view(), name='podcast_shows'),

    # Episode list of one show
    re_path(r'^(?P<slug>[-\w]+)/$', view=episode_list.as_view(), name='podcast_episodes'),

    # Episode list feed by show (RSS 2.0 and iTunes)
    re_path(r'^(?P<slug>[-\w]+)/feed/$', view=show_list_feed.as_view(), name='podcast_feed'),

    # Episode list feed by show (Atom)
    re_path(r'^(?P<slug>[-\w]+)/atom/$', view=show_list_atom.as_view(), name='podcast_atom'),
    
    # Episode list feed by show (Media RSS)
    re_path(r'^(?P<slug>[-\w]+)/media/$', view=show_list_media.as_view(), name='podcast_media'),

    # Episode sitemap list of one show
    re_path(r'^(?P<slug>[-\w]+)/sitemap.xml$', view=episode_sitemap.as_view(), name='podcast_sitemap'),

    # Episode detail of one show
    re_path(r'^(?P<show_slug>[-\w]+)/(?P<slug>[-\w]+)/$', view=episode_detail.as_view(), name='podcast_episode'),

]
