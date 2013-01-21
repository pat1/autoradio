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
import os,stat,time,urlparse,urllib
import gobject

def convert_ns(t):
    s,ns = divmod(t, 1000000)
    m,s = divmod(s, 60)
    
    if m < 60:
      return "%02i:%02i" %(m,s)
    else:
      h,m = divmod(m, 60)
    return "%i:%02i:%02i" %(h,m,s)


class Main(object):

  def delete_event(self, widget, event, data=None):
    gtk.main_quit()
    return False
 
  def playhandler(self, *args, **kw): 
      #print args, kw
      playbackstatus = args[2].get("PlaybackStatus",None)
      position = args[2].get("Position",None)
      if playbackstatus is not None:
          print "PlaybackStatus",playbackstatus

      if position is not None:
          length=self.tl.GetTracksMetadata((self.play.Metadata.get(u'mpris:trackid',None),))[0].get(u'mpris:length',None)
          #print "Position", position,length
          frac = float(position)/float(length)
          self.pbar.set_fraction(frac)
      else:
          self.pbar.pulse()
          

  def __init__(self):

    self.multimedia_file=None

    #Connect to player
    DBusGMainLoop(set_as_default=True)
    uris = get_players_uri(pattern=".")

    if len(uris) >0 :
        uri=uris[0]
        self.mp2 = MediaPlayer2(dbus_interface_info={'dbus_uri': uri})
        self.play = Player(dbus_interface_info={'dbus_uri': uri})
    else:
        print "No players availables"
        return
    
    if self.mp2.HasTrackList:
      self.tl = TrackList(dbus_interface_info={'dbus_uri': uri})
      #tl.PropertiesChanged = trackhandler

    else:
      self.tl = None

    self.play.PropertiesChanged = self.playhandler

    # Create the GUI
    self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)

    self.win.set_size_request(400, 300)
    self.win.set_title("AutoPlayer gui")
    self.win.connect("delete_event", self.delete_event)
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

#        # Create a centering alignment object
#    align = gtk.Alignment(0.5, 0.5, 0, 0)
#    vbox.pack_start(align, False, False, 5)
#    align.show()


    # Create the ProgressBar
    self.pbar = gtk.ProgressBar()
    self.pbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
    self.pbar.set_fraction(.5)
    hbox.pack_start(self.pbar)
    self.pbar.show()

    vbox.pack_start(self.load_file, False, True, 0)
    vbox.pack_start(hbox, False, True, 0)

#    vbox.pack_start(self.pbar)
#    self.pbar.show()
#    self.pbar.pulse()
    #separator = gtk.HSeparator()
    #vbox.pack_start(separator, False, False, 0)

        # create the TreeView
    column_names = ['ID', 'Len', 'Artist', 'Title']
    cell_data_funcs = (self.id, self.Len, self.Artist,self.Title)

    self.treeview = gtk.TreeView()
 
        # create the TreeViewColumns to display the data
    self.tvcolumn = [None] * len(column_names)
    listmodel = self.make_list()

    for n in range(0, len(column_names)):
      cell = gtk.CellRendererText()
      self.tvcolumn[n] = gtk.TreeViewColumn(column_names[n], cell)
      if n == 1:
        cell.set_property('xalign', 1.0)
      self.tvcolumn[n].set_cell_data_func(cell, cell_data_funcs[n])
      self.treeview.append_column(self.tvcolumn[n])

    self.treeview.connect('row-activated', self.open_file)
    self.scrolledwindow = gtk.ScrolledWindow()
    self.scrolledwindow.add(self.treeview)
    vbox.pack_start(self.scrolledwindow, True, True, 0)
    self.treeview.set_model(listmodel)
    self.win.add(vbox)
    self.win.show_all()

    gobject.timeout_add(  1000,self.update)


  def update(self):
      new_model = self.make_list()
      self.treeview.set_model(new_model)
      return True

  def on_file_selected(self, widget):
    self.multimedia_file = self.load_file.get_filename()
  def on_play_clicked(self, widget):
    if self.multimedia_file is None:
        self.play.Play()
    else:
        url=urlparse.urlsplit(self.multimedia_file)
        uri=urlparse.urljoin("file://",urllib.unquote(url.path))
        self.play.OpenUri(uri)
        self.multimedia_file=None
        new_model = self.make_list()
        self.treeview.set_model(new_model)

  def on_pause_clicked(self, widget):
    self.play.PlayPause()
  def on_stop_clicked(self, widget):
    self.play.Stop()

  def open_file(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        self.tl.GoTo(model.get_value(iter, 0))
        new_model = self.make_list()
        self.treeview.set_model(new_model)

  def make_list(self):
    listmodel = gtk.ListStore(object)

    if self.tl is not None:
      # attributes and methods together
      for track in  self.tl.GetTracksMetadata( self.tl.Tracks):
        listmodel.append([track.get(u'mpris:trackid',"")])
    return listmodel

  def id(self, column, cell, model, iter):
        cell.set_property('text', model.get_value(iter, 0))
        if model.get_value(iter, 0) == self.play.Metadata.get(u'mpris:trackid',None):
            cell.set_property('cell-background',"red")
        else:
            cell.set_property('cell-background',"green")
        return

  def Len(self, column, cell, model, iter):
    track=self.tl.GetTracksMetadata((model.get_value(iter, 0),))
    cell.set_property('text', convert_ns(track[0].get(u'mpris:length',"")))
    return

  def Artist(self, column, cell, model, iter):
    track=self.tl.GetTracksMetadata((model.get_value(iter, 0),))
    cell.set_property('text', track[0].get(u'xesam:artist',""))
    return

  def Title(self, column, cell, model, iter):
    track=self.tl.GetTracksMetadata((model.get_value(iter, 0),))
    cell.set_property('text', track[0].get(u'xesam:title',""))
    return
      
if __name__ == "__main__":
    Main()
    gtk.main()
