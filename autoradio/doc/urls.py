from django.conf.urls import *
from django.urls import re_path
#from django.views.generic.simple import direct_to_template
#from django.conf.urls import patterns
from django.views.generic import TemplateView

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name="doc/index.html")),
    re_path(r'^(?P<docitem>\w+)/$', TemplateView.as_view(template_name="doc/doc.html")),
]

#urlpatterns = patterns('autoradio.doc.views',
#    (r'^$', direct_to_template , {'template' : 'doc/index.html'}),
#    (r'^(?P<docitem>\w+)/$', direct_to_template , {'template' : 'doc/doc.html'}),
#)
