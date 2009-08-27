# Create your views here.

from django.shortcuts import render_to_response
from programs.models import Schedule
from django.http import HttpResponse
from datetime import datetime
import autoradio_config
import autoradio_core

#def index_old(request):
#    latest_schedule_list = Schedule.objects.filter(emission_date__gte=datetime.now()).order_by('emission_date')[:5]
#    latest_schedule_done = Schedule.objects.filter(emission_date__lt=datetime.now()).order_by('emission_date')[:5]
#    return render_to_response('schedule/index.html', {'latest_schedule_done': latest_schedule_done , 'latest_schedule_list': latest_schedule_list})
#
#def detail(request, schedule_id):
#    return HttpResponse("You're looking at %s." % schedule_id)


def index(request):


    scheds=autoradio_core.schedules([])

    return render_to_response('schedule/index.html', {'schedule': scheds.get_all_refine(genfile=False)})


def stato(request):
    import urllib2
        
    xmmsweb=""
    url=urllib2.urlopen("http://"+autoradio_config.XMMSHOST+":8888/")
    for line in url:
        xmmsweb=xmmsweb+line

    return render_to_response('xmms/index.html', {'xmmsweb': xmmsweb})
