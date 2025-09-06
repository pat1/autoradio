from django.conf.urls import *
#from django.contrib import admin
from django.urls import re_path

#from models import Program, Schedule
from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^xmms/$', views.dbusstato),
    re_path(r'^programsbook/$', views.programsbook),
]

