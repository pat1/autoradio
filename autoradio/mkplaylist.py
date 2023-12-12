#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:          mkplaylist.py
# Purpose:       ReCreate playlists from directory scans or m3u playlist.
#
# Author:        Marc 'BlackJack' Rintsch
#                Paolo Patruno
# Created:       2004-11-09
# Last modified: 2012-08-04
# Copyright:     (c) 2004-2009
# Licence:       GPL
#-----------------------------------------------------------------------------
"""Make a playlist file.

:var factory: instance of a `PlaylistEntryFactory`.
:var WRITERS: dictionary that maps playlist format names to functions
    that write a sequence of `PlaylistEntry` objects in that format
    to a file.

:todo: Check if docstrings and code are still in sync.
:todo: Refactor cache code.  Introduce a Cache class.  Maybe subclassing
    `PlaylistEntryFactory` with a caching version.  Keep in mind that this
    scales, i.e. implementing an SQLite cache or using AmaroK's db should be
    considered too.
:todo: Find a strategically favourable place to minimise the contents of the
    meta data dictionaries to the bare minimum to cut down the cache file size.
    It is not necessary to have the version of the vorbis library in ogg meta
    data for example.
"""
from past.builtins import cmp
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
import sys
import os
import os.path
import random
import logging
from itertools import chain
import mutagen
import urllib.request, urllib.error, urllib.parse

__author__ = "Marc 'BlackJack' Rintsch <marc(at)rintsch(dot)de>"
__version__ = '0.6.0'
__date__ = '$Date: 2012-11-26 $'

__docformat__ = 'reStructuredText'

# Disable `pylint` name convention warning for names on module level that
# are not ``def``\ed functions and still have no conventional constant names,
# i.e. only capital letters.
# 
# pylint: disable-msg=C0103

#
# Use logging for ouput at different *levels*.
#
logging.getLogger().setLevel(logging.INFO)
log = logging.getLogger("mkplaylist")
handler = logging.StreamHandler(sys.stderr)
log.addHandler(handler)

#-----------------------------------------------------------------------------
# Functions to read meta data from media files.
#
# now use mutagen
#
# The functions return a dictionary with the meta data.  The minimal
# postcondition is an empty dictionary if no information could be
# read from the file.
#
# Keys to use (yes, they are all uppercase!):
#
# ARTIST, TITLE, TIME (playing time in seconds)
#
# All other keys are currently not used by any output format.


def metadata_reader(path):
    """Reads info from media file."""
    
    info = dict()

    if path[:5] == "http:":
        info['TIME'] = None
        info['ARTIST'] = "streaming"
        info['ALBUM'] = "streaming"
        info['TITLE'] = path
        
    else:

        try:
            m=mutagen.File(path,easy=True)
            # in seconds (type float).

            info['TIME'] = m.info.length

            for value_name, key in (('artist', 'ARTIST'),
                                    ('album', 'ALBUM'),
                                    ('title', 'TITLE')):
                value = m.get(value_name)
                if value:
                    info[key] = value[0]

        except:
            log.info("Could not read info from file: %s ",path)


    return info


#-----------------------------------------------------------------------------

class PlaylistEntry(object):
    """A generic playlist entry with a `path` attribute and dictionary
    like behavior for meta data.
    
    `PlaylistEntry` objects can be converted to strings and are
    comparable with their `path` attribute as key.
    
    The meta data contains at least the path of the media file.
    
    :ivar path: path of the media file.
    :type path: str
    :ivar metadata: meta data of the media file.
    :type metadata: dict of str -> str
    
    :invariant: self['path'] is not None
    """
    def __init__(self, path, metadata=None):
        """Creates a playlist entry.
        
        :param path: the path of the media file.
        :type path: str
        :param metadata: a dictionary with meta data.
        :type metadata: dict of str -> str
        
        :precondition: The meta data must not contain a key 'path'.
        :postcondition: The meta data contains the `path` as key.
        """
        self.path = path
        
        if metadata is None:
            metadata = dict()
        
        metadata['PATH'] = self.path
        self.metadata = metadata
        
        
        # TODO: Some black magic to fill the metadata from examining
        #       the file name if the dict is empty.
    
    def __getitem__(self, key):
        return self.metadata.get(key, '')
    
    def __setitem__(self, key, value):
        self.metadata[key] = value
        if key == 'PATH':
            self.path = key
    
    def __cmp__(self, other):
        return cmp(self.path, other.path)
        
    def __str__(self):
        return self.path

    def __unicode__(self):
        try:
            return self.path.decode("UTF-8")
        except:
            log.info("Could not decode UTF-8: %s ",self.path)
            return ""

class PlaylistEntryFactory(object):
    """A media file factory allows registritation of media file types,
    their file name extensions and functions for reading meta data from
    the files.
    
    This is not a "real" class but more an abuse of a class as a
    namespace.  If the program grows so large that it will become
    unavoidable to split it into several modules, the contents of
    this class may be moved to the top level of a module.
    
    :ivar types: dictionary that maps a file name extension to a
        tuple containing a descriptive name of the type and a
        sequence of functions to read meta data from this file type.
    :type types: dict
    :ivar cachefile: pathname of a file to store the pickled data from cached 
        PlaylistEntries
    :type cachefile: string
    """
    def __init__(self):
        pass

    def is_media_file(self, path):
        """Check file if it is a known media file.

        The check is based on mutagen file test

        :param path: filename of the file to check.
        :type path: str

        :returns: `True` if known media file, `False` otherwise.
        :rtype: bool
        """
        try:
            return not mutagen.File(path) is None
        except:
            return False

    def is_media_url(self, path):
        """Check file if it is a url.

        The check is based on the prefix thet will be http:
        :param path: filename of the file to check.
        :type path: str

        :returns: `True` if url, `False` otherwise.
        :rtype: bool
        """
        return path[:5] in  ("http:","file:")
    


    def create_entry(self, path):
        """Reads metadata and returns PlaylistEntry objects.
        
        :param path: path to the media file.
        :type path: str
        
        :return: dictionary with meta data.
        :rtype: dict of str -> str
        """

        playlist_entry = PlaylistEntry(path, metadata_reader(path))
        log.debug("(new)")
        return playlist_entry

#
# Create a PlaylistEntryFactory instance and populate it with the
# known file extensions.
#
factory = PlaylistEntryFactory()


#-----------------------------------------------------------------------------
# Playlist writers.

def write_m3u(playlist, outfile,timelen=None):
    """Writes the playlist in m3u format."""
    
    totaltime=0.
    i=0 
    for entry in playlist:
        if not  entry['TIME'] is None :
            totaltime += entry['TIME']
        else:
            if not timelen is None :
                log.error("error evalutate time length on file: %s ",entry )
                continue

        if totaltime < timelen or timelen is None :
            print(str(entry), file=outfile)
            i+=1
        else:
            break

    log.info("That's %d out file(s).", i)

def write_extm3u(playlist, outfile,timelen=None):
    """Writes the playlist in extended m3u format."""
    
    totaltime=0.
    i=0 
    print('#EXTM3U', file=outfile)
    for entry in playlist:
        if not  entry['TIME'] is None :
            totaltime += entry['TIME']
        else:
            if not timelen is None :
                log.error("error evalutate time length on file: %s",entry )
                continue

        if totaltime < timelen  or timelen is None :
            time=entry['TIME']
            if time is None : time = -1
            if entry['ARTIST'] and entry['TITLE']:
                print('#EXTINF:%s,%s - %s' % (time,
                                                      entry['ARTIST'],
                                                      entry['TITLE']), file=outfile)
        
            print(str(entry), file=outfile)
            i+=1
        else:

            break

    log.info("That's %d out file(s).", i)

def write_pls(playlist, outfile,timelen=None):
    """Write the `playlist` in PLS format.
    
    :todo: Guess playlist name from `outfile.name`.
    :todo: Add command line option for playlist title.
    """
    totaltime=0.
    print('[playlist]', file=outfile)
    print('PlaylistName=Playlist', file=outfile)
    i = 0
    for i, entry in enumerate(playlist):
        if not  entry['TIME'] is None :
            totaltime += entry['TIME']
        else:
            log.error("evaluate time length on file: %s",entry )
            continue

        if totaltime < timelen  or timelen is None :

            i += 1
            print('File%d=%s' % (i, entry), file=outfile)
            title = entry['TITLE'] or os.path.basename(str(entry))
            print('Title%d=%s' % (i, title), file=outfile)
            print('Length%d=%s' % (i, entry['TIME']), file=outfile)

        else:

            break

    print('NumberOfEntries=%d' % i, file=outfile)
    print('Version=2', file=outfile)
    log.info("That's %d out file(s).", i)


WRITERS = { 'm3u': write_m3u,
            'extm3u': write_extm3u,
            'pls': write_pls }

#-----------------------------------------------------------------------------



def read_playlist(infile, absolute_paths=True):
    """Iterates over media files in playlist.
    
    Extended M3U directives are skipped.
    
    :param infile: filename of playlist
    :type infile: str
    :param absolute_paths: converts relative path names to absolute ones
        if set to `True`.
    :type absolute_paths: bool
    
    :returns: iterator over `PlaylistEntry` objects.
    :rtype: iterable of `PlaylistEntry`
    """

    root  = os.getcwd()

    if infile == '-':
        finfile = sys.stdin
    else:
        finfile = file(infile, "r")
        root  =  os.path.join(root , os.path.dirname(infile))
    
    log.debug("root dir: %s", root)

    for filename in  finfile.read().strip().split("\n"):

        log.debug("entry: %s", filename)

        if len(filename) == 0 or filename[0] == "#": # skip empty and comment lines
            log.debug("ignore %s", filename)
            continue

        # convert thinks like %20 in file name
        filename=urllib2.url2pathname(filename)
        if filename[:7] == "file://" :
            filename=filename[7:]

        if factory.is_media_file(filename):
            log.debug("found %s", filename)
            if filename[0] != "/" :
                full_name = os.path.join(root, filename)
            else:
                full_name=filename

            log.debug("full_name: %s", full_name)

            if not os.path.isfile(full_name):
                log.info("ignore %s do not exist", full_name)
                continue
    
            if absolute_paths:
                full_name = os.path.abspath(full_name)
            else:
                l=len(os.path.commonprefix((root,full_name)).rpartition("/")[0])
                if l>0 :
                    full_name=full_name[l+1:]

            log.debug("post full_name: %s", full_name)

            yield factory.create_entry(full_name)

        elif  factory.is_media_url(filename):
            yield factory.create_entry(filename)

        else:
            log.info("ignore %s", filename)

    finfile.close()


def search(path, absolute_paths=True):
    """Iterates over media files in `path` (recursivly).
    
    Symlinked directories are skipped to avoid endless
    scanning due to possible cycles in directory structure.
    
    :param path: root of the directory tree to search.
    :type path: str
    :param absolute_paths: converts relative path names to absolute ones
        if set to `True`.
    :type absolute_paths: bool
    
    :returns: iterator over `PlaylistEntry` objects.
    :rtype: iterable of `PlaylistEntry`
    """
    for (root, dummy, filenames) in os.walk(path):
        log.info("Scanning %s...", root)
        # TODO: Check if there are linked directories.
        for filename in filenames:
            full_name = os.path.join(root, filename)
            if factory.is_media_file(full_name):
                log.debug("found %s", filename)
                if absolute_paths:
                    full_name = os.path.abspath(full_name)
                yield factory.create_entry(full_name)


def main():
    """Main function."""
    
    import codecs
    from optparse import OptionParser
    
    usage = ("usage: %prog [-h|--help|--version]\n"
             "       %prog [options] directory [directory ...]")
    
    parser = OptionParser(usage=usage, version="%prog " + __version__)
    parser.add_option("-i", "--input", type="string", dest="infile",
                     default='-',
                     help="name of the m3u playlist input file or '-' for stdout (default)")
    parser.add_option("-t", "--timelen", type="float", dest="timelen",
                     default=None,
                     help="Len of Playlist in seconds (default= infinite)")
    parser.add_option("-o", "--output", type="string", dest="outfile",
                     default='-',
                     help="name of the output file or '-' for stdout (default)")
    parser.add_option("-f", "--output-format", type="choice",
                      dest="output_format", default="extm3u",
                      choices=list(WRITERS.keys()),
                      help="format of the output %r (default: %%default)" %
                            list(WRITERS.keys()))
    parser.add_option("-r", "--relative-paths", action="store_true",
                      dest="relative_paths", default=False,
                      help="write relative paths. (default: absolute paths)")
    parser.add_option("--shuffle", action="store_true", default=False,
                      help="shuffle the playlist before saving it.")
    parser.add_option("--sort", action="store_true", default=False,
                      help="sort the playlist before saving it.")
    parser.add_option("-v", "--verbose", action="store_true", default=False,
                      dest="verbose", help="be more verbose.")
    parser.add_option("-q", "--quiet", action="store_true", default=False,
                      dest="quiet", help="be really quiet.")
    
    (options, args) = parser.parse_args()
    
#    if len(args) == 0:
#        parser.error("wrong number of arguments")
    
    write_playlist = WRITERS[options.output_format]
    
    if options.quiet:
        log.setLevel(logging.WARNING)
    
    if options.verbose:
        log.setLevel(logging.DEBUG)
    
    #
    # Input.
    #

    if len(args) == 0:

        log.info("Read %s file.", options.infile)
        media_files=list(read_playlist(options.infile, not options.relative_paths))
    

    else:
        media_files = list(chain(*[search(path, not options.relative_paths)
                               for path in args]))
    
    #
    # Processing.
    #
    if options.shuffle:
        random.shuffle(media_files)
    elif options.sort:
        media_files.sort()


    #
    # Output.
    #
    outfile = sys.stdout
    if options.outfile != '-':
        #outfile = file(options.outfile, "w")
        outfile = codecs.open(options.outfile, "w", encoding="UTF-8")

    write_playlist(media_files, outfile,options.timelen)
    outfile.close()
    
    log.info("That's %d good input file(s).", len(media_files))
    
if __name__ == '__main__':
    main()
