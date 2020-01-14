from __future__ import absolute_import
from django.conf.urls import *
#from django.contrib import admin

#from models import Program, Schedule
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^xmms/$', views.dbusstato),
    url(r'^programsbook/$', views.programsbook),
]

