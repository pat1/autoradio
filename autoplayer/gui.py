#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GPL. (C) 2013 Paolo Patruno.

from mpris2.mediaplayer2 import MediaPlayer2
from mpris2.player import Player
from mpris2.tracklist import TrackList
from mpris2.interfaces import Interfaces
from mpris2.some_players import Some_Players
from mpris2.utils import get_players_uri
from dbus.mainloop.glib import DBusGMainLoop
from mpris2.utils import get_session
import pygtk, gtk

class Main(object):
  def __init__(self):
    self.multimedia_file=None
    # Create the GUI
    self.win = gtk.Window()
    self.win.set_title("Play Video Example")
    self.win.connect("delete_event",
    lambda w,e: gtk.main_quit())
    vbox = gtk.VBox(False, 0)
    hbox = gtk.HBox(False, 0)
    self.load_file = gtk.FileChooserButton("Choose Audio File")
    self.play_button = gtk.Button("Play", gtk.STOCK_MEDIA_PLAY)
    self.pause_button = gtk.Button("Pause", gtk.STOCK_MEDIA_PAUSE)
    self.stop_button = gtk.Button("Stop", gtk.STOCK_MEDIA_STOP)
    self.load_file.connect("selection-changed",self.on_file_selected)
    self.play_button.connect("clicked", self.on_play_clicked)
    self.pause_button.connect("clicked", self.on_pause_clicked)
    self.stop_button.connect("clicked", self.on_stop_clicked)
    hbox.pack_start(self.play_button, False, True, 0)
    hbox.pack_start(self.pause_button, False, True, 0)
    hbox.pack_start(self.stop_button, False, True, 0)
    vbox.pack_start(self.load_file, False, True, 0)
    vbox.pack_start(hbox, False, True, 0)
    self.win.add(vbox)
    self.win.show_all()

    #Connect to player
    DBusGMainLoop(set_as_default=True)
    uris = get_players_uri(pattern=".")

    if len(uris) >0 :
        uri=uris[0]
        self.mp2 = MediaPlayer2(dbus_interface_info={'dbus_uri': uri})
        self.play = Player(dbus_interface_info={'dbus_uri': uri})
    else:
        print "No players availables"

  def on_file_selected(self, widget):
    self.multimedia_file = self.load_file.get_filename()
  def on_play_clicked(self, widget):
    if self.multimedia_file is None:
      self.play.Play()
    else:
      self.play.OpenUri("file://" + self.multimedia_file)
      self.multimedia_file=None
  def on_pause_clicked(self, widget):
    self.play.PlayPause()
  def on_stop_clicked(self, widget):
    self.play.Stop()
      
if __name__ == "__main__":
  Main()
  gtk.main()
