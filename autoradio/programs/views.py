# Create your views here.

from django.shortcuts import render_to_response
from models import Schedule
from django.http import HttpResponse
from datetime import datetime
import autoradio.autoradio_config
import autoradio.autoradio_core

#def index_old(request):
#    latest_schedule_list = Schedule.objects.filter(emission_date__gte=datetime.now()).order_by('emission_date')[:5]
#    latest_schedule_done = Schedule.objects.filter(emission_date__lt=datetime.now()).order_by('emission_date')[:5]
#    return render_to_response('schedule/index.html', {'latest_schedule_done': latest_schedule_done , 'latest_schedule_list': latest_schedule_list})
#
#def detail(request, schedule_id):
#    return HttpResponse("You're looking at %s." % schedule_id)


def index(request):


    scheds=autoradio.autoradio_core.schedules([])

    return render_to_response('schedule/index.html', {'schedule': scheds.get_all_refine(genfile=False)})


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

    return render_to_response('xmms/index.html', {'xmmsweb': xmmsweb})



from reportlab.platypus import *
    
def programsbook(request):

    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import inch
    from reportlab.lib import colors


    def myPages(canvas, doc):
        pageinfo="test page"
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
        canvas.restoreState()


    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'


    PAGE_HEIGHT=defaultPageSize[1]
    styles = getSampleStyleSheet()
    title = "Generating Reports with Python"
    Title = Paragraph(title, styles["Heading1"])
    author = "Brian K. Jones"
    Author = Paragraph(author, styles["Normal"])
    Abstract = Paragraph("""This is a simple example document that illustrates how to put together a basic PDF with a table.
I used the PLATYPUS library, which is part of ReportLab, and the capabilities built into ReportLab.""", styles["Normal"])
    # First the top row, with all the text centered and in Times-Bold,
    # and one line above, one line below.
    Space=Spacer(inch, 0.75 * inch)
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

    dati=[["data","nome","ora inizio","durata","tipo","dett.","note"]]
    scheds=autoradio.autoradio_core.schedules([])
  #  for sched in scheds.get_all_refine(genfile=False):
    for nome,datet,media,length,tipo,datetdone,future in scheds.get_all_refine(genfile=False):
        dati.append(["oggi",Paragraph(str(nome), styles["Normal"]),str(datetdone),length,tipo,"XX","ok"])

    #dati.append(["totale","fine"])
        
    Tabella=Table(dati,style=ts,repeatRows=1)

    Elements = [Abstract,Space,Tabella]

    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response,title=title,author=author)

    p.build(Elements, onFirstPage=myPages, onLaterPages=myPages)


    return response
