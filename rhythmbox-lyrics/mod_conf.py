#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2009-05-18 14:06:10

import os
import imp, ConfigParser

class LyricsConf :
    def __init__(self):
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
        inifile = imp.find_module('mod_conf')[1]
        inifile = os.path.dirname(inifile) + "/configure"
        try:
            f = open(inifile,'r')
        except:
            f = open(inifile,'w+')
            f.write(CONF)
            f.seek(0)

        self.conf = ConfigParser.ConfigParser()
        self.conf.readfp( f )
        f.close()

    def getint(self,sect,param,default=None):
        try:
            return self.conf.getint(sect,param)
        except:
            return default

    def get(self,sect,param,default=None):
        try:
            return self.conf.get(sect,param)
        except:
            return default

