#!/usr/bin/python
# -*- coding: UTF8 -*
'''
This is a copy of mprisV2.2 documentation

http://specifications.freedesktop.org/mpris-spec/latest/

That also works as python lib.



Version 2.2
===========
Copyright © 2006-2010 the VideoLAN team(Mirsal Ennaime, Rafaël Carré, Jean-Paul Saman)

Copyright © 2005-2008 Milosz Derezynski

Copyright © 2008 Nick Welch

Copyright © 2010-2012 Alex Merry

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.



About
=====
The Media Player Remote Interfacing Specification is a standard D-Bus interface which aims to provide a common programmatic API for controlling media players.

It provides a mechanism for compliant media players discovery, basic playback and media player state control as well as a tracklist interface which is used to add context to the current item.



Changes
=======
 Changes (Permalink)

From 2.1 to 2.2:

* Added the optional Fullscreen and CanSetFullscreen properties to the org.mpris.MediaPlayer2 interface.
* The path /org/mpris/MediaPlayer2/TrackList/NoTrack now represents "no track" where required in the org.mpris.MediaPlayer2.TrackList interface (since empty paths are not allowed by D-Bus).
* The suggested unique instance identifier no longer violates the D-Bus specification by begining with a digit.


From 2.0 to 2.1:

* Added the optional org.mpris.MediaPlayer2.Playlists interface.



Bus Name Policy
===============
Each media player *must* request a unique bus name which begins with *org.mpris.MediaPlayer2*. For example:

* org.mpris.MediaPlayer2.audacious
* org.mpris.MediaPlayer2.vlc
* org.mpris.MediaPlayer2.bmp
* org.mpris.MediaPlayer2.xmms2

This allows clients to list available media players (either already running or which can be started via D-Bus activation)

In the case where the media player allows multiple instances running simultaneously, each additional instance should request a unique bus name, adding a dot and a unique identifier to its usual bus name, such as one based on a UNIX process id. For example, this could be:

* org.mpris.MediaPlayer2.vlc.7389

Note: According to the D-Bus specification, the unique identifier "must only contain the ASCII characters '[A-Z][a-z][0-9]_-'" and "must not begin with a digit". 

Entry point
===========
The media player *must* expose the */org/mpris/MediaPlayer2* object path, which *must* implement the following interfaces:

* :doc:`org.mpris.MediaPlayer2<../mpris2.mediaplayer2>`
* :doc:`org.mpris.MediaPlayer2.Player<../mpris2.player>`

The */org/mpris/MediaPlayer2* object may implement the :doc:`org.mpris.MediaPlayer2.TrackList<../mpris2.tracklist>` interface.

The */org/mpris/MediaPlayer2* object may implement the :doc:`org.mpris.MediaPlayer2.Playlists<../mpris2.playlists>` interface.


The PropertiesChanged signal
============================
The MPRIS uses the org.freedesktop.DBus.Properties.PropertiesChanged signal to notify clients of changes in the media player state. If a client implementation uses D-Bus bindings which do not support this signal, then it should connect to it manually. If a media player implementation uses D-Bus bindings which do not support this signal, then it should send it manually


Corrections
===========
2010-09-26: Added EmitsChangedSignal annotation to Volume property on the Player interface.

2011-01-26: Added PlaylistChanged signal to the Playlists interface.


Interfaces
==========
* :doc:`org.mpris.MediaPlayer2<../mpris2.mediaplayer2>`
* :doc:`org.mpris.MediaPlayer2.Player<../mpris2.player>`
* :doc:`org.mpris.MediaPlayer2.Playlists<../mpris2.playlists>`
* :doc:`org.mpris.MediaPlayer2.TrackList<../mpris2.tracklist>`


'''

from .interfaces import Interfaces
from .mediaplayer2 import MediaPlayer2
from .player import Player
from .playlists import Playlists
from .tracklist import TrackList
from .utils import get_players_uri
from .some_players import Some_Players as SomePlayers
