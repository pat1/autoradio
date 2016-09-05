from django.conf.urls import *
#from django.contrib import admin

#from models import Program, Schedule
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^xmms/$', views.dbusstato),
    url(r'^programsbook/$', views.programsbook),
]

