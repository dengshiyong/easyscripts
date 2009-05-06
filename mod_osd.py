#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2008-12-27 22:16:45

import os
import pyosd # python-osd

class LyricsOSD :
    def __init__(self):
        print "CALL LyricsOSD __init__"
        self.__OSD=None
        self.__initOSD()

    def __initOSD(self):
        print "CALL LyricsOSD __initOSD"
        import imp, ConfigParser
        CONF="""
[OSD]
# lines>1 to display muti-line,significantly reduce the rate of compiz. BUG ??
lines=1
# font shadow
shadow=1
# ALIGN_CENTER=1 ALIGN_LEFT=0 ALIGN_RIGHT=2
align=1
# font color
colour=#FFFFFF
# font
font=-*-bookman-*-*-*-*-34-*-*-*-*-*-*-*,-*-kai-*-*-*-*-48-*-*-*-*-*-*-*
# POS_BOT=1 POS_MID=2 POS_TOP=0
pos=1
# timeout,delay before lyric disappear
timeout=10
# horizontal offset
hoffset=0
# vertical offset, skip status-bar --> 30
offset=30

### not support yet :-(
noLocale=False
# set_outline_colour
outline_colour="#00FF00"
# set_outline_offset
outline_offset="#FFFFFF"
# set_shadow_colour
shadow_colour="#FFFFFF"
# set_shadow_offset
shadow_offset="#FFFFFF"

"""
        inifile = imp.find_module('mod_osd')[1]
        inifile = os.path.dirname(inifile) + "/configure"
        try:
            f = open(inifile,'r')
        except:
            f = open(inifile,'w+')
            f.write(CONF)
            f.seek(0)

        conf = ConfigParser.ConfigParser()
        conf.readfp( f )

        try:
            v_lines = conf.getint("OSD","lines")
        except:
            v_lines = 1

        try:
            v_shadow = conf.getint("OSD","shadow")
        except:
            v_shadow = 1

        self.__OSD=pyosd.osd(lines=v_lines,shadow=v_shadow)

        if self.__OSD==None:
            self.__OSD = pyosd.osd()

        try:
            self.__OSD.set_font( conf.get("OSD","font") )
        except:
            self.__OSD.set_font("-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        try:
            self.__OSD.set_colour( conf.get("OSD","colour") )
        except:
            print "colour not defined,use default"

        try:
            self.__OSD.set_timeout( conf.getint("OSD","timeout") )
        except:
            print "timeout not defined,use default"

        try:
            self.__OSD.set_pos( conf.getint("OSD","pos") )
        except:
            print "pos not defined,use default"

        try:
            self.__OSD.set_align( conf.getint("OSD","align") )
        except:
            print "align not defined,use default"
        try:
            self.__OSD.set_offset( conf.getint("OSD","offset") )
        except:
            print "offset not defined,use default"

        f.close()

    def get_number_lines(self):
        return self.__OSD.get_number_lines()

    def Reset(self):
        #print "CALL LyricsOSD Reset"
        self.__OSD.hide()

    def Show(self,str,line=0):
        #print "CALL LyricsOSD Show"
        self.__OSD.display(str,line=line)

