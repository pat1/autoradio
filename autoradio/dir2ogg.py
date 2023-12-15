#!/usr/bin/python
#
# Copyright (C) 2007-2009 Julian Andres Klode <jak@jak-linux.org>
# Copyright (C) 2003-2006 Darren Kirby <d@badcomputer.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# 10-08-2009 modified by Paolo Patruno

'''
dir2ogg converts mp3, m4a, and wav files to the free open source OGG format. Oggs are
about 20-25% smaller than mp3s with the same relative sound quality. Your mileage may vary.

Keep in mind that converting from mp3 or m4a to ogg is a conversion between two lossy formats.
This is fine if you just want to free up some disk space, but if you're a hard-core audiophile
you may be dissapointed. I really can't notice a difference in quality with 'naked' ears myself.

This script converts mp3s to wavs using mpg123 then converts the wavs to oggs using oggenc.
m4a conversions require faad. Id3 tag support requires mutagen for mp3s.
Scratch tags using the filename will be written for wav files (and mp3s with no tags!)
'''
from past.utils import old_div
import sys
import os, os.path
import re
from fnmatch import _cache, translate
from optparse import OptionParser
from subprocess import Popen, call, PIPE

__version__ = '0.11.7'
__date__    = '2009-05-03'

FILTERS = {'mp3': ('*.mp3',),
           'm4a': ('*.aac', '*.m4a', '*.mp4'),
           'wma': ('*.asf', '*.wma', '*.wmf'),
           'flash': ('*.flv', ),
           'flac': ('*.flac',),
           'wav': ('*.wav', ),
           'speex': ('*.spx','*.speex' ),
           }

def mmatch(names, patterns, rbool=True):
    '''names/patterns=str/list/tuple'''
    results = []
    if isinstance(names, str):
        names = [names]
    if isinstance(patterns, str):
        patterns = [patterns]
    for pat in patterns:
        pat = pat.lower()
        if not pat in _cache:
            _cache[pat] = re.compile(translate(pat))
        match = _cache[pat].match
        for name in names:
            if match(name.lower()):
                if rbool:
                    return True
                else:
                    results.append(name)
    if rbool:
        return bool(results)
    else:
        return results

def read_opts():
    if not '--version' in sys.argv:
        show_banner()
    if len(sys.argv[1:]) == 0:
        fatal('No arguments specified, see --help for usage.')
    parser = OptionParser(usage='%prog [options] [arguments]', version='%prog ' + __version__)
    parser.add_option('-l', '--license', action='callback', callback=show_license, help='display license informations')
    parser.add_option('-d', '--directory', action='store_true', help='convert files in all directories specified as arguments')
    parser.add_option('-r', '--recursive', action='store_true', help='convert files in all subdirectories of all directories specified as arguments')
    parser.add_option('-c', '--cdda', action='store_true', help="convert audio cd in all devices specified as arguments (or default: /dev/cdrom) [EXPERIMENTAL]")
    parser.add_option('-q', '--quality', metavar='N', default=3.0, type='float', help='quality. N is a number from 1-10 (default %default)')
    parser.add_option('-t', '--smart-mp3', action='store_true', help='try to use similar quality as original mp3 file (overwrites -q)')
    parser.add_option('-T', '--smart-mp3-correction', metavar='N', default=0.0, type='float', help='decrease detected quality (implies -t)')
    parser.add_option('-n', '--no-mp3', dest='convert_mp3', action='store_false', default=True, help="don't convert mp3s (use with '-d' or '-r')")
    parser.add_option('-a', '--convert-all', action='store_true', help="convert all supported formats")
    parser.add_option('-f', '--convert-flac', action='store_true', help="convert flac files (use with '-d')")
    parser.add_option('-x', '--convert-speex', action='store_true', help="convert speex files (use with '-d')")
    parser.add_option('-m', '--convert-m4a', action='store_true', help="convert m4a files (use with '-d')")
    parser.add_option('-w', '--convert-wav', action='store_true', help="convert wav files (use with '-d')")
    parser.add_option('-W', '--convert-wma', action='store_true', help="convert wma files (use with '-d').")
    parser.add_option('-F', '--convert-flash', action='store_true', help="convert flash files (use with '-d').")
    parser.add_option('--delete-input', action='store_true', help='delete input files')
    parser.add_option('-p', '--preserve-wav', action='store_true', help='keep the wav files (also includes -P)')
    parser.add_option('-P', '--no-pipe', action='store_true', help='Do not use pipes, use temporary wav files')
    parser.add_option('-v', '--verbose', action='store_true', help='verbose output')

    # Setup decoders
    commands = {'mp3': ('mpg123', 'mpg321', 'lame',  'mplayer'),
        'wma': ('mplayer',),
        'm4a': ('faad', 'mplayer'),
        'flash':  ('mplayer',),
        'flac': ('flac', 'ogg123', 'mplayer'),
        'speex': ('speexdec',),
        'cd':  ('cdparanoia', 'icedax','cdda2wav', 'mplayer'),
        }

    for ext, dec in list(commands.items()):
        default, choices = None, []
        for command in dec:
            in_path = [prefix for prefix in os.environ['PATH'].split(os.pathsep) if os.path.exists(os.path.join(prefix, command))]
            if in_path:
                choices.append(command)
                default = default or command
        parser.add_option('--' + ext + '-decoder', type="choice", metavar=default, default=default, choices=choices, help="decoder for %s files (choices: %s)" % (ext, ', '.join(choices)))

    # End of decoder options
    options, args = parser.parse_args()

    options.convert_cd = options.cdda
    options.filters    = []
    for ext, pat in list(FILTERS.items()):
        # Activate Encoders for files on the commandline
        if options.convert_all or mmatch(args, pat):
            setattr(options, 'convert_' + ext, True)
        if getattr(options, 'convert_' + ext):
            options.filters += pat
        # Missing decoders
        if ext != 'wav' and getattr(options, 'convert_' + ext) and not getattr(options, ext + '_decoder'):
            fatal('%s was enabled, but no decoder has been found.' % ext)

    if len(args) == 0 and not options.cdda:
        fatal('No files/directories specified.')
    return options, args

def info(msg):
    print('Information: %s' % msg)

def warn(msg):
    '''print errors to the screen (red)'''
    print("Warning: %s" % msg, file=sys.stderr)

def fatal(msg):
    '''Fatal error (error + exit)'''
    print("Error: %s" % msg, file=sys.stderr)
    sys.exit(1)

def return_dirs(root):
    mydirs = {}
    for pdir, dirs, files in os.walk(root):
        if not pdir in mydirs:
            mydirs[pdir] = files
    return mydirs

class Id3TagHandler(object):
    '''Class for handling meta-tags. (Needs mutagen)'''
    accept = ['album', 'album_subtitle', 'albumartist', 'albumartistsort',
              'albumsort', 'artist', 'artistsort', 'asin', 'bpm', 'comment',
              'compilation', 'composer', 'composersort', 'conductor', 'copyright',
              'date', 'discid', 'discnumber', 'encodedby', 'engineer', 'gapless',
              'genre', 'grouping', 'isrc', 'label', 'lyricist', 'lyrics', 'mood',
              'musicbrainz_albumartistid', 'musicbrainz_albumid', 'musicbrainz_artistid',
              'musicbrainz_discid', 'musicbrainz_sortname', 'musicbrainz_trackid',
              'musicbrainz_trmid', 'musicip_puid', 'podcast', 'podcasturl',
              'releasecountry', 'musicbrainz_albumstatus', 'musicbrainz_albumtype', 'remixer', 'show',
              'showsort', 'subtitle', 'title', 'titlesort', 'tracknumber', 'tracktotal']

    def __init__(self, song):
        self.song = song
        self.tags = {}

    def grab_common(self, handler, convert=None, error=None):
        '''Common grabber, starts the handler and applies the tags to self.tags'''
        try:
            mydict  = handler(self.song)
        except error as msg:
            import warnings,traceback;
            warn('Mutagen failed on %s, no tags available' % self.song)
            traceback.print_exc(0)
            print(file=sys.stderr)
            return
        if convert:
            convert = dict([(k.lower(), v.lower()) for k, v in list(convert.items())]) # Fix convert
        for key, val in list(mydict.items()):
            key = key.lower()
            key = convert and (key in convert and convert[key] or key) or key
            if not key in self.accept:
                continue
            if not convert: # Hack for FLAC, which uses Vorbis tags
                pass
            elif hasattr(val, 'text'):
                val = val.text
            if convert:
                new_val = []
                if not isinstance(val, list):
                    val = [val]
                for i in val:
                    if not isinstance(i, str):
                        # Convert all invalid values to unicode
                        try:
                            new_val.append(str(i))
                        except UnicodeDecodeError:
                            warn('Ignoring UnicodeDecodeError in key %s' % key)
                            new_val.append(str(i, errors='ignore'))
                    else:
                        new_val.append(i)
                val = new_val
                del new_val

            self.tags[key] = val

    def grab_m4a_tags(self):
        '''Import MP4 tags handler, set convert and call commonGrab'''
        convert = {'----:com.apple.iTunes:ASIN': 'asin',
                   '----:com.apple.iTunes:MusicBrainz Album Artist Id': 'musicbrainz_albumartistid',
                   '----:com.apple.iTunes:MusicBrainz Album Id': 'musicbrainz_albumid',
                   '----:com.apple.iTunes:MusicBrainz Album Release Country': 'releasecountry',
                   '----:com.apple.iTunes:MusicBrainz Album Status': 'musicbrainz_albumstatus',
                   '----:com.apple.iTunes:MusicBrainz Album Type': 'musicbrainz_albumtype',
                   '----:com.apple.iTunes:MusicBrainz Artist Id': 'musicbrainz_artistid',
                   '----:com.apple.iTunes:MusicBrainz Disc Id': 'musicbrainz_discid',
                   '----:com.apple.iTunes:MusicBrainz TRM Id': 'musicbrainz_trmid',
                   '----:com.apple.iTunes:MusicBrainz Track Id': 'musicbrainz_trackid',
                   '----:com.apple.iTunes:MusicIP PUID': 'musicip_puid',
                   'aART': 'albumartist', 'cpil': 'compilation', 'cprt': 'copyright',
                   'pcst': 'podcast', 'pgap': 'gapless', 'purl': 'podcasturl',
                   'soaa': 'albumartistsort', 'soal': 'albumsort', 'soar': 'artistsort',
                   'soco': 'composersort', 'sonm': 'titlesort', 'sosn': 'showsort',
                   'trkn': 'tracknumber', 'tvsh': 'show', '\xa9ART': 'artist',
                   '\xa9alb': 'album', '\xa9cmt': 'comment', '\xa9day': 'date',
                   '\xa9gen': 'genre', '\xa9grp': 'grouping', '\xa9lyr': 'lyrics',
                   '\xa9nam': 'title', '\xa9too': 'encodedby','\xa9wrt': 'composer'}
        try:
            from mutagen.mp4 import MP4, error
        except ImportError:
            from mutagen.m4a import M4A as MP4, error
        self.grab_common(MP4, convert, error)

    def grab_wma_tags(self):
        '''Import ASF tags handler, set convert and call commonGrab'''
        convert = {'Author': 'artist', 'Description': 'comment',
                   'MusicBrainz/Album Artist Id': 'musicbrainz_albumartistid',
                   'MusicBrainz/Album Id': 'musicbrainz_albumid',
                   'MusicBrainz/Album Release Country': 'releasecountry',
                   'MusicBrainz/Album Status': 'musicbrainz_albumstatus',
                   'MusicBrainz/Album Type': 'musicbrainz_albumtype',
                   'MusicBrainz/Artist Id': 'musicbrainz_artistid',
                   'MusicBrainz/Disc Id': 'musicbrainz_discid',
                   'MusicBrainz/TRM Id': 'musicbrainz_trmid',
                   'MusicBrainz/Track Id': 'musicbrainz_trackid',
                   'MusicIP/PUID': 'musicip_puid',
                   'WM/AlbumArtist': 'albumartist',
                   'WM/AlbumArtistSortOrder': 'albumartistsort',
                   'WM/AlbumSortOrder': 'albumsort',
                   'WM/AlbumTitle': 'album',
                   'WM/ArtistSortOrder': 'artistsort',
                   'WM/BeatsPerMinute': 'bpm',
                   'WM/Composer': 'composer',
                   'WM/Conductor': 'conductor',
                   'WM/ContentGroupDescription': 'grouping',
                   'WM/Copyright': 'copyright',
                   'WM/EncodedBy': 'encodedby',
                   'WM/Genre': 'genre',
                   'WM/ISRC': 'isrc',
                   'WM/Lyrics': 'lyrics',
                   'WM/ModifiedBy': 'remixer',
                   'WM/Mood': 'mood',
                   'WM/PartOfSet': 'discnumber',
                   'WM/Producer': 'engineer',
                   'WM/Publisher': 'label',
                   'WM/SetSubTitle': 'album_subtitle',
                   'WM/SubTitle': 'subtitle',
                   'WM/TitleSortOrder': 'titlesort',
                   'WM/TrackNumber': 'tracknumber',
                   'WM/Writer': 'lyricist',
                   'WM/Year': 'date',
                  }
        from mutagen.asf import ASF, error
        self.grab_common(ASF, convert, error)

    def grab_flac_tags(self):
        '''Import FLAC tags handler, and call commonGrab'''
        from mutagen.flac import FLAC, error
        self.grab_common(FLAC, error=error)

    def grab_flash_tags(self):
        '''Import FLAC tags handler, and call commonGrab'''
        pass

    def grab_speex_tags(self):
        '''Import speex tags handler, and call commonGrab'''
        from mutagen.oggspeex import OggSpeex, error
        self.grab_common(OggSpeex, error=error)


    def grab_mp3_tags(self):
        '''Import MP3 tags handler, and call commonGrab'''
        from mutagen.id3 import ID3, error
        convert = {'TPE1': 'artist', 'TPE2': 'albumartist', 'TPE3': 'conductor', 'TPE4': 'remixer',
                   'TCOM': 'composer', 'TCON': 'genre', 'TALB': 'album', 'TIT1': 'grouping',
                   'TIT2': 'title', 'TIT3': 'subtitle', 'TSST': 'discsubtitle', 'TEXT': 'lyricist',
                   'TCMP': 'compilation', 'TDRC': 'date', 'COMM': 'comment', 'TMOO': 'mood',
                   'TMED': 'media', 'TBPM': 'bpm', 'WOAR': 'website', 'TSRC': 'isrc',
                   'TENC': 'encodedby', 'TCOP': 'copyright', 'TSOA': 'albumsort',
                   'TSOP': 'artistsort', 'TSOT': 'titlesort','TPUB': 'label',
                   'TRCK': 'tracknumber'}
        self.grab_common(ID3, convert, error)

    def list_if_verbose(self):
        info('Meta-tags I will write:')
        for key, val in list(self.tags.items()):
            if type(val) == list:
                info(key + ': ' + ','.join(val))
            else:
                info(key + ': ' + val)

class Convert(Id3TagHandler):
    '''
    Base conversion Class.

    __init__ creates some useful attributes,
    grabs the id3 tags, and sets a flag to remove files.
    Methods are the conversions we can do
    '''

    def __init__(self, song, conf):
        self.device  = ""
        self.track   = ""
        Id3TagHandler.__init__(self, song)
        self.conf    = conf
        song_root    = os.path.splitext(song)[0] + "."
        self.songwav = song_root + 'wav'
        self.songogg = song_root + 'ogg'
        self.decoder = ''

        if (os.path.exists(self.songogg)):
            warn('try to convert to an already present file: %s' % self.songogg)
            return

        # (smartmp3) I have to remember default quality for next files
        original_quality = self.conf.quality
        for ext, pat in list(FILTERS.items()):
            if mmatch(self.song, pat) and ext != 'wav':
                self.decoder = getattr(self.conf, ext + '_decoder')
                getattr(self, 'grab_%s_tags' % ext)()
                if ext == 'mp3' and  (self.conf.smart_mp3 or \
                                      self.conf.smart_mp3_correction):
                    self.smart_mp3()
        #self.songogg = "%(artist)s/%(album)s/%(track)s - %(title)s.ogg" % self.tags
        #self.songogg = "%(artist)s/%(album)s - %(title)s.ogg" % self.tags
        self.convert()
        # (smartmp3) Replacing quality by default value
        self.conf.quality = original_quality

    def smart_mp3(self):
        # initial Code by Marek Palatinus <marek@palatinus.cz>, 2007
        # Table of quality = relation between mp3 bitrate and vorbis quality. Source: wikipedia
        # quality_table = {45:-1, 64:0, 80:1, 96:2, 112:3, 128:4, 160:5, 192:6, 224:7, 256:8, 320:9, 500:10 }
        # log(0.015*bitrate, 1.19) is logaritmic regression of table above. Useful for mp3s in VBR :-).

        try:
            from mutagen.mp3 import MP3, HeaderNotFoundError
        except ImportError:
            warn('(smartmp3) You dont have mutagen installed. Bitrate detection failed. Using default quality %.02f' % self.conf.quality)
            return
        try:
            mp3info = MP3(self.song)
            bitrate = mp3info.info.bitrate
        except HeaderNotFoundError:
            info('(smartmp3) File is not an mp3 stream. Using default quality %.02f' % self.conf.quality)
            return

        import math
        self.conf.quality = round(5.383 * math.log(0.01616 * bitrate/1000.) - self.conf.smart_mp3_correction, 2)
        self.conf.quality = max(self.conf.quality, -1) # Lowest quality is -1
        self.conf.quality = min(self.conf.quality, 6) # Highest quality is 6
        info("(smartmp3) Detected bitrate: %d kbps" % (old_div(bitrate,1000)))
        info("(smartmp3) Assumed vorbis quality: %.02f" % self.conf.quality)

    def decode(self):
        # Used for mplayer
        tempwav = 'dir2ogg-%s-temp.wav' % os.getpid()
        if self.decoder not in ('mplayer','speexdec') and not self.conf.no_pipe and not self.conf.preserve_wav:
            outfile, outfile1 = '-', '/dev/stdout'
            use_pipe = 1
        else:
            outfile = outfile1 = self.songwav
            use_pipe = 0
        decoder = {'mpg123':  ['mpg123', '-w', outfile1, self.song],
                   'mpg321':  ['mpg321', '-w', outfile, self.song],
                   'faad':    ['faad',  '-o' , outfile1, self.song],
                   'ogg123':  ['ogg123', '-dwav', '-f' , outfile, self.song],
                   'flac':    ['flac', '-o', outfile, '-d', self.song],
                   'speexdec':['speexdec', self.song, outfile],
                   'lame':    ['lame', '--quiet', '--decode', self.song, outfile],
                   'mplayer': ['mplayer', '-vo', 'null', '-vc' ,'dummy', '-af', 'resample=44100', '-ao', 'pcm:file=' + tempwav, self.song],
                   'alac-decoder': ['alac-decoder',  self.song],
                   'cd-cdparanoia': ['cdparanoia', '-Z', '-q',  '-w', '-d', self.device, str(self.track), outfile],
                   'cd-icedax':      ['icedax', '-H', '-t', str(self.track), '-D',self.device],
                   'cd-cdda2wav':    ['cdda2wav', '-H', '-t', str(self.track), '-D',self.device],
                   'cd-mplayer':     ['mplayer', '-vo', 'null', '-vc' ,'dummy', '-af', 'resample=44100', '-ao', 'pcm:file=temp.wav', '-cdrom-device', self.device, "cdda://" + str(self.track)]}
        if use_pipe:
            return True, Popen(decoder[self.decoder], stdout=PIPE)
        else:
            decoder['cd-cdparanoia'].remove('-q')
            decoder['lame'].remove('--quiet')
            retcode = call(decoder[self.decoder])
            if self.decoder == 'mplayer':
                # Move the file for mplayer (which uses tempwav), so it works
                # for --preserve-wav.
                os.rename(tempwav, self.songwav)
            if retcode != 0:
                return (False, None)
            else:
                return (True, None)

    def convert(self):
        ''' Convert wav -> ogg.'''
        if self.songwav == self.song:
            success = True
            dec = None
        else:
            success, dec = self.decode()
        if not success:
            warn('Decoding of "%s" failed.' % self.song)
            return

        if dec and self.decoder == 'mpg123':
            import mutagen
            try:
                info("additional option:" )
                opts=['-R', str(mutagen.File(self.song).info.sample_rate)]
                info(str(opts))
            except:
                opts=[]
        else:
            opts=[]

        if dec:
            enc = Popen(['oggenc', '-Q', '-o', self.songogg, '-q', str(self.conf.quality).replace('.', ','), '-'] + opts, stdin=dec.stdout)
            enc.communicate()
            dec.wait()
            if dec.returncode < 0:
                warn('Decoding of "%s" failed.' % self.song)
                return False
            elif enc.returncode < 0:
                warn('Encoding of "%s" failed.' % self.song)
                return False
        else:
            enc = call(['oggenc', '-o', self.songogg, '-q', str(self.conf.quality).replace('.', ','), self.songwav])
            if enc != 0:
                warn('Encoding of "%s" failed.' % self.songwav)
                return False
            elif not self.conf.preserve_wav and self.song != self.songwav:
                os.remove(self.songwav)

        if self.tags != {}:
            try:
                # Add tags to the ogg file
                from mutagen.oggvorbis import OggVorbis
                myogg = OggVorbis(self.songogg)
                myogg.update(self.tags)
                myogg.save()
            except:
                warn('Could not save the tags')
                import traceback
                traceback.print_exc()
                return False
        elif self.songwav != self.song or 'cd-' in self.decoder:
            warn('No tags found...')

        if self.conf.delete_input:
            os.remove(self.song)
        return True

class ConvertTrack(Convert):
    '''Wrapper around Convert for CD Tracks'''
    def __init__(self, device, conf, track, tags):
        self.device, self.track, self.tags, self.conf = device, track, tags, conf
        self.song    = ''
        self.songwav = "audio.wav"
        self.songogg = "%(artist)s/%(album)s/%(ntracknumber)s - %(title)s.ogg" % tags
        self.conf.preserve_wav = False
        self.decoder           = 'cd-' + self.conf.cd_decoder
        self.convert()

class ConvertDisc(object):
    '''Wrapper around ConvertTrack to Convert complete cds
    Currently uses MusicBrainz, but a CDDB fallback will be added, too.'''
    def __init__(self, dev, conf):
        warn("Converting CDs is not well supported, please use another "
             "solution.")
        self.dev, self.conf = dev, conf
        try:
            self.get_mb()
        except self.MBError:
            warn('MusicBrainz failed. Trying FreeDB...')
            self.get_cddb()

    class MBError(Exception):
        '''Empty'''

    def get_cddb(self):
        try:
            import CDDB, DiscID
        except ImportError:
            fatal('You need python-cddb (http://cddb-py.sf.net) to convert cds. Please install it.')

        disc_id    = DiscID.disc_id(DiscID.open(self.dev))
        query_info = CDDB.query(disc_id)[1]
        if not query_info:
            fatal('The disk is not listed in FreeDB, dir2ogg only supports disk listed in MusicBrainz or FreeDB')
        if isinstance(query_info, list):
            query_info = query_info[0]
        read_info = CDDB.read(query_info['category'], query_info['disc_id'])[1]

        for track in range(disc_id[1]):
            title           = {}
            title['discid'] = query_info['disc_id']
            title['artist'], title['album'] = (track.strip() for track in query_info['title'].split("/"))
            title['genre']  = read_info['DGENRE']
            title['date']   = read_info['DYEAR']
            title['title']  = read_info['TTITLE' + str(track)]
            title['tracktotal'] = str(len(list(range(disc_id[1]))) + 1)
            title['ntracknumber'] = '0' * (len(title['tracktotal'] ) - len(str(track+1)) ) + str(track+1)
            title['tracknumber'] = str(track+1)
            for key, val in list(title.items()):
                title[key] =  str(str(val), "ISO-8859-1")
            ConvertTrack(self.dev, self.conf, track+1, title)

    def get_mb(self):
        try:
            import musicbrainz2.disc as mbdisc
            import musicbrainz2.webservice as mbws
        except ImportError as err:
            warn('You need python-musicbrainz2 (or python-cddb) to convert cds. Please install it. Trying cddb.')
            raise self.MBError(err)

        service = mbws.WebService()
        query = mbws.Query(service)

        # Read the disc in the drive
        try:
            disc = mbdisc.readDisc(self.dev)
        except mbdisc.DiscError as err:
            warn(err)
            raise self.MBError

        discId = disc.getId()
        try:
            myfilter = mbws.ReleaseFilter(discId=discId)
            results = query.getReleases(myfilter)
        except mbws.WebServiceError as err:
            warn(err)
            raise self.MBError

        if len(results) == 0:
            print("Disc is not yet in the MusicBrainz database.")
            print("Consider adding it via", mbdisc.getSubmissionUrl(disc))
            raise self.MBError
        try:
            inc = mbws.ReleaseIncludes(artist=True, tracks=True, releaseEvents=True)
            release = query.getReleaseById(results[0].release.getId(), inc)
        except mbws.WebServiceError as err:
            warn(err)
            raise self.MBError

        isSingleArtist = release.isSingleArtistRelease()

        try:
            # try to get the CDDB ID
            import DiscID
            cddb_id = '%08lx' % int(DiscID.disc_id(DiscID.open(self.dev))[0])
        except:
            cddb_id = False

        trackn = 1
        for track in release.tracks:
            title           = {}
            title['artist'] = isSingleArtist and release.artist.name or track.artist
            if cddb_id:
                title['discid'] = cddb_id
            title['album']  = release.title
            title['date']   = release.getEarliestReleaseDate()
            title['musicbrainz_albumartistid'] = release.artist.id.split("/")[-1]
            title['musicbrainz_albumid'] = release.id.split("/")[-1]
            title['musicbrainz_discid'] = discId
            title['musicbrainz_sortname'] = release.artist.sortName
            title['musicbrainz_trackid'] = track.id.split("/")[-1]
            title['title']  = track.title
            title['tracktotal'] = str(len(release.tracks))
            title['ntracknumber'] = "%02d" % trackn
            title['tracknumber'] = str(trackn)
            ConvertTrack(self.dev, self.conf, trackn, title)
            trackn+=1

class ConvertDirectory(object):
    '''
    This class is just a wrapper for Convert.

    Grab the songs to convert, then feed them one
    by one to the Convert class.
    '''

    def __init__(self, conf, directory, files):
        ''' Decide which files will be converted.'''
        if os.path.exists(directory) == 0:
            fatal('Directory: "%s" not found' % directory)

        self.directory = directory = os.path.normpath(directory) + os.path.sep
        self.songs = mmatch(files, conf.filters, False)

        if conf.verbose:
            self.print_if_verbose()

        for song in self.songs:
            try:
                Convert(directory + song, conf)
            except:
                warn('File: %s error in ogg conversion' % directory + song)
                

    def print_if_verbose(self):
        ''' Echo files to be converted if verbose flag is set.'''
        info('In %s I am going to convert:' % self.directory)
        for song in self.songs:
            print(" ", song)


def show_banner():
    print('dir2ogg %s (%s), converts audio files into ogg vorbis.\n' % (__version__, __date__))

def show_license(*args, **kwargs):
    print('Copyright (C) 2007-2008 Julian Andres Klode <jak@jak-linux.org>')
    print('Copyright (C) 2003-2006 Darren Kirby <d@badcomputer.org>\n')
    print('This program is distributed in the hope that it will be useful,')
    print('but WITHOUT ANY WARRANTY; without even the implied warranty of')
    print('MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
    print('GNU General Public License for more details.\n')
    print('Currently developed by Julian Andres Klode <jak@jak-linux.org>.')
    sys.exit(0)

def main():
    conf = read_opts()
    conf_args, conf = conf[1], conf[0]
    if conf.cdda:
        discs = len(conf_args) and conf_args or ("/dev/cdrom",)
        for disc in discs:
            ConvertDisc(disc, conf)
    elif conf.directory or conf.recursive:
        rdirs = {}
        for path in conf_args:
            if not os.path.isdir(path):
                fatal('Path: %s does not exists' % path)
            elif conf.recursive:
                rdirs.update(return_dirs(path))
            elif conf.directory:
                rdirs.update({path: os.listdir(path)})
        for directory, files in list(rdirs.items()):
            try:
                ConvertDirectory(conf, directory, files)
            except:
                warn('DIR: %s ;Files: %s error in ogg conversion' % (directory,files))
    else:
        for path in conf_args:
            if not os.path.isfile(path):
                fatal('Path: %s does not exists' % path)
        for filename in conf_args:
            try:
                Convert(filename, conf)
            except:
                warn('File: %s error in ogg conversion' % filename)
                

    sys.exit(0)

if __name__ == '__main__':
    main()
