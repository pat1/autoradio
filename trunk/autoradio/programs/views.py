# Create your views here.

from django.shortcuts import render_to_response
from models import Schedule
from django.http import HttpResponse
from datetime import datetime
import autoradio.autoradio_config
import autoradio.autoradio_core
import autoradio.settings

#def index_old(request):
#    latest_schedule_list = Schedule.objects.filter(emission_date__gte=datetime.now()).order_by('emission_date')[:5]
#    latest_schedule_done = Schedule.objects.filter(emission_date__lt=datetime.now()).order_by('emission_date')[:5]
#    return render_to_response('schedule/index.html', {'latest_schedule_done': latest_schedule_done , 'latest_schedule_list': latest_schedule_list})
#
#def detail(request, schedule_id):
#    return HttpResponse("You're looking at %s." % schedule_id)


def index(request):


    scheds=autoradio.autoradio_core.schedules([])

    return render_to_response('schedule/index.html', {'schedule': scheds.get_all_refine(genfile=False),'media_url':autoradio.settings.MEDIA_URL })


def stato(request):
    import urllib2
        
    xmmsweb=""
    try:
        url=urllib2.urlopen("http://"+autoradio.autoradio_config.XMMSHOST+":8888/")
        for line in url:
            xmmsweb=xmmsweb+line
    except:
        xmmsweb="<p>Error getting player status !!</p>"
        xmmsweb=xmmsweb+"<p>Start autoradiod or verify settings</p>"

    return render_to_response('xmms/index.html', {'xmmsweb': xmmsweb,'media_url':autoradio.settings.MEDIA_URL })

