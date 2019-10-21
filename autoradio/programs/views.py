from __future__ import absolute_import
# Create your views here.

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from django.shortcuts import render_to_response
from .models import Schedule
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime,timedelta,time
import autoradio.autoradio_config
import autoradio.autoradio_core
import autoradio.settings
import autoradio.autompris2
import os

#from django.forms.extras.widgets import SelectDateWidget
from .widgets import MySelectDateWidget
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

    scheds.get_all_refine(genfile=False)
    #print ("s=",scheds)
    #for ss in scheds:
    #    ss
    #    print ("ss=",ss)
    #    for sss in ss:
    #        print ("sss=",sss)
    return render_to_response('schedule/index.html', {'schedules': scheds})


def stato(request):
    import urllib.request, urllib.error, urllib.parse
        
    xmmsweb=""
    try:
        url=urllib.request.urlopen("http://"+autoradio.autoradio_config.XMMSHOST+":8888/")
        for line in url:
            xmmsweb=xmmsweb+line
    except:
        xmmsweb="<p>Error getting player status !!</p>"
        xmmsweb=xmmsweb+"<p>Start autoradiod or verify settings</p>"

    return render_to_response('xmms/index.html', {'xmmsweb': xmmsweb,})


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
            return render_to_response('xmms/index.html', {'xmmsweb': htmlresponse,})
    else:
        return stato(request)
        #htmlresponse += "Invalid player for dbus interface"

    try:

        cpos=mp.get_playlist_pos()
        if cpos is None: cpos=0
        cpos=int(cpos)
        isplaying= mp.isplaying()

        len=mp.get_playlist_len()
        htmlresponse+='<p>player have %i songs in playlist // song number %i selected</p>' % (len,cpos+1)
        htmlresponse+='<table border="1">'
        htmlresponse+='<td>position</td><td>lenght // remain</td><td>media</td>'

        for pos in range(0,min(len,maxplele)):
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

    except:
        htmlresponse +="<p>Error getting player status !!</p>"
        htmlresponse +=htmlresponse+"<p>Start autoradiod or verify settings</p>"
        
    del mp
    return render_to_response('xmms/index.html', {'xmmsweb': htmlresponse,})



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
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'


            PAGE_HEIGHT=defaultPageSize[1]
            styles = getSampleStyleSheet()

            MezzoTrasmissione=Paragraph("Mezzo di diffusione: "+str(mezzo)+
                                        "  //   Tipo di trasmissione: "+str(trasmissione), styles["Normal"])
            EmittenteCanale=Paragraph("Denominazione dell'emittente: "+str(emittente)+
                                      "  //   Denominazione del canale: "+str(canale), styles["Normal"])
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
            p = SimpleDocTemplate(response,title="Libro programmi: "+str(emittente),author=author)
            p.build(Elements, onFirstPage=myPages, onLaterPages=myPages)


            return response


    else:
        form = ExtremeForm() # An unbound form

    return render_to_response('palimpsest/extreme.html', {
        'form': form})


#----------------------------------------------------
# section for podcast
from django.views.generic.list  import ListView
from django.views.generic.detail import DetailView
#from django.views.generic.list_detail import object_list
from autoradio.programs.models import Episode, Show, Enclosure
from django.urls import reverse

class episode_detail(DetailView):
#class episode_detail(ListView):
    """
    Episode detail

    Template:  ``podcast/episode_detail.html``
    Context:
        object_detail
            Detail of episode.
    """

    template_name='podcast/episode_detail.html'
    date_field = "date"

    def get_context_data(self, **kwargs):
        context = super(episode_detail, self).get_context_data(**kwargs)
        extra_context={
        'enclosure_list': Enclosure.objects.filter
        (episode__show__slug__exact=self.show_slug).filter(episode__slug__exact=self.episode_slug).order_by('-episode__date'),}
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.show_slug = kwargs.get('show_slug')
        self.episode_slug = kwargs.get('slug')
        self.queryset=Episode.objects.published().filter(show__slug__exact=self.show_slug)
        return super(episode_detail, self).get(request, *args, **kwargs)



class episode_list(ListView):

# Qui slug e' passato ma non si sa come !!!!!
#, slug):
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

    template_name='podcast/episode_list.html'

    def get_context_data(self, **kwargs):
        context = super(episode_list, self).get_context_data(**kwargs)

# todo da implementare questo try nel passaggio a django 1.5
#        try:
        show = Show.objects.get(slug=self.slug)
#        except:
#           return HttpResponseRedirect(reverse('podcast_shows'))

        extra_context = {'show':show,}
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')

        self.queryset=Episode.objects.published().filter(show__slug__exact=self.slug)
        return super(episode_list, self).get(request, *args, **kwargs)


class episode_sitemap(ListView):
    """
    Episode sitemap

    Template:  ``podcast/episode_sitemap.html``
    Context:
        object_list
            List of episodes.
    """

    template_name='podcast/episode_sitemap.html'

    def get_context_data(self, **kwargs):
        context = super(episode_sitemap, self).get_context_data(**kwargs)
        extra_context={
            'enclosure_list': Enclosure.objects.filter
            (episode__show__slug__exact=self.slug).order_by('-episode__date'),},
        context.update(extra_context)
        return context


    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.queryset=Episode.objects.published().filter(show__slug__exact=self.slug).order_by('-date')
        return super(episode_sitemap, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        return super(episode_sitemap, self).render_to_response(context,
                        content_type='application/xml', **kwargs)


class show_list(ListView):
#def show_list(request):
    """
    Episode list

    Template:  ``podcast/show_list.html``
    Context:
        object_list
            List of shows.
    """

    queryset=Show.objects.all().order_by('title')
    template_name='podcast/show_list.html'

    def get_context_data(self, **kwargs):
        context = super(show_list, self).get_context_data(**kwargs)
        context.update()
        return context


class show_list_feed(ListView):
    """
    Episode feed by show

    Template:  ``podcast/show_feed.html``
    Context:
        object_list
            List of episodes by show.
    """

    template_name='podcast/show_feed.html'

    def get_context_data(self, **kwargs):
        context = super(show_list_feed, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        self.queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21]
        return super(show_list_feed, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        return super(show_list_feed, self).render_to_response(context,
                        content_type='application/xml', **kwargs)



class show_list_media(ListView):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_media.html``
    Context:
        object_list
            List of episodes by show.
    """

    template_name='podcast/show_feed_media.html'

    def get_context_data(self, **kwargs):
        context = super(show_list_media, self).get_context_data(**kwargs)
        extra_context={
            'enclosure_list': Enclosure.objects.filter
            (episode__show__slug__exact=self.slug).order_by('-episode__date')}
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.queryset=Episode.objects.filter(show__slug__exact=self.slug).order_by('-date')[0:21]
        return super(show_list_media, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        return super(show_list_media, self).render_to_response(context,
                        content_type='application/xml', **kwargs)


class show_list_atom(ListView):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_atom.html``
    Context:
        object_list
            List of episodes by show.
    """

    template_name='podcast/show_feed_atom.html'

    def get_context_data(self, **kwargs):
        context = super(show_list_atom, self).get_context_data(**kwargs)
        extra_context={
            'enclosure_list': Enclosure.objects.filter
            (episode__show__slug__exact=self.slug).order_by('-episode__date')}
        context.update(extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.queryset=Episode.objects.filter(show__slug__exact=self.slug).order_by('-date')[0:21]
        return super(show_list_atom, self).get(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        return super(show_list_atom, self).render_to_response(context,
                        content_type='application/xml', **kwargs)
