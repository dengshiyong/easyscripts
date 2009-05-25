#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2008-12-27 22:16:45

import os
import pyosd # python-osd
from mod_conf import LyricsConf

class LyricsOSD :
    def __init__(self):
        print "CALL LyricsOSD __init__"
        self.__OSD=None
        self.__initOSD()

    def __initOSD(self):
        print "CALL LyricsOSD __initOSD"

        conf = LyricsConf()

        v_lines = conf.getint("OSD","lines",1)
        v_shadow = conf.getint("OSD","shadow",1)

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

    def get_number_lines(self):
        return self.__OSD.get_number_lines()

    def Reset(self):
        #print "CALL LyricsOSD Reset"
        self.__OSD.hide()

    def Show(self,str,line=0):
        #print "CALL LyricsOSD Show"
        self.__OSD.display(str,line=line)

