#!/usr/bin/python
# -*- coding: utf-8 -*-
# GPL. (C) 2012 Paolo Patruno.

import logging
import collections
import mutagen
import sys
from xml.sax import make_parser, handler, SAXParseException
from xml.dom.minidom import Document
import urllib

#Track=collection.namedtuple("track",("path","time","artist","album","title"))

class Track(collections.namedtuple('Track',("path","time","artist","album","title"))):
  __slots__ = ()

  def get_metadata(self):

#    try:
#      m=mutagen.File(self.path[7:].encode(sys.getfilesystemencoding()),easy=True)
      m=mutagen.File(self.path[7:],easy=True)
      # in seconds (type float).

      metadata=collections.OrderedDict()
      metadata["path"] =self.path
      metadata["time"] = m.info.length*1000000000
      metadata["artist"]=None
      metadata["album"]=None
      metadata["title"]=None

      value = m.get("artist")
      if value:
        metadata["artist"]=value[0]
        value = m.get("album")[0]
      if value:
        metadata["album"]=value
        value = m.get("title")[0]
      if value:
        metadata["title"]=value
      self
#    except:
      #log.info("Could not read info from file: %s ",self.path)
#      print "errore"

      return metadata


def is_xml(data):
  # returns : empty -1, xml 1, else 0
  if data.strip() == "":
    return -1
	
  parser = make_parser ()
  try:
    parser.feed(data.encode('utf-8'))
  except:
    return 0
  else:
    return 1

def parse_xspf2(data):
  handler = XSPFParser2()
  parser = make_parser()
  parser.setContentHandler(handler)
  parser.feed(data.encode('utf-8'))
  return handler

class XSPFParser2(handler.ContentHandler):

  def __init__(s):
    s.path = u""
    s.tracks = []

  def parseFile(s, fileName):
	   
    try:
      parser = make_parser()
      parser.setContentHandler(s)
      parser.parse(fileName)
      return True
    except SAXParseException:
      return False

  def startElement(s, name, attrs):
    s.path += "/%s" % name
    s.content = ""
    if s.path == "/playlist/trackList/track":
      s.track = {}

  def characters(s, content):
    s.content = s.content + content

  def endElement(s, name):

    if s.path == "/playlist/trackList/track":
      if s.track.get('location'):
        s.tracks.append(s.track)
        del s.track
    elif s.path == "/playlist/title":
      s.track['title'] = s.content
    elif s.path == "/playlist/trackList/track/location":
      s.track['location'] = urllib.unquote(s.content)
    elif s.path == "/playlist/trackList/track/title":
      s.track['title'] = s.content
    elif s.path == "/playlist/trackList/track/creator":
      s.track['creator'] = s.content
    elif s.path == "/playlist/trackList/track/album":
      s.track['album'] = s.content
		
    s.path = s.path.rsplit("/", 1)[0]


class Playlist(list):
	
  def __init__(self,media=None,tracks=None):
    super( Playlist, self ).__init__([])
    
    if media is not None:
      for ele in media:
        if ele.lower().endswith(".xspf"):
          self.read(ele)
        else:
          track_meta=Track(ele,None,None,None,None)
        #print track_meta.get_metadata().values()
          tr=Track._make(track_meta.get_metadata().values())
          self.append(tr)

    if tracks is not None:
      for ele in tracks:
        self.append(ele)

  def read(s, path):

    try:
      with open(path, "r") as f:
        data = f.read().decode('utf-8')
    except UnicodeDecodeError,e:
      logging.debug( "PLAYLIST: unicode decode error")
      return
    except:
      logging.debug( "PLAYLIST: error opening file %s" % path)
      return
		
    if data.strip() == "": #empty
      logging.debug( "PLAYLIST: empty")
      return

    logging.debug( "PLAYLIST: parse")
    parser = make_parser ()
    try:
      parser.feed(data.encode('utf-8'))
    except:
      logging.debug( "PLAYLIST: not XML")
      return
    else:
      p = parse_xspf2(data)
      logging.debug( "PLAYLIST: xspf parsed")
      for ele in p.tracks:

        track=Track._make(Track(ele.get('location',None),ele.get('time',None),ele.get('creator',None),
                    ele.get('album',None),ele.get('title',None)).get_metadata().values())
        s.append(track)


  def write(s,path):

    doc = Document()
    xspf_vlc_compatibility=False
    xspf_audacious_compatibility=False
    xspf_qmmp_compatibility=False
    PEYOTE_EXTNSION="bho"

    with open(path, "w") as f:
			#head
      f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
      if xspf_vlc_compatibility:
        f.write('<playlist version="1" xmlns="http://xspf.org/ns/0/"' + \
                  ' xmlns:vlc="%s">\n' % VLC_NS)
      else:
        f.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')
      f.write('<trackList>\n')
      for track in s:
        track=track._asdict()
        f.write('\t<track>\n')
        if track.get('title') not in ['', None]:
          f.write( '\t\t<title>%s</title>\n' \
                     % doc.createTextNode(track['title']).toxml() )
        if track.get('artist') not in ['', None]:
          f.write('\t\t<creator>%s</creator>\n' \
                    % doc.createTextNode(track['artist']).toxml() )
        if track.get('album') not in ['', None]:
          f.write( '\t\t<album>%s</album>\n' \
                     % doc.createTextNode(track['album']).toxml() )
        if track.get('id') not in ['', None]:
          if type(track['id']) == int:
            no = track['id']
          elif type(track['id']) in [unicode, str]:
            no = int( track['id'].split("/")[0].lstrip('0') )
          else:
            no = 0
            if no > 0:
              f.write( '\t\t<trackNum>%i</trackNum>\n' % no )
        if type(track.get('time')) == float:
          tm = track['time']*1000
          if tm%1 >= 0.5:	
            tm = int(tm) + 1
          else:
            tm = int(tm)
          f.write('\t\t<duration>%i</duration>\n' % tm )

        #write location
        #make valid quoted location
        location = track['path']

        if    not 'http://' in location.lower() and \
              not 'file://' in location.lower():
          location = urllib.quote( location )
          location = 'file://' + location
                                  
        #write the location
        f.write( '\t\t<location>%s</location>\n' \
                   % doc.createTextNode(location).toxml() )
        f.write('\t</track>\n')
			#tail
      f.write('</trackList>\n')
      f.write('</playlist>\n')


class Playlist_mpris2(collections.OrderedDict):
	
  def __init__(self,playlist=Playlist([])):
    super( Playlist_mpris2, self ).__init__(collections.OrderedDict())
    for id,track in enumerate(playlist):
      self[str(id)]=track

    if len (self) == 0 :
      self.current = None
    else:
      self.current = self.keys()[0]

  def get_current(self):
    if self.current is not None: 
      return self[self.current]
    else:
      return Track(None,None,None,None,None)

  def set_current(self,id):
    if id in self.keys():
      self.current=id
    else:
      print "set_current: invalid id"

  def next(self):

    self.current = self.nextid(self.current)
    print "current:",self.current

  def nextid(self,id):

    if id is None:
      return None

    keys=self.keys()
    ind = keys.index(id)

    if len(keys)-1 <= ind :
      return None
    ind += 1
    return keys[ind]


  def previous(self):

    self.current = self.previousid(self.current)
    print "current:",self.current


  def previousid(self,id):

    if id is None:
      return None

    keys=self.keys()
    ind = keys.index(id)

    if ind == 0 :
      return None
    ind -= 1
    return keys[ind]


  def addtrack(self,uri,aftertrack=None,setascurrent=False):

    keys=self.keys()

    if aftertrack is None:
      ind =0
    else:
      ind = keys.index(aftertrack)

    newself=Playlist_mpris2()

    if  len(keys) > 0:
      id = keys[ind]
      startnewid=max([int(x) for x in keys]) + 1 
    else:
      id="0"
      startnewid=0
      p=Playlist([uri])
      for newid,track in enumerate(p,startnewid):
        newself[str(newid)]=Track._make(track.get_metadata().values())

    for nid,ntrack in self.iteritems():
      newself[nid]=ntrack
      if nid == id:
        p=Playlist([uri])
        for newid,track in enumerate(p,startnewid):
          newself[str(newid)]=Track._make(track.get_metadata().values())

    if setascurrent: 
      if len(newself) >=0:
        newself.current=str(startnewid)
      else:
        newself.current=self.current

    return newself


  def removetrack(self,trackid):
    self.pop(trackid,None)

  def write(self,path):
    Playlist(tracks=self.values()).write(path)
    

def main():

  import logging
  logging.basicConfig(level=logging.DEBUG,)

  media=(
    u"file:///home/pat1/Musica/Paolo Benvegnù/Piccoli fragilissimi film/3 - Io e te.flac",
    u"file:///home/pat1/Musica/Paolo Benvegnù/Piccoli fragilissimi film/5 - Fiamme.flac",
    u"file:///home/pat1/Musica/Paolo Benvegnù/Piccoli fragilissimi film/9 - Only for You.flac",
    )

  uri=u"file:///home/pat1/Musica/Paolo Benvegnù/Piccoli fragilissimi film/2 - Cerchi nell'acqua.flac"

  print "-------------- playlist ------------------"
  p=Playlist(media)

  print p

  print "--------- playlist ord dict -----------------------"
  op=Playlist_mpris2(p)
  print op


  op=op.addtrack(uri,aftertrack="1",setascurrent=True)
  print op

  print "--------- playlist from file -----------------------"

  p=Playlist(["/tmp/tmp.xspf"])
  print p

  print "--------- playlist from file ord dict -----------------------"
  op=Playlist_mpris2(p)
  print op

  op.write("/tmp/tmpout.xspf")


if __name__ == '__main__':
  main()  # (this code was run as script)
    
