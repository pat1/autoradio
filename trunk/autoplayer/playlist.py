#!/usr/bin/python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

import logging
import collections
import mutagen
import sys
from xml.sax import make_parser, handler, SAXParseException
from xml.dom.minidom import Document
import urllib, urlparse

class Track(collections.namedtuple('Track',("path","time","artist","album","title","id"))):
  __slots__ = ()

  def get_metadata(self):

#    try:
#      m=mutagen.File(self.path[7:].encode(sys.getfilesystemencoding()),easy=True)
      m=mutagen.File(self.path[7:],easy=True)
      # in seconds (type float).

      metadata=collections.OrderedDict()
      metadata["path"] =self.path
      metadata["time"] = int(m.info.length*1000000000)
      metadata["artist"]=None
      metadata["album"]=None
      metadata["title"]=None
      metadata["id"]=None

      value = m.get("artist")
      if value:
        metadata["artist"]=value[0]#.encode("UTF-8")
      value = m.get("album")
      if value:
        metadata["album"]=value[0]#.encode("UTF-8")
      value = m.get("title")
      if value:
        metadata["title"]=value[0]#.encode("UTF-8")

#    except:
      #log.info("Could not read info from file: %s ",self.path)
#      print "errore"

      return metadata


def parse_pls(lines):

#    titles = {}
    songs = {}
    for line in lines:
      spl = line.split( '=', 1)
      if len(spl) == 2:
        name, value = spl

        if name.lower().startswith('file'):
          num = name[4:]
          try:
            n = int(num)
          except:
            pass
          else:
            songs["%05d" % n]  = value

        #elif name.lower().startswith('title'):
        #  num = name[4:]
        #  try:
        #    n = int(num)
        #  except:
        #    pass
        #  else:
        #    titles["%05d" % n]  = value

        else:
          logging.debug( "PLAYLIST: skip this line from pls playlist: %s",line)

    ret = []
    for k in sorted(songs.keys()):
#      ret.append( (songs[k], titles.get(k, None) ) )
      ret.append(songs[k])
    return ret
				

def parse_xspf2(data):
  handler = XSPFParser2()
  parser = make_parser()
  parser.setContentHandler(handler)
  parser.feed(data)
  return handler

class XSPFParser2(handler.ContentHandler):

  def __init__(s):
    s.path = u""
    s.tracks = []
    s.current=None
    s.position=None
    s.extensionapplication=None

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
    elif s.path == "/playlist/extension":
    #if name == 'extension':
      s.extensionapplication=  attrs.get('application',None) 

  def characters(s, content):
    s.content += content

  def endElement(s, name):

    if s.path == "/playlist/title":
      s.title = s.content
    elif s.path == "/playlist/extension/current":
      if s.extensionapplication == "autoplayer":
        s.current = str(s.content)
    elif s.path == "/playlist/extension/position":
      if s.extensionapplication == "autoplayer":
        s.position = int(s.content)
    elif s.path == "/playlist/trackList/track/location":
      # mmmm this is for audacious but I think is wrong
      ##s.track['location'] = urllib.unquote(s.content)
      #s.track['location'] = urllib.unquote(s.content.encode("UTF-8"))

      url=urlparse.urlsplit(s.content)
      s.track['location']=urlparse.urljoin("file://",urllib.unquote(url.path.encode("UTF-8")))

    elif s.path == "/playlist/trackList/track/title":
      s.track['title'] = s.content
    elif s.path == "/playlist/trackList/track/creator":
      s.track['creator'] = s.content
    elif s.path == "/playlist/trackList/track/album":
      s.track['album'] = s.content
    elif s.path == "/playlist/trackList/track/extension/id":
      s.track['id'] = s.content
    elif s.path == "/playlist/trackList/track":
      if s.track.get('location'):
        s.tracks.append(s.track)
        del s.track

    s.path = s.path.rsplit("/", 1)[0]


class Playlist(list):
	
  def __init__(self,media=None,tracks=None,current=None,position=None):
    super( Playlist, self ).__init__([])

    self.current=current
    self.position=position

    if media is not None:
      for ele in media:
        if ele.lower().endswith(".xspf") or \
        ele.lower().endswith(".m3u") or \
        ele.lower().endswith(".pls") :
          self.read(ele)
        else:
          track_meta=Track(ele,None,None,None,None,None)
        #print track_meta.get_metadata().values()
          tr=Track._make(track_meta.get_metadata().values())
          self.append(tr)

    if tracks is not None:
      for ele in tracks:
        self.append(ele)

  def read(s, path):

    try:
      with open(path, "r") as f:
        data = f.read()

    except IOError :
      logging.warning( "PLAYLIST: error opening file %s" % path)
      return

    if data.strip() == "": #empty
      logging.info( "PLAYLIST: empty")
      return

    logging.debug( "PLAYLIST: parse")
    parser = make_parser ()
    try:
      parser.feed(data)
    except:

      lines = data.split('\n')
      lines = map(lambda line: line.strip().rstrip(), lines)
      lines = filter(lambda line: line if line != "" and line[0] != '#' else None, lines)
      if lines == []:
        return

      #detect type of playlist
      if '[playlist]' in lines:
        logging.debug( "PLAYLIST: is PLS")
        lines = parse_pls(lines)

      for location in lines:

        url=urlparse.urlsplit(location)
        location=urlparse.urljoin("file://",urllib.unquote(url.path.encode("UTF-8")))

        track=Track._make(Track(location,None,None,None,None,None).get_metadata().values())
        s.append(track)

    else:
      logging.debug( "PLAYLIST: is XML")

      p = parse_xspf2(data)
      logging.debug( "PLAYLIST: xspf parsed")

      for ele in p.tracks:

        track=Track._make(Track(ele.get('location',None),ele.get('time',None),ele.get('creator',None),
                    ele.get('album',None),ele.get('title',None),ele.get('id',None)).get_metadata().values())
        s.append(track)


      #TODO read from file !!!!
      #s.current=s[2][5]
      #s.position=0

      s.current=p.current
      s.position=p.position
      #s.current="1"
      #s.position=180000000000
      logging.info ( "read from xspf current: %s" % s.current)
      logging.info ( "read from xspf position: %s" % s.position)


  def write(s,path):

    doc = Document()
    xspf_vlc_compatibility=False
    xspf_audacious_compatibility=False
    xspf_qmmp_compatibility=False

    with open(path, "w") as f:
			#head
      f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
      if xspf_vlc_compatibility:
        f.write('<playlist version="1" xmlns="http://xspf.org/ns/0/"' + \
                  ' xmlns:vlc="%s">\n' % VLC_NS)
      else:
        f.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')

      logging.info ( "writing to xspf current: %s" % s.current)
      logging.info ( "writing to xspf position: %s" % s.position)

      if s.current is not None or s.position is not None:
        f.write('\t<extension application="autoplayer">\n')

        if s.current is not None :
          k="current"
          t="int"
          v = doc.createTextNode(str(s.current)).toxml()
          f.write(u"\t\t<%s type='%s'>%s</%s>\n"	% (k, t, v, k))

        if s.position is not None:
          k="position"
          v = doc.createTextNode(str(s.position)).toxml()
          f.write(u"\t\t<%s type='%s'>%s</%s>\n"	% (k, t, v, k))

        f.write('\t</extension>\n')

      f.write('<trackList>\n')
      for track in s:
        track=track._asdict()
        f.write('\t<track>\n')
        if track.get('title') not in ['', None]:
          f.write( '\t\t<title>%s</title>\n' \
                     % doc.createTextNode(track['title'].encode("utf-8")).toxml() )
        if track.get('artist') not in ['', None]:
          f.write('\t\t<creator>%s</creator>\n' \
                    % doc.createTextNode(track['artist'].encode("utf-8")).toxml() )
        if track.get('album') not in ['', None]:
          f.write( '\t\t<album>%s</album>\n' \
                     % doc.createTextNode(track['album'].encode("utf-8")).toxml() )
        if track.get('tracknum') not in ['', None]:
          if type(track['tracknum']) == int:
            no = track['tracknum']
          elif type(track['tracknum']) in [unicode, str]:
            cnum=track['tracknum'].split("/")[0].lstrip('0')
            if cnum != "":
              no = int( track['tracknum'].split("/")[0].lstrip('0') )
            else:
              no=0
          else:
            no = 0
          if no > 0:
            f.write( '\t\t<trackNum>%i</trackNum>\n' % no )

        #if float are seconds; if integer nanosec
        # out should be millisec
        if type(track.get('time')) == float:
          tm = track['time']*1000000
        elif type(track.get('time')) == int:
          tm = track['time']/1000000.
        else:
          tm= None

        if tm is not None:
          tm = int(round(tm))
          f.write('\t\t<duration>%i</duration>\n' % tm )

        #write location
        #make valid quoted location
        location = track['path']

        url=urlparse.urlsplit(location)
        #here problem when file name come fron gtk or command line
        try:
          location=urlparse.urljoin("file://",urllib.quote(url.path))
        except:
          location=urlparse.urljoin("file://",urllib.quote(url.path.encode("UTF-8")))

        ##location = location.encode("utf-8")
        #if    not 'http://' in location.lower() and \
        #      not 'file://' in location.lower():
        #  location = 'file://' + location
        #location = urllib.quote( location )
                                  
        #write the location
        f.write( '\t\t<location>%s</location>\n' \
                   % doc.createTextNode(location).toxml() )

        #write other info:
        keys = set(track.keys())
        keys.discard('title')
        keys.discard('artist')
        keys.discard('album')
        keys.discard('tracknum')
        keys.discard('time')
        keys.discard('path')
        if len(keys) > 0:
          f.write('\t\t<extension application="autoplayer">\n')
          for k in sorted(keys):
            if track[k] != None:
              v = track[k]
              t = type(v)
              if t in [str, unicode]:
                t = "str"
                v = unicode(v)
              elif t == bool:
                t = "bool"
                v = '1' if v else '0'
              elif t in [int, long]:
                t = "int"
                v = str(v).encode("utf-8")
              elif t == float:
                t = "float"
                v = repr(v)
              else:
                continue
              v = doc.createTextNode(v).toxml()
          
              f.write(u"\t\t\t<%s type='%s'>%s</%s>\n"	% (k, t, v, k))
          f.write('\t\t</extension>\n')
        f.write('\t</track>\n')
			#tail
      f.write('</trackList>\n')
      f.write('</playlist>\n')


class Playlist_mpris2(collections.OrderedDict):
	
  def __init__(self,playlist=Playlist([]),current=None,position=None):
    super( Playlist_mpris2, self ).__init__(collections.OrderedDict())
    for id,track in enumerate(playlist):
      if (track.id is None):
        self[str(id)]=track
      else:
        self[track.id]=track

    if len (self) == 0 :
      self.current = None
    else:
      #self.current = self.keys()[0]
      if current is None:
        self.current = self.keys()[0]
      else:
        self.current=current

    self.position=position

    self.redefine_id()

  def get_current(self):
    if self.current is not None: 
      return self[self.current]
    else:
      return Track(None,None,None,None,None,None)

  def set_current(self,id):
    if id in self.keys():
      self.current=id
    else:
      logging.warning ("set_current: invalid id")

  def next(self):

    self.current = self.nextid(self.current)
    logging.info ( "current: %s" % self.current)

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
    logging.info ( "current: %s" % self.current)


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
      ind =len(keys)-1
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

    newself.redefine_id()
    return newself


  def removetrack(self,trackid):
    self.pop(trackid,None)

  def redefine_id(self):
    tracks=[]
    for id,track in self.iteritems():
      tr=Track._make((track.path,track.time,track.artist,track.album,track.title,str(id)))
      self[id]=tr
    
  def write(self,path):
    Playlist(tracks=self.values(),current=self.current,position=self.position).write(path)
    
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

  print "--------- playlist ord dict -----------------------"
  op=Playlist_mpris2(p)

  op=op.addtrack(uri,aftertrack="1",setascurrent=True)

  op.write("/tmp/tmp.xspf")

  print "--------- playlist from file -----------------------"

  p=Playlist(["/tmp/tmp.xspf"])

  print "--------- playlist from file ord dict -----------------------"
  op=Playlist_mpris2(p)

  op=op.addtrack(uri,aftertrack="1",setascurrent=True)
  print op

  op.write("/tmp/tmpout.xspf")

  print "--------- reread playlist from file ord dict -----------------------"
  p=Playlist(["/tmp/tmpout.xspf"])
  op=Playlist_mpris2(p)
  print op
  op.write("/tmp/tmpout2.xspf")
  
if __name__ == '__main__':
  main()  # (this code was run as script)
    
