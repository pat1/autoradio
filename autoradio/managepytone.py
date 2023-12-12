from builtins import object
import os,sys
import events, network, requests, version, helper
from datetime import *
from threading import *



def ar_emitted(self):
    self.emission_done=datetime.now()
    self.save()


class ScheduleProgram(object):

    def __init__ (self,function,operation,media,scheduledatetime,programma):
        "init schedule"
        
        self.function=function
        self.operation=operation
        self.media=media
        self.scheduledatetime=scheduledatetime
        self.programma=programma

        scheduledatetime
        print("differenza ",datetime.now(),self.scheduledatetime)
        delta=( self.scheduledatetime - datetime.now())
        print(delta)

        #self.deltasec=max(secondi(delta),1)
        self.deltasec=secondi(delta)
        self.deltasec
        self.timer = Timer(self.deltasec, self.function,
                      [self.operation,self.media,self.programma])

    def start (self):
        "start of programmed schedule"
        
        self.timer.start()

def ManagePytone (operation,media,programma):
    "Manage pytone to do operation on media"


    unixsocketfile =  os.path.expanduser("~/.pytone/pytonectl")
    networklocation = unixsocketfile
    print(networklocation)

    try:
        channel = network.clientchannel(networklocation)

    except Exception as e:

        print("Error: cannot connect to PyTone server: %s" % e)
        sys.exit(2)
        
    channel.start()

    root,ext=os.path.splitext(media)

    if (ext == ".m3u"):
        medias=[]
        f = open(media, "r")
        for line in f.readlines():
            medias.append(line[:-1])
        f.close()

    else:
        medias=(media,)

    for mediasplit in medias:
        print("invio ->",mediasplit)
        if operation == "queueMedia":
            song = channel.request(\
                requests.autoregisterer_queryregistersong("main", mediasplit))
            channel.notify(events.playlistaddsongtop(song))

    channel.quit()


    print("scrivo in django")
    print(programma)
    ar_emitted(programma)
    print("scritto in django")


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
        print("faccio finta di salvarlo")

def main():

    programma=dummy_programma()

    function=ManagePytone
    operation="queueMedia"
#   media = "/home/pat1/django/autoradio/media/spots/spot-bibbiano.ogg"
    media="/home/pat1/django/autoradio/media/playlist/pomeridiana_ore_14_00.m3u"
    #media = raw_input("dammi il media? ")
    scheduledatetime=datetime.now()+timedelta(seconds=15)
    schedule=ScheduleProgram(function,operation,media,scheduledatetime,programma)
    schedule.start()

    scheduledatetime=datetime.now()+timedelta(seconds=100)
    media = "/home/pat1/django/autoradio/media/spots/spot-nocino.ogg"

    schedule=ScheduleProgram(function,operation,media,scheduledatetime,programma)
    schedule.start()

    scheduledatetime=datetime.now()+timedelta(seconds=200)
    media = "/home/pat1/django/autoradio/media/spots/spot-panedellamoni.ogg"

    schedule=ScheduleProgram(function,operation,media,scheduledatetime,programma)
    schedule.start()

    
if __name__ == '__main__':
    main()  # (this code was run as script)
    
