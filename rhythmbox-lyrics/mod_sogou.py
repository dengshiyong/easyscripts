#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, re
import urllib2
from threading import Thread


class wget:
    def __init__(self):
        #print "CALL wget __init__"
        self.__OPENER = None

    def __initOpener(self):
        #print "CALL wget __initOpener"
        proxy = os.getenv("http_proxy")

        if proxy :
            http_proxy = urllib2.ProxyHandler({"http":proxy})
            opener = urllib2.build_opener(http_proxy)
        else:
            opener = urllib2.build_opener()

        self.__OPENER = opener

    def geturlasfile(self,url):
        #print "CALL wget geturlasfile"
        if self.__OPENER is None :
            self.__initOpener()

        urlfile = self.__OPENER.open(url)
        return urlfile

    def geturlaslines(self,url):
        #print "CALL wget geturlaslines"
        if self.__OPENER is None :
            self.__initOpener()

        try:
            urlfile = self.__OPENER.open(url)
            return urlfile.readlines()
        except:
            print "ERROR: network error"
            return []

class LyricsSearch(Thread) :
    def __init__(self,title,artic="UNKNOWN",check=True):
        print "CALL LyricsSearch __init__"
        self.__title = title
        self.__artic = artic
        self.__check = check
        lypath = "%s/.lyrics/" % os.environ.get('HOME')
        if not os.path.exists(lypath):
            os.mkdir(lypath)

        Thread.__init__(self)

    def searchLyric(self):
        print "CALL LyricsSearch searchLyric"
        """ get lyric from mp3.sogou.com """

        title = self.__title
        artic = self.__artic
        check = self.__check

        w = wget()
        URL = "http://mp3.sogou.com/gecisearch.so?query=%s-%s" % ( artic,title )
        print "SONG [%s][%s]" %(artic,title)
        #URL = unicode(URL,"UTF8").encode("GB18030")
        URL = URL.encode("GB18030")
        urllib2.quote(URL)
        htmls = w.geturlaslines(URL)
        #open("k1","w+").write("".join(htmls))
        for html in htmls :
            if html.find("downlrc.jsp") < 0 : continue
            link = html[html.find("downlrc.jsp"):html.find("LRC")-2]
            link = "http://mp3.sogou.com/" + link
            lyrows = w.geturlaslines(link)
            #open("k2","w+").write("".join(lyrows))
            if check == False :
                return lyrows
            art=tit=None
            for n in lyrows :
                n = unicode(n,"GB18030").encode("UTF8")
                if re.search("^\[ar:",n):
                    art = n[n.find("[ar:"):]
                    art = art[4:art.find("]")]
                if re.search("^\[ti:",n):
                    tit = n[n.find("[ti:"):]
                    tit = tit[4:tit.find("]")]
                if art != None and tit != None : break
            print "FIND [%s][%s]" % (art,tit)
            if ( artic is None or artic == "" ) and art is not None :
                artic = art
            self.__artic = artic
            self.__title = title
            if title and tit and title == unicode(tit,"UTF8") :
                return lyrows
            #if title and tit and str(title).upper() == tit.upper() :
                #return lyrows
            return []
        return []

    def saveLyric(self,lines,conv=True):
        print "CALL LyricsSearch saveLyric"
        if lines == [] : return
        s = "".join(lines)
        if conv :
            s = unicode(s,"GB18030").encode("UTF8")
        lypath = "%s/.lyrics/%s" % ( os.environ.get('HOME'), self.__artic )
        if not os.path.exists(lypath):
            os.mkdir(lypath)
        lyfullname = "%s/%s.lrc" % (lypath,self.__title)
        f = open(lyfullname,"w+")
        f.write(s)
        f.close()

    def run(self):
        lines = self.searchLyric()
        if lines != [] :
            self.saveLyric(lines)
