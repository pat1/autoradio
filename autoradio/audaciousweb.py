#!/usr/bin/env python
# coding=utf-8

"""
Show audacious playlist on a simple web server.
"""

session=0         # sessione di xmms
maxplele=100      # massimo numero di elementi della playlist
port=8888         # port for server

#try:
#    import sys,glob
#    from distutils.sysconfig import get_python_lib
#    compatCherryPyPath = glob.glob( get_python_lib()+"/CherryPy-2.*").pop()
#    sys.path.insert(0, compatCherryPyPath)
#finally:

import cherrypy
cpversion3=cherrypy.__version__.startswith("3")

import datetime

# ------- dbus interface ---------
import dbus

bus = dbus.SessionBus()

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

class HomePage:
    
#    def Main(self):
#        # Let's link to another method here.
#        htmlresponse='Goto xmms <a href="status">status</a> for autoradio!<BR>'
#        htmlresponse+='Goto xmms <a href="playList">playlist</a> for autoradio!<BR>'
#        return htmlresponse
#    Main.exposed = True
    

    def __init__(self,iht):
        self.iht=iht


    def test(self):
        "return test page"
        return "Test Page"
            
    test.exposed = True

    def status(self):
        "return xmms status"

        try:
            # ---------------------------------
            org_obj       = bus.get_object("org.atheme.audacious", '/org/atheme/audacious')
            org       = dbus.Interface(org_obj, dbus_interface='org.atheme.audacious')
            # ---------------------------------
        except:

            return "error intializing dbus"

        if (org.Playing()):
            return "audacious is playing"
        else:
            return "audacious is stopped"

            
    status.exposed = True

    def index(self):
        "return xmms playlist"


        if (self.iht) :
            htmlresponse=head
        else:
            htmlresponse=""


        try:
            # -----------------------------------------------------------
            root_obj      = bus.get_object("org.atheme.audacious", '/')
            player_obj    = bus.get_object("org.atheme.audacious", '/Player')
            tracklist_obj = bus.get_object("org.atheme.audacious", '/TrackList')
            org_obj       = bus.get_object("org.atheme.audacious", '/org/atheme/audacious')

            root      = dbus.Interface(root_obj,      dbus_interface='org.freedesktop.MediaPlayer')
            player    = dbus.Interface(player_obj,    dbus_interface='org.freedesktop.MediaPlayer')
            tracklist = dbus.Interface(tracklist_obj, dbus_interface='org.freedesktop.MediaPlayer')
            org       = dbus.Interface(org_obj, dbus_interface='org.atheme.audacious')
            # -----------------------------------------------------------
        except:

            return "error intializing dbus"

        try:
            cpos=int(tracklist.GetCurrentTrack())

        except:
            return "error tracklist.GetCurentTrack()"

        try:
            isplaying= org.Playing()

        except:
            return "error org.Playing()"

        try:
            len=tracklist.GetLength()
            htmlresponse+='<p>audacious ha %i brani in playlist // selezionato brano numero %i</p>' % (len,cpos+1)
            htmlresponse+='<table border="1">'
            htmlresponse+='<td>posizione</td><td>durata</td><td>brano</td>'

            for pos in xrange(0,min(len,maxplele)):
                htmlresponse+='<tr>'
                metadata=tracklist.GetMetadata(pos)

                try:
                    file=metadata["URI"]
                except:
                    file=None
                try:
                    title=metadata["title"]
                    if title=="":
                        title=None
                except:
                    title=None
                try:
                    mtimelength=metadata["length"]
                except:
                    mtimelength=None
                try:
                    mtimeposition=player.PositionGet()
                except:
                    mtimeposition=None

                timelength=datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimelength).seconds)
                timeposition=datetime.timedelta(seconds=datetime.timedelta(milliseconds=mtimeposition).seconds)

                if pos == cpos and isplaying:
                    col="#FF0000"
                    toend=timelength-timeposition
                elif  pos < cpos :
                    col="#0000FF"
                    toend=None
                else:
                    col="#00FF00"
                    toend=None

                htmlresponse+='<td bgcolor="%s">%i</td><td> %s // %s </td><td><a href="%s">%s</a></td>' % (col,pos+1,str(timelength),str(toend),file,title)
                htmlresponse+='</tr>'

        except:
            htmlresponse+='error get audacious information'
            raise

        htmlresponse+='</table>'
        if len > maxplele :
            htmlresponse+="<p>ATTENZIONE: ci sono molti elementi nella playlist e gli ultimi non sono visualizzati</p>"

        if (self.iht) :
            htmlresponse+=tail
        return htmlresponse
            
    index.exposed = True



def start_http_server(iht=False):
    """
    start web server to monitor audacious
    iht=False         # emetti header e tail
    """
    #import os
    #pid = os.fork()
    settings = { 
        'global': {
            'server.socket_port' : port,
            'server.socket_host': "0.0.0.0",
            'server.socket_file': "",
            'server.socket_queue_size': 5,
            'server.protocol_version': "HTTP/1.0",
            'server.log_to_screen': False,
            'server.log_file': "/tmp/xmmsweb.log",
            'server.reverse_dns': False,
            'server.thread_pool': 10,
            #'server.environment': "development"
            'server.environment': "production"
            },
        }


# CherryPy always starts with cherrypy.root when trying to map request URIs
# to objects, so we need to mount a request handler object here. A request
# to '/' will be mapped to cherrypy.root.index().

    if (cpversion3):
        cherrypy.quickstart(HomePage(iht),config=settings)

    else:
        cherrypy.config.update(settings)
        cherrypy.root = HomePage(iht)
        cherrypy.server.start()


if __name__ == '__main__':

    # Set the signal handler
    #import signal
    #signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start the CherryPy server.
    try:
        start_http_server(iht=True)
    except:
        print "Error"
        raise
    finally:
        print "Terminated"

