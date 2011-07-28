from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.http import Http404

def index(request):
    return direct_to_template(request, 'doc/index.html')

def doc_reader(request, docname):
    return direct_to_template(request, 'doc/doc.html', dict(doc=docname))
