#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys, re

import urllib2


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

        urlfile = self.__OPENER.open(url)
        return urlfile.readlines()

class LyricsSearch :
    def __init__(self):
        print "CALL LyricsSearch __init__"
        self.__artic = "UNKOWN"
        self.__title = "NULL"

        lypath = "%s/.lyrics/" % os.environ.get('HOME')
        if not os.path.exists(lypath):
            os.mkdir(lypath)

    def searchLyric(self,title,artic="UNKNOWN",check=True):
        print "CALL LyricsSearch searchLyric"
        """ get lyric from mp3.sogou.com """
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
        lyfullname = "%s/%s.lyric" % (lypath,self.__title)
        f = open(lyfullname,"w+")
        f.write(s)
        f.close()

if __name__ == "__main__":
    argc = len(sys.argv)
    mm = LyricsSearch()
    if argc == 1 :
        lines = mm.searchLyric("我的中国心")
        mm.saveLyric(lines)
    elif argc == 2 :
        lines = mm.searchLyric(sys.argv[1])
        mm.saveLyric(lines)
    elif argc == 3 :
        lines = mm.searchLyric(sys.argv[1],sys.argv[2])
        mm.saveLyric(lines)

