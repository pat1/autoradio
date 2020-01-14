#!/usr/bin/env python
# coding=utf-8

"""
Show xmms playlist on a simple web server.
"""

from builtins import str
from builtins import range
from builtins import object
session=0         # sessione di xmms
maxplele=100      # massimo numero di elementi della playlist
iht=False         # emetti header e tail
port=8888         # port for server

#try:
#    import sys,glob
#    from distutils.sysconfig import get_python_lib
#    compatCherryPyPath = glob.glob( get_python_lib()+"/CherryPy-2.*").pop()
#    sys.path.insert(0, compatCherryPyPath)
#finally:

import cherrypy
cpversion3=cherrypy.__version__.startswith("3")

import xmms
import datetime

head='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Language" content="it-it" />

		<title>XMMS monitor | </title>

		<meta name="ROBOTS" content="ALL" />
		<meta http-equiv="imagetoolbar" content="no" />

		<meta name="MSSmartTagsPreventParsing" content="true" />
		<meta name="Copyright" content="This site's design and contents Copyright (c) 2007 Patruno Paolo." />

		<meta name="keywords" content="Python, xmms" />
		<meta name="description" content="xmms web monitor" />

		<meta http-equiv="refresh" content="10">

      
	</head>
<body>
'''

tail='''
</body>
</html>
'''

class HomePage(object):
    
#    def Main(self):
#        # Let's link to another method here.
#        htmlresponse='Goto xmms <a href="status">status</a> for autoradio!<BR>'
#        htmlresponse+='Goto xmms <a href="playList">playlist</a> for autoradio!<BR>'
#        return htmlresponse
#    Main.exposed = True
    
    def test(self):
        "return test page"
        return "Test Page"
            
    test.exposed = True

    def status(self):
        "return xmms status"

        ok=xmms.control.is_playing(0)
        if ok:
            return "xmms is playing"
        else:
            return "xmms is stopped"
            
    status.exposed = True

    def index(self):
        "return xmms playlist"
        if (iht) :
            htmlresponse=head
        else:
            htmlresponse=""
    
        try:
            cpos=xmms.control.get_playlist_pos(session)
            ok=True

        except:
            return "error xmms.control.get_playlist_pos"

        try:
            isplaying= xmms.control.is_playing(session)

        except:
            return "error xmms.control.is_playing"

        try:
            len=xmms.control.get_playlist_length(session)
            htmlresponse+='<p>xmms ha %i brani in playlist // selezionato brano numero %i</p>' % (len,cpos+1)
            htmlresponse+='<table border="1">'
            htmlresponse+='<td>posizione</td><td>durata</td><td>brano</td>'

            for pos in range(0,min(len,maxplele)):
                htmlresponse+='<tr>'
                file=xmms.control.get_playlist_file(pos, session)
                title=xmms.control.get_playlist_title(pos, session)
                time=datetime.timedelta(seconds=datetime.timedelta(milliseconds=xmms.control.get_playlist_time(pos, session)).seconds)

                if pos == cpos and isplaying:
                    col="#FF0000"
                    toend=time-datetime.timedelta(seconds=datetime.timedelta(milliseconds=xmms.control.get_output_time(session)).seconds)
                elif  pos < cpos :
                    col="#0000FF"
                    toend=None
                else:
                    col="#00FF00"
                    toend=None

                htmlresponse+='<td bgcolor="%s">%i</td><td> %s // %s </td><td><a href="file:%s">%s</a></td>' % (col,pos+1,str(time),str(toend),file,title)
                htmlresponse+='</tr>'

        except:
            htmlresponse+='error xmms.control.get_playlist_length'

        htmlresponse+='</table>'
        if len > maxplele :
            htmlresponse+="<p>ATTENZIONE: ci sono molti elementi nella playlist e gli ultimi non sono visualizzati</p>"

        if (iht) :
            htmlresponse+=tail
        return htmlresponse
            
    index.exposed = True



def start_http_server():
    #import os
    #pid = os.fork()
    settings = { 
        'global': {
            'server.socket_port' : port,
            'server.socket_host': "",
            'server.socket_file': "",
            'server.socket_queue_size': 5,
            'server.protocol_version': "HTTP/1.0",
            'server.log_to_screen': False,
            'server.log_file': "/tmp/xmmsweb.log",
            'server.reverse_dns': False,
            'server.thread_pool': 10,
            #            'server.environment': "development"
            'server.environment': "production"
            },
        }


# CherryPy always starts with cherrypy.root when trying to map request URIs
# to objects, so we need to mount a request handler object here. A request
# to '/' will be mapped to cherrypy.root.index().

    if (cpversion3):
        cherrypy.quickstart(HomePage(),config=settings)

    else:
        cherrypy.config.update(settings)
        cherrypy.root = HomePage()
        cherrypy.server.start()


if __name__ == '__main__':

    # Set the signal handler
    #import signal
    #signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start the CherryPy server.
    start_http_server()

