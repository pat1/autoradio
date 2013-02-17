# Create your views here.

from django.shortcuts import render_to_response
from models import Schedule
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime,timedelta,time
import autoradio.autoradio_config
import autoradio.autoradio_core
import autoradio.settings
import autoradio.autompris2
import os

#from django.forms.extras.widgets import SelectDateWidget
from widgets import MySelectDateWidget
from django.utils.translation import ugettext_lazy

#----------------------------------------------------
# section for programs

#def index_old(request):
#    latesst_schedule_list = Schedule.objects.filter(emission_date__gte=datetime.now()).order_by('emission_date')[:5]
#    latest_schedule_done = Schedule.objects.filter(emission_date__lt=datetime.now()).order_by('emission_date')[:5]
#    return render_to_response('schedule/index.html', {'latest_schedule_done': latest_schedule_done , 'latest_schedule_list': latest_schedule_list})
#
#def detail(request, schedule_id):
#    return HttpResponse("You're looking at %s." % schedule_id)


def index(request):


    scheds=autoradio.autoradio_core.schedules([])

    return render_to_response('schedule/index.html', {'schedule': scheds.get_all_refine(genfile=False),'site_media_url':autoradio.settings.SITE_MEDIA_URL})


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

    return render_to_response('xmms/index.html', {'xmmsweb': xmmsweb,'site_media_url':autoradio.settings.SITE_MEDIA_URL })


def dbusstato(request):
        
    maxplele=100
    player = autoradio.autoradio_config.player
    htmlresponse=""

    if  player == "vlc" or player == "AutoPlayer":
        try:
            mp= autoradio.autompris2.mediaplayer(player=player,session=0)
        except:
            htmlresponse +="<p>Error getting player status !!</p>"
            htmlresponse +=htmlresponse+"<p>Start autoradiod or verify settings</p>"
            return render_to_response('xmms/index.html', {'xmmsweb': htmlresponse,'site_media_url':autoradio.settings.SITE_MEDIA_URL })
    else:
        return stato(request)
        #htmlresponse += "Invalid player for dbus interface"

    cpos=mp.get_playlist_pos()
    if cpos is None: cpos=0
    cpos=int(cpos)
    isplaying= mp.isplaying()

    len=mp.get_playlist_len()
    htmlresponse+='<p>player have %i songs in playlist // song number %i selected</p>' % (len,cpos+1)
    htmlresponse+='<table border="1">'
    htmlresponse+='<td>position</td><td>lenght // remain</td><td>media</td>'

    for pos in xrange(0,min(len,maxplele)):
        htmlresponse+='<tr>'
        metadata=mp.get_metadata(pos)

        timelength=timedelta(seconds=timedelta(milliseconds=metadata["mtimelength"]).seconds)
        timeposition=timedelta(seconds=timedelta(milliseconds=metadata["mtimeposition"]).seconds)

        if pos == cpos and isplaying:
            col="#FF0000"
            toend=timelength-timeposition
        elif  pos < cpos :
            col="#0000FF"
            toend=""
        else:
            col="#00FF00"
            toend=""

        if (metadata["artist"] is not None) or (metadata["title"] is not None):
            htmlresponse+='<td bgcolor="%s">%i</td><td> %s // %s </td><td><a href="%s">%s // %s</a></td>' % \
                (col,pos+1,str(timelength),str(toend),metadata["file"],metadata["artist"],metadata["title"])
        else:
            purefilename=os.path.splitext(metadata["file"])[0]
            htmlresponse+='<td bgcolor="%s">%i</td><td> %s // %s </td><td><a href="%s">%s</a></td>' % \
                (col,pos+1,str(timelength),str(toend),metadata["file"],os.path.basename(purefilename))


        htmlresponse+='</tr>'

    htmlresponse+='</table>'

    if len > maxplele :
        htmlresponse+="<p>ATTENTION: there are more file than you can see here.</p>"

    return render_to_response('xmms/index.html', {'xmmsweb': htmlresponse,'site_media_url':autoradio.settings.SITE_MEDIA_URL })



#----------------------------------------------------
# section for palimpsest

from django import forms
from reportlab.platypus import *


def decode(code):
    car=""
    digit=""
    for i in range(len(code)):

        if code[i-1].isdigit():
            digit+=code[i-1]
        else:
            car+=code[i-1]

    if len(car) > 0 :
        car=digit+car

    return digit,car


class ExtremeForm(forms.Form):

    initial_start=date.today()-timedelta(days=10)
    initial_end=date.today()

#    datetime_start = forms.DateTimeField(required=True,initial=initial_start,widget=SelectDateWidget(years=(2010,etc)))
#    datetime_end = forms.DateTimeField(required=True,initial=initial_end,widget=SelectDateWidget(years=(2010,etc)))
    datetime_start = forms.DateTimeField(required=True,initial=initial_start,widget=MySelectDateWidget(),label=ugettext_lazy("Starting date & time"),help_text=ugettext_lazy("Elaborate palimpsest starting from this date and time"))

    datetime_end = forms.DateTimeField(required=True,initial=initial_end,widget=MySelectDateWidget(),label=ugettext_lazy("Ending date & time"),help_text=ugettext_lazy("Elaborate palimpsest ending to this date and time"))

def programsbook(request):

    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import inch
    from reportlab.lib import colors


    if request.method == 'POST': # If the form has been submitted...
        form = ExtremeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass

            def myPages(canvas, doc):
                pageinfo="Libro Programmi"
                canvas.saveState()
                canvas.setFont('Times-Roman',9)
                canvas.drawString(inch, 0.75 * inch, "Pagina %d               %s" % (doc.page, pageinfo))
                canvas.restoreState()

            # time constants
            now=datetime.now()
            minelab=1


            datetime_start=form.cleaned_data['datetime_start']
            datetime_end=form.cleaned_data['datetime_end']

            datetime_start = datetime.combine(datetime_start.date(),time(00))
            datetime_end = datetime.combine(datetime_end.date(),time(23,59))

            #datetime_start=(now-timedelta(days=4))
            #datetime_end=now

            pro=autoradio.gest_palimpsest.gest_palimpsest(now,minelab)

            emittente,canale,mezzo,trasmissione=pro.get_info()

            author = "Autoradio Radio Automation Free Software"

            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(mimetype='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'


            PAGE_HEIGHT=defaultPageSize[1]
            styles = getSampleStyleSheet()

            MezzoTrasmissione=Paragraph("Mezzo di diffusione: "+mezzo+
                                        "  //   Tipo di trasmissione: "+trasmissione, styles["Normal"])
            EmittenteCanale=Paragraph("Denominazione dell'emittente: "+emittente+
                                      "  //   Denominazione del canale: "+canale, styles["Normal"])
            Space=Spacer(inch, 0.25 * inch)

            # First the top row, with all the text centered and in Times-Bold,
            # and one line above, one line below.
            ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
                  ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
                  ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
                  ('FONT', (0,0), (-1,0), 'Times-Bold'),

                  # The bottom row has one line above, and three lines below of
                  # various colors and spacing.
                  #('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),
                  #('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple,
                  # 1, None, None, 4,1),
                  ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
                  ('FONT', (0,-1), (-1,-1), 'Times-Bold'),
                  ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                  ('BOX', (0,0), (-1,-1), 0.25, colors.black)]

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            #p.drawString(100, 100, "Hello world.")

            dati=[["data",
                   Paragraph("titolo programma", styles["Normal"]),
                   Paragraph("ora inizio", styles["Normal"]),
                   Paragraph("ora fine", styles["Normal"]),
                   "tipologia","dettagli","produzione","note"]]


            pali=autoradio.autoradio_core.palimpsests([])

            for title,pdatetime_start,pdatetime_end,code,type,subtype,production,note in pali.get_palimpsest(datetime_start,datetime_end):

                # if you want extensive text comment this line
                type,subtype=decode(code)

                dati.append([str(pdatetime_start.date()),Paragraph(title, styles["Normal"]),
                             pdatetime_start.time().strftime("%H:%M"),pdatetime_end.time().strftime("%H:%M"),
                             Paragraph(type, styles["Normal"]),Paragraph(subtype, styles["Normal"]),production,note])


            #dati.append(["totale","fine"])

            Tabella=Table(dati,style=ts,repeatRows=1)

            Elements = [MezzoTrasmissione,EmittenteCanale,Space,Tabella]

            # Create the PDF object, using the response object as its "file."
            p = SimpleDocTemplate(response,title="Libro programmi: "+emittente,author=author)
            p.build(Elements, onFirstPage=myPages, onLaterPages=myPages)


            return response


    else:
        form = ExtremeForm() # An unbound form

    return render_to_response('palimpsest/extreme.html', {
        'form': form,'site_media_url':autoradio.settings.SITE_MEDIA_URL
    })


#----------------------------------------------------
# section for podcast

from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from autoradio.programs.models import Episode, Show, Enclosure
from django.core.urlresolvers import reverse


def episode_detail(request, show_slug, episode_slug):
    """
    Episode detail

    Template:  ``podcast/episode_detail.html``
    Context:
        object_detail
            Detail of episode.
    """
    return object_detail(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=show_slug),
        slug=episode_slug,
        slug_field='slug',
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=show_slug).filter(episode__slug__exact=episode_slug).order_by('-episode__date'),'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/episode_detail.html')


def episode_list(request, slug):
    """
    Episode list

    Template:  ``podcast/episode_list.html``
    Context:
        object_list
            List of episodes.
    """
#    return object_list(
#        request,
#        queryset=Episode.objects.published().filter(show__slug__exact=slug),
#        extra_context={'site_media_url':autoradio.settings.SITE_MEDIA_URL},
#        template_name='podcast/episode_list.html')

# from: http://code.google.com/p/django-podcast/issues/detail?id=12

    try:
        show = Show.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(reverse('podcast_shows'))

    context = {'show':show, 'site_media_url':autoradio.settings.SITE_MEDIA_URL}
    return object_list(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=slug),
        template_name='podcast/episode_list.html',
        extra_context = context)


def episode_sitemap(request, slug):
    """
    Episode sitemap

    Template:  ``podcast/episode_sitemap.html``
    Context:
        object_list
            List of episodes.
    """
    return object_list(
        request,
        mimetype='application/xml',
        queryset=Episode.objects.published().filter(show__slug__exact=slug).order_by('-date'),
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/episode_sitemap.html')


def show_list(request):
    """
    Episode list

    Template:  ``podcast/show_list.html``
    Context:
        object_list
            List of shows.
    """
    return object_list(
        request,
        queryset=Show.objects.all().order_by('title'),
        extra_context={'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/show_list.html')


def show_list_feed(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/show_feed.html')


def show_list_media(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_media.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/show_feed_media.html')


def show_list_atom(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_atom.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'site_media_url':autoradio.settings.SITE_MEDIA_URL},
        template_name='podcast/show_feed_atom.html')



