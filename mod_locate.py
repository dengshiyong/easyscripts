#!/usr/bin/env python
# -*- coding: utf8 -*-
# 2009-04-03

import os, re, time

from mod_osd import LyricsOSD


class LyricsLocate :
    def __init__(self):
        print "CALL LyricsLocate __init__"
        self.__RE_TIME=r"^\[[0-9][0-9][:.][0-5][0-9][:.][0-9][0-9]\]"
        self.__RE_OFFSET=r"^\[OFFSET *[+-][0-9]*\]"
        self.__lines = None
        self.__pos = 0
        self.__btime = time.time() # begin time
        self.__OFFSET = 0
        self.__OSD = LyricsOSD()

    def Reset(self):
        print "CALL LyricsLocate Reset"
        self.__lines = None
        self.__pos = 0
        self.__btime = time.time()
        self.__OFFSET = 0
        self.__OSD.Reset()

    def __countTime(self,stime):
        try:
            sec = "%d.%d" % (int(stime[0:2])*60+int(stime[3:5]),int(stime[6:8]))
        except:
            sec = "0.0"
        return eval(sec)

    def __filterSong(self,song):
        #print "CALL LyricsLocate __filterSong"
        if song == None : return "~~ ~~ ~~"
        song = song.replace("\n","").replace("\r","")
        if len(song) == 0 : song = "~~ ~~ ~~"
        return song

    def __GetLyrics(self,filename):
        #print "CALL LyricsLocate __GetLyrics"
        self.__lines = None
        if filename == None : return
        if not os.path.exists(filename) : return

        lines=None
        try:
            f = open(filename,'r')
            lines = f.readlines()
            f.close()
        except IOError,message:
            print message

        if lines == None : return

        self.__lines = []
        for line in lines:
            if line == "" : continue
            if line[0] != '[': continue
            ti=[]
            while re.search(self.__RE_TIME,line):
                ti.append(line[0:10])
                line = line[10:]
            if len(ti) == 0 :
                self.__lines.append("[00:00.00]"+line)
            else:
                for t in ti:
                    self.__lines.append(t+line)

        if len(self.__lines) == 0 :
            self.__lines == None
            return

        self.__lines.sort()

    def __getHead(self,lines):
        print "CALL LyricsLocate __getHead"
        song=''
        stime=''
        for line in lines :
            if line[1:9] == "00:00.00" :
                song = song + " " + line[10:]
                self.__pos=self.__pos+1
            else:
                stime = line[1:9]
                break
        song = song.replace('[','').replace(']','')
        song = song.replace('ti:','').replace('ar:','')
        song = song.replace('al:','').replace('by:','')
        return [stime,song]

    def __getSong(self,lines,idx):
        line = lines[idx]
        stime= line[1:9]
        song = line[10:]
        return [stime,song]

    def LyricsShow(self,filename=None,elapsed=0):
        #print "CALL LyricsLocate LyricsShow"
        offset = elapsed - self.__OFFSET
        if offset < 0 : offset = 0

        if self.__lines == None :
            self.__GetLyrics(filename)
            if self.__lines == None : return
        if len(self.__lines) == 0 : return

        if elapsed > 0 and abs(self.__btime + offset - time.time()) > 0.2 :
            self.__btime = time.time() - offset

            self.__OFFSET=0
            self.__pos = 1
            n=-1
            while n < 0 and self.__pos < len(self.__lines) :
                stime,song = self.__getSong(self.__lines,self.__pos)
                if re.search(self.__RE_OFFSET,song):
                    self.__OFFSET = eval(song.replace(']','')[8:])
                ntime = self.__countTime(stime)
                n = self.__btime + ntime - time.time()
                self.__pos = self.__pos + 1
            self.__pos = self.__pos - 2
            if self.__pos < 0 : self.__pos = 0
            print "%2d/%d SEED" % ( self.__pos, len(self.__lines) )

        if self.__pos >= len(self.__lines) : return

        if self.__pos == 0 :
            stime,song = self.__getHead(self.__lines)
        else:
            stime,song = self.__getSong(self.__lines,self.__pos)

        ntime=self.__countTime(stime)
        n = self.__btime + ntime - time.time()
        if n > 0 : return

        song = self.__filterSong(song)

        if re.search(self.__RE_OFFSET,song):
            self.__OFFSET = eval(song.replace(']','')[8:])

        self.__OSD.Show(song,line=0)

        i = self.__OSD.get_number_lines()
        while i > 1 :
            i = i - 1
            song = self.__getSong(self.__lines,self.__pos + i)[1]
            song = self.__filterSong(song)
            self.__OSD.Show(song,line=i)

        self.__pos = self.__pos + 1

        print "%2d/%d %s %6.2f/%2.2f %6.2f %.2f %s" % ( self.__pos, len(self.__lines), stime, elapsed, offset, ntime, time.time(), song )

