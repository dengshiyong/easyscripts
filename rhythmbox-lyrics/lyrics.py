#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2009-04-03

import rb

class Lyrics(rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)
        from dbus.mainloop.glib import DBusGMainLoop
        import gobject
        from mod_dbus import LyricsDBus
        DBusGMainLoop(set_as_default=True)
        dbus_loop = gobject.MainLoop()
        self.__lybus = LyricsDBus()

    def activate(self,shell):
        print "CALL activate: %s" % ( str(shell) )
        self.__lybus.connect()

    def deactivate(self,shell):
        print "CALL deactivate: %s" % ( str(shell) )
        self.__lybus.disconnect()

