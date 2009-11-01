from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime
import autoradio.autoradio_config
import autoradio.autoradio_core
from reportlab.platypus import *

import autoradio.gest_palimpsest

    
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

    # time constants
    now=datetime.now()
    minelab=1000

    pro=autoradio.gest_palimpsest.gest_palimpsest(now,minelab)

    emittente,canale,mezzo,trasmissione=pro.get_info()

    #emittente="L'informazione Nuova"
    #canale="Radio citta' Fujiko"
    #mezzo="analogico terrestre"
    #trasmissione="radiofonica"
    author = "Autoradio Radio Automation Free Software"

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'


    PAGE_HEIGHT=defaultPageSize[1]
    styles = getSampleStyleSheet()

    MezzoTrasmissione=Paragraph("Mezzo di diffusione: "+mezzo+"  //   Tipo di trasmissione: "+trasmissione, styles["Normal"])
    EmittenteCanale=Paragraph("Denominazione dell'emittente: "+emittente+"  //   Denominazione del canale: "+canale, styles["Normal"])
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

    dati=[["data","titolo programma","ora inizio","ora fine","tipologia","dettagli","produzione","note"]]


    pali=autoradio.autoradio_core.palimpsests([])

    for title,datetime_start,datetime_end,type,subtype,production,note in pali.get_palimpsest():
        dati.append([str(datetime_start.date()),Paragraph(title, styles["Normal"]),
                     datetime_start.time().strftime("%H:%M"),datetime_end.time().strftime("%H:%M"),
                     Paragraph(type, styles["Normal"]),Paragraph(subtype, styles["Normal"]),production,note])


    #dati.append(["totale","fine"])
        
    Tabella=Table(dati,style=ts,repeatRows=1)

    Elements = [MezzoTrasmissione,EmittenteCanale,Space,Tabella]

    # Create the PDF object, using the response object as its "file."
    p = SimpleDocTemplate(response,title="Libro programmi: "+emittente,author=author)
    p.build(Elements, onFirstPage=myPages, onLaterPages=myPages)


    return response
