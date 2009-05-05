#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2009-04-03

import os

import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

from mod_sogou import LyricsSearch
from mod_locate import LyricsLocate


class LyricsDBus :
    def __init__(self):
        print "CALL LyricsDBus __init__"
        self.__handlers = []
        self.__player = None
        self.__shell = None
        self.__elapsed = -1
        self.__lyfilename = None
        self.artist = None
        self.title = None

    def __set_uri(self,uri):
        print "CALL LyricsDBus __set_uri (%s)" % uri
        if uri is not None and uri != "" :
            self.__uri = uri
            self.__shell.getSongProperties(uri,
                    reply_handler=self.__set_song_properties,
                    error_handler=self._report_dbus_error)
        else:
            self._set_no_song()

    def __set_song_properties(self,prop):
        print "CALL LyricsDBus __set_song_properties"
        self.title = prop.get("title")
        self.artist = prop.get("artist")
        self.__lyfilename = "%s/.lyrics/%s/%s.lyric" % (os.getenv("HOME"),self.artist,self.title)

        if not os.path.exists(self.__lyfilename) :
            lines = self.__lys.searchLyric(self.title,self.artist)
            if lines != [] :
                self.__lys.saveLyric(lines)

        self.__loc.Reset()

    def __set_playing(self,playing):
        print "CALL LyricsDBus __set_playing (%s)" % playing
        self.playing = playing
        self.__loc.Reset()

        if not self.playing and self.__elapsed < 0 :
            self._set_no_song()

    def __set_elapsed(self, elapsed):
        #print "CALL LyricsDBus __set_elapsed (%s) " % elapsed
        self.__elapsed = elapsed

        self.__loc.LyricsShow(self.__lyfilename,self.__elapsed)

        if not self.playing and self.__elapsed < 0 :
            self._set_no_song()

    def __property_changed(self,uri,prop,old_val,new_val):
        print "CALL LyricsDBus __property_changed (%s|%s|%s|%s)" % ( uri,prop,old_val,new_val)
        if prop == "title":
            self.title = new_val
        elif prop == "artist":
            self.artist = new_val
        self.__lyfilename = "%s/.lyrics/%s/%s.lyric" % (os.getenv("HOME"),self.artist,self.title)
        self.__loc.Reset()

    def connect (self):
        print "CALL LyricsDBus connect"
        if self.__player is not None:
            return

        bus = dbus.SessionBus ()
        proxy = bus.get_object ("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Player")
        self.__player = dbus.Interface (proxy, "org.gnome.Rhythmbox.Player")

        proxy = bus.get_object ("org.gnome.Rhythmbox", "/org/gnome/Rhythmbox/Shell")
        self.__shell = dbus.Interface (proxy, "org.gnome.Rhythmbox.Shell")

        self.__handlers = [
                self.__player.connect_to_signal ("playingChanged", self.__set_playing),
                self.__player.connect_to_signal ("elapsedChanged", self.__set_elapsed),
                self.__player.connect_to_signal ("playingUriChanged", self.__set_uri),
                self.__player.connect_to_signal ("playingSongPropertyChanged", self.__property_changed),
                ]

        self.__player.getPlaying (reply_handler=self.__set_playing,
                error_handler=self._report_dbus_error)

        self.__player.getElapsed (reply_handler=self.__set_elapsed,
                error_handler=self._report_dbus_error)

        self.__player.getPlayingUri (reply_handler=self.__set_uri,
                error_handler=self._report_dbus_error)
        
        self.__loc = LyricsLocate()
        self.__lys = LyricsSearch()

        self.connected = True

    def disconnect(self):
        print "CALL LyricsDBus disconnect"
        for handler in self.__handlers:
            handler.remove()
        self.__handlers = []
        self.__player = None
        self.__shell = None
        self.__loc = None
        self.__lys = None

    def _set_no_song(self):
        print "CALL LyricsDBus _set_no_song"
        self.__loc.Reset()

    def _report_dbus_error(self,err):
        print "CALL LyricsDBus _report_dbus_error"

if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    dbus_loop = gobject.MainLoop()

    lybus = LyricsDBus()
    lybus.connect()

    dbus_loop.run()

