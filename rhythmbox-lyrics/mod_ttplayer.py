#!/usr/bin/env python
# -*- coding: utf8 -*-
from lydown import wget
from xml.dom import minidom

@staticmethod
def ttpEncode(str) :
    str = unicode(str,"UTF8")
    res = ""
    for i in range(len(str)) :
        hex = "%04x" % ord(str[i])
        hex = "%s%s" % (hex[2:],hex[0:2])
        res += hex
    return res

@staticmethod
def CodeFunc(Id, data):
    tmp1 = (Id & 0x0000FF00) >> 8
    tmp2=0
    tmp3=0

    if ( (Id & 0x00FF0000) == 0 ):
        tmp3 = 0x000000FF & ~tmp1
    else:
        tmp3 = 0x000000FF & ((Id & 0x00FF0000) >> 16)

    tmp3 = tmp3 | ((0x000000FF & Id) << 8)
    tmp3 = tmp3 << 8
    tmp3 = tmp3 | (0x000000FF & tmp1)
    tmp3 = tmp3 << 8
    if ( (Id & 0xFF000000) == 0 ) :
        tmp3 = tmp3 | (0x000000FF & (~Id))
    else :
        tmp3 = tmp3 | (0x000000FF & (Id >> 24))



    length = len(data)
    i=length-1
    while(i >= 0):
        char = ord(data[i])
        if char >= 0x80:
            char = char - 0x100
        tmp1 = (char + tmp2) & 0x00000000FFFFFFFF
        tmp2 = (tmp2 << (i%2 + 4)) & 0x00000000FFFFFFFF
        tmp2 = (tmp1 + tmp2) & 0x00000000FFFFFFFF

        i -= 1

    i=0
    tmp1=0
    while(i<=length-1):
        char = ord(data[i])
        if char >= 128:
            char = char - 256
        tmp7 = (char + tmp1) & 0x00000000FFFFFFFF
        tmp1 = (tmp1 << (i%2 + 3)) & 0x00000000FFFFFFFF
        tmp1 = (tmp1 + tmp7) & 0x00000000FFFFFFFF
        i += 1


    tmp1 = (((((tmp2 ^ tmp3) & 0x00000000FFFFFFFF) + (tmp1 | Id)) & 0x00000000FFFFFFFF) * (tmp1 | tmp3)) & 0x00000000FFFFFFFF
    tmp1 = (tmp1 * (tmp2 ^ Id)) & 0x00000000FFFFFFFF

    if tmp1 > 0x80000000:
        tmp1 = tmp1 - 0x100000000
    return tmp1

    @staticmethod
    def EncodeArtTit(str):
        rtn = ''
        str = str.encode('UTF-16')[2:]
        for i in range(len(str)):
            rtn += '%02x' % ord(str[i])

        return rtn



def getList(art,tit):
    url = "http://ttlrcct2.qianqian.com/dll/lyricsvr.dll?sh?Artist=%s&Title=%s&Flags=0" % ( ttpEncode(art),ttpEncode(tit) )
    print url
    exit(0)
    w = wget()
    xmlstr = w.geturlasfile(url).read()
    LyXML = minidom.parseString(xmlstr)
    lists = []
    for node in LyXML.getElementsByTagName('lrc') :
        id = node.getAttribute('id')
        art = node.getAttribute('artist')
        tit = node.getAttribute('title')
        print id,art,tit
        lists.append((id,art,tit))
    return lists

getList("刘欢","我和你")
