#!/usr/bin/env python
# coding=utf-8

"""
Show mediaplayer playlist on a simple web server.
"""

#try:
#    import sys,glob
#    from distutils.sysconfig import get_python_lib
#    compatCherryPyPath = glob.glob( get_python_lib()+"/CherryPy-2.*").pop()
#    sys.path.insert(0, compatCherryPyPath)
#finally:

import autoradio_config
import cherrypy
import os
import datetime
import autompris
import autompris2

cpversion3=cherrypy.__version__.startswith("3")
maxplele=100      # max number of elements in playlist
port=8888         # server port

head='''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<meta http-equiv="Content-Language" content="it-it" />

		<title>MediaPlayer monitor | </title>

		<meta name="ROBOTS" content="ALL" />
		<meta http-equiv="imagetoolbar" content="no" />

		<meta name="MSSmartTagsPreventParsing" content="true" />
		<meta name="Copyright" content="This site's design and contents Copyright (c) 2007 Patruno Paolo." />

		<meta name="keywords" content="Python, Media Player" />
		<meta name="description" content="media player web monitor" />

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
#        htmlresponse='Goto player <a href="status">status</a> for autoradio!<BR>'
#        htmlresponse+='Goto player <a href="playList">playlist</a> for autoradio!<BR>'
#        return htmlresponse
#    Main.exposed = True


    def __init__(self,iht,player,session):
        self.iht=iht
        self.player=player
        self.session=session


    def test(self):
        "return test page"
        return "Test Page"
            
    test.exposed = True

#    def status(self):
#        "return media player status"
#
#        try:
#            # ---------------------------------
#            org_obj       = bus.get_object("org.atheme.audacious", '/org/atheme/audacious')
#            org       = dbus.Interface(org_obj, dbus_interface='org.atheme.audacious')
#            # ---------------------------------
#        except:
#
#            return "error intializing dbus"
#
#        if (org.Playing()):
#            return "player is playing"
#        else:
#            return "player is stopped"
#
#
#            
#    status.exposed = True

    def index(self):
        "return media player playlist"


        if (self.iht) :
            htmlresponse=head
        else:
            htmlresponse=""

        try:
            if  self.player == "vlc" or self.player == "AutoPlayer":
                mp= autompris2.mediaplayer(player=self.player,session=0)
            else:
                mp= autompris.mediaplayer(player=self.player,session=0)

        except:
            return "error intializing dbus"

        try:
            cpos=mp.get_playlist_pos()
	    if cpos is None: cpos=0
	    cpos=int(cpos)

        except:
            raise
            #return "error get_playlist_pos()"
	
        try:
            isplaying= mp.isplaying()

        except:
            return "error org.Playing()"

        try:
            len=mp.get_playlist_len()
            htmlresponse+='<p>player have %i songs in playlist // song number %i selected</p>' % (len,cpos+1)
            htmlresponse+='<table border="1">'
            htmlresponse+='<td>position</td><td>lenght // remain</td><td>media</td>'

            for pos in xrange(0,min(len,maxplele)):
                htmlresponse+='<tr>'
                metadata=mp.get_metadata(pos)

                timelength=datetime.timedelta(seconds=datetime.timedelta(milliseconds=metadata["mtimelength"]).seconds)
                timeposition=datetime.timedelta(seconds=datetime.timedelta(milliseconds=metadata["mtimeposition"]).seconds)

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

        except:
            htmlresponse+='error get player information'

        htmlresponse+='</table>'
        if len > maxplele :
            htmlresponse+="<p>ATTENTION: there are more file than you can see here.</p>"

        if (self.iht) :
            htmlresponse+=tail
        return htmlresponse
            
    index.exposed = True



def start_http_server(iht=False,player="AutoPlayer",session=0):
    """
    start web server to monitor player
    iht=False         # do not emit header e tail
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
            'server.log_file': "/tmp/mprisweb.log",
            'server.reverse_dns': False,
            'server.thread_pool': 10,
            'server.environment': "development",
            #'server.environment': "production",
            'tools.encode.on':True,
#            'tools.encode.encoding':'utf8',
            },
        }


# CherryPy always starts with cherrypy.root when trying to map request URIs
# to objects, so we need to mount a request handler object here. A request
# to '/' will be mapped to cherrypy.root.index().

    if (cpversion3):
        cherrypy.quickstart(HomePage(iht,player,session),config=settings)

    else:
        cherrypy.config.update(settings)
        cherrypy.root = HomePage(iht,player,session)
        cherrypy.server.start()


if __name__ == '__main__':

    # Set the signal handler
    #import signal
    #signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start the CherryPy server.
    try:
        start_http_server(iht=True,player=autoradio_config.player,session=0)

    except:
        print "Error"
        raise
    finally:
        print "Terminated"

