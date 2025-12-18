from pydub import AudioSegment
import logging
from .autoplayer.playlist import *

SILENCE_MS =8000

def assemble_playlists(playlistnames,playlistnames_fillers, multichannelname):

    NUM_CHANNEL=len(playlistnames)
    NUM_TRACK=NUM_CHANNEL*2
            
    p=[]
    for playlistname in playlistnames:
        p.append(Playlist([playlistname]))
        print("playlist:",playlistname)

    stereotracks= []    
    for pl in p:
        audiosegment=AudioSegment.empty()
        for element in pl:
            metadata=element.get_metadata()
            #print (metadata)
            audiosegment+=AudioSegment.from_file(metadata["path"][6:])
        stereotracks.append(audiosegment.set_channels(2))
        print("playlist read")



    pf=[]
    for playlistname in playlistnames_fillers:
        pf.append(Playlist([playlistname]))
        print("playlist filler:",playlistname)

    stereotracks_fillers= []    
    for pl in pf:
        audiosegment=AudioSegment.empty()
        for element in pl:
            metadata=element.get_metadata()
            #print (metadata)
            audiosegment+=AudioSegment.from_file(metadata["path"][6:])
        stereotracks_fillers.append(audiosegment.set_channels(2))
        print("playlist filler read")

        
    
    tracks=[]
    tracks_fillers=[]
    for i in range(NUM_TRACK):
        tracks.append(None)
        tracks_fillers.append(None)

    for i in range(0,NUM_TRACK,2):
        print (i)
        tracks[i],tracks[i+1]=stereotracks[int(i/2)].split_to_mono()
        tracks_fillers[i],tracks_fillers[i+1]=stereotracks_fillers[int(i/2)].split_to_mono()

    print ([len(tracks[i]) for i in range(NUM_TRACK)],"//",[len(tracks_fillers[i]) for i in range(NUM_TRACK)] )

    lunghezza = max([len(tracks[i]) for i in range(NUM_TRACK)])

    for i in range(NUM_TRACK):
        cortezza = len(tracks[i])
        print (cortezza,lunghezza)

        if ((lunghezza-cortezza) > SILENCE_MS and len(tracks_fillers[i]) >0):
            fillernumber = int((lunghezza-cortezza) / len(tracks_fillers[i])) +1
        else:
            fillernumber = 0
        print(fillernumber)

        if (fillernumber > 2) :
            tracks_fillers[i]=tracks_fillers[i] * fillernumber

        if (lunghezza != len(tracks[i])):
            if (lunghezza - len(tracks[i]) <= SILENCE_MS or len(tracks_fillers[i]) == 0):
                tracks[i] = tracks[i].append(AudioSegment.silent(duration = lunghezza - len(tracks[i])+1000, frame_rate=tracks[i].frame_rate), crossfade=0)[:lunghezza]
            else:
                tracks[i] = tracks[i].append(tracks_fillers[i][:lunghezza - len(tracks[i])+1000], crossfade=0)
                tracks[i] = tracks[i][:lunghezza].fade_out(duration=1000)

    print ([len(tracks[i]) for i in range(NUM_TRACK)])

    #faketrack = AudioSegment.silent(duration = lunghezza+1000, frame_rate=tracks[0].frame_rate)[:lunghezza]
    #tracks.append(faketrack)
    #if (NUM_CHANNEL == 6):
    #    remap=(0,2,1,5,6,4)
    #elif (NUM_CHANNEL == 7):
    #remap=(0,2,1,6,5,3,4)
    #else:
    #remap=tuple((i) for i in range(NUM_TRACK+1))
    #multitrack = AudioSegment.from_mono_audiosegments(*[tracks[remap[i]][:lunghezza] for i in range(NUM_TRACK+1)]) #,faketrack)
    #multitrack = AudioSegment.from_mono_audiosegments(*[tracks[i][:lunghezza] for i in range(NUM_TRACK)], faketrack)
    
    multitrack = AudioSegment.from_mono_audiosegments(*[tracks[i][:lunghezza] for i in range(NUM_TRACK)])

    multitrack.export( multichannelname, format="ogg")


def main():
    playlists=["media/spots/er_mezzogiorno.m3u","media/spots/lo_mezzogiorno.m3u","media/spots/to_mezzogiorno.m3u"]
    filler_playlists=["media/spots/er_mezzogiorno_filler.m3u","media/spots/er_mezzogiorno_filler.m3u","media/spots/er_mezzogiorno_filler.m3u"]
    outname="output.ogg"
    assemble_playlists(playlists,filler_playlists,outname)

if __name__ == '__main__':
    main()  # (this code was run as script)
    
