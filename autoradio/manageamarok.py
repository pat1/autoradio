#!/usr/bin/env python
# GPL. (C) 2007 Paolo Patruno.

from builtins import str
from builtins import object
import logging
from qt import *
import dcopext
from kdecore import *
from datetime import *
from threading import *


def ar_emitted(self):
    self.emission_done=datetime.now()
    self.save()


def KdeInit():
    "inizializzo kde"
        
    aboutdata = KAboutData("AutoAmarok","Autoamarok","1.0",
                           "Amarok radio station",
                           KAboutData.License_GPL,
                           "Copyright (C) 2007 Paolo Patruno")    
    KCmdLineArgs.init(aboutdata)
    return KApplication ()

class Kde(object):

    def __init__ (self,kapp):
        "init of kde application"
        
        self.dcopclient = kapp.dcopClient()

    def connect(self,application):
        "connetto with kde application"

        self.dcopapplication = dcopext.DCOPApp(application, self.dcopclient)

class ScheduleProgram(object):

    def __init__ (self,kapp,function,operation,media,scheduledatetime,programma):
        "init schedule"
        
        self.kapp=kapp
        self.function=function
        self.operation=operation
        self.media=media
        self.scheduledatetime=scheduledatetime
        self.programma=programma

        scheduledatetime
        #print "differenza ",datetime.now(),self.scheduledatetime
        delta=( self.scheduledatetime - datetime.now())
        #print delta

        #self.deltasec=max(secondi(delta),1)
        self.deltasec=secondi(delta)
        self.deltasec
        self.timer = Timer(self.deltasec, self.function,
                      [self.kapp,self.operation,self.media,self.programma])

    def start (self):
        "start of programmed schedule"
        
        #self.function (self.kde,self.media)
        self.timer.start()

def ManageAmarok (kapp,operation,media,programma):
    "Manage amarok to do operation on media"
    
    kde=Kde(kapp)
    kde.connect("amarok")

    logging.info( "kde operation: %s",operation)
    if ( operation == "queueMedia"):
#        ok,result = kde.dcopapplication.playlist.adjustDynamicPrevious()
#        print "kde.dcopapplication.playlist.adjustDynamicPrevious"
#        print 'status is:',ok,result

        ok,result = kde.dcopapplication.playlist.queueMedia(KURL(media))
        logging.info( "kde.dcopapplication.playlist.queueMedia %s",media)
        test_status(ok,result)

        ok,result = kde.dcopapplication.player.isPlaying()
        logging.info( "kde.dcopapplication.player.isPlaying")
        test_status(ok,result)

        if ( not result):
            ok,result = kde.dcopapplication.player.play()
            logging.info ("kde.dcopapplication.player.play")
            test_status(ok,result)

    elif (operation == "loadPlaylist"):
        ok,result = kde.dcopapplication.playlistbrowser.loadPlaylist(QString(media))
        logging.info( "kde.dcopapplication.playlistbrowser.loadPlaylist %s",media)
        test_status(ok,result)

        ok,result = kde.dcopapplication.playlist.repopulate()
        logging.info( "kde.dcopapplication.playlistbrowser.repopulate")
        test_status(ok,result)

        ok,result = kde.dcopapplication.player.isPlaying()
        logging.info( "kde.dcopapplication.player.isPlaying")
        test_status(ok,result)

        if ( not result):
            ok,result = kde.dcopapplication.player.play()
            logging.info( "kde.dcopapplication.player.play")
            test_status(ok,result)



    if (ok):
        logging.info( "scrivo in django: %s",programma)
        ar_emitted(programma)
        logging.info( "scritto in django: %s",programma)

def secondi(delta):
    secondi=delta.seconds
    # correggo i viaggi che si fa seconds
    if delta.days < 0 :
        secondi = secondi + (3600*24*delta.days)
    return secondi



class dummy_programma(object):

    def __init__(self):
        pass
    
    def save(self):
        pass
        #print "faccio finta di salvarlo"
    

def amarok_watchdog(kapp):

    try:
        kde=Kde(kapp)
        kde.connect("amarok")

        ok,result = kde.dcopapplication.playlist.getTotalTrackCount()
        logging.info( "kde.dcopapplication.playlist.getTotalTrackCount")
    except:
        ok=False
        result="error on kde.dcopapplication.playlist.getTotalTrackCount()"

    test_status(ok,result)

    if (result > 40 or result < 5 ):
        logging.error("Ho trovato troppa (poca) roba in playlist ! ci sono %s tracce",result)

        ok,result = kde.dcopapplication.playlist.saveM3u(QString("/tmp/autoradio.m3u"), False)
        logging.info( "kde.dcopapplication.playlist.saveM3u")
        test_status(ok,result)

        ok,result = kde.dcopapplication.playlist.repopulate()
        logging.info( "kde.dcopapplication.playlist.repopulate")
        test_status(ok,result)

    return ok


def save_status(kapp):

    kde=Kde(kapp)
    kde.connect("amarok")
    ok,result = kde.dcopapplication.playlist.saveCurrentPlaylist()
    logging.info ( "kde.dcopapplication.playlist.saveCurrentPlaylist")
    test_status(ok,result)
    return ok

def test_status( ok,result):

#    print ok,result
    if (ok == True):
        logging.info( "status is: %s result: %s",ok,str(result))
    else:
        logging.error( "status is: %s result: %s",ok,str(result))


def main():

    kapp=KdeInit()

    programma=dummy_programma()
        
    function=ManageAmarok
    operation="queueMedia"
    media = "/home/pat1/Musica/mp3/goran_bregovic/ederlezi/talijanska.mp3"
    #media = raw_input("dammi il media? ")
    scheduledatetime=datetime.now()+timedelta(seconds=15)
    schedule=ScheduleProgram(kapp,function,operation,media,scheduledatetime,programma)
    schedule.start()

    scheduledatetime=datetime.now()+timedelta(seconds=30)
    media = "/home/pat1/Musica/mp3/goran_bregovic/ederlezi/underground_tango.mp3"
    schedule=ScheduleProgram(kapp,function,operation,media,scheduledatetime,programma)
    schedule.start()

    scheduledatetime=datetime.now()+timedelta(seconds=45)
    media = "/home/pat1/Musica/mp3/goran_bregovic/ederlezi/lullabye.mp3"
    schedule=ScheduleProgram(kapp,function,operation,media,scheduledatetime,programma)
    schedule.start()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
