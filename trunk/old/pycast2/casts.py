#! /usr/bin/python
# casts.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-08
  
import gtk
import gtk.glade
import feedparser
import urllib
import os
import datetime
import app
import tempfile
import time
from conf import GLADEFILE,CONFIG,CASTDB,RSSDB,Get
from kirbybase import KirbyBase, KBError

def DownloadRSS(pycast,name):
  Rss = KirbyBase()
  Casts = KirbyBase()

  if not app.checkdb(RSSDB):
    Rss.create(RSSDB, ['name:str',
                                       'date:datetime.datetime',
                                       'title:str',
                                       'description:str',
                                       'link:str',
                                       'enclosure:str',
                                       'enclosuretype:str',
                                       'downloaded:bool',
                                       'filename:str',
                                       'opml:str'])

  CastList=Casts.select(CASTDB,['name','url'],['',''],['name','url'])
  for cast in CastList:
    if cast[0] == name and name != '' or name == '':
      (handle, tmp) = tempfile.mkstemp()
      urlgood = TestURL(cast[1])
      print "ok",cast
      if urlgood:
        print cast
        urllib.urlretrieve(cast[1],tmp)
        rssfile=feedparser.parse(tmp)
        for entry in rssfile.entries:
          debug=False
          if cast[0]=="Evil Genius Chronicles":
            print entry
            debug=True
          try:
            enclosureurl=entry.enclosures[0].url
            enclosuretype=entry.enclosures[0].type
          except AttributeError:
            enclosureurl=''
            enclosuretype=''     
          try:
            NewEntry = []
            NewEntry.append(cast[0])
            NewEntry.append(datetime.datetime.now())
            NewEntry.append(str(entry.title))
          except AttributeError:
            NewEntry.append('')     
          try:
            NewEntry.append(str(entry.summary))
          except AttributeError:
            NewEntry.append('')     
          try:
            NewEntry.append(str(entry.link))
          except AttributeError:
            NewEntry.append('')     
          NewEntry=NewEntry+[str(enclosureurl),str(enclosuretype),False,'na','na']
          NewEntryCut = [NewEntry[0]]+NewEntry[2:6]   
          ExistingEntries = Rss.select(RSSDB,['name','title','description','link','enclosure',],  
                                                   ['','','','',''],['name','title','description','link','enclosure',])
          if NewEntryCut not in ExistingEntries:
            Rss.insert(RSSDB,NewEntry)
            print "Added: "+NewEntry[2] 
      else:
        print "well the url "+cast[0]+" went bad, offer to remove later..."     

def TestURL(url):
try:
  urlgood=True
  dl=urllib.urlopen(url)
  dl.close()
except IOError:
  urlgood=False
return urlgood

def DownloadPodcast():
  Rss = KirbyBase()
  Items = Rss.select(RSSDB,['recno','name','enclosure','enclosuretype','filename'],
                         ['','','',''],['recno','name','enclosure','enclosuretype','filename'])

  for Item in Items:
    if Item[4]: == "":
      DownloadPodcast(Item)

def DownloadPodcast(Item):

  Rss = KirbyBase()
  Library=Get("LIBRARY")  
  download=False
  
  if TestURL(Item[2]):
    date=time.strftime(Get("DATE"))
    format=Get("LIBFORMAT")
    if os.access(Library,os.W_OK):
      if format == "name":
        if not os.access(Library+Item[1],os.W_OK):
          os.mkdir(Library+Item[1])
        download=True
        downloaddir=Library+Item[1]
      elif format == "name/date":
        if not os.access(Library+Item[1],os.F_OK):
          os.mkdir(Library+Item[1])
        if os.access(Library+Item[1]+date, os.W_OK):
          download=True
          downloaddir=Library+Item[1]+date
        else: 
          os.mkdir(Library+Item[1]+date)
          download=True
          downloaddir=Library+Item[1]+date
      elif format == "date/name":
        if not os.access(Library+date):
          os.mkdir(Library+date)
        if os.access(Library+date+Item[1]):
          download=True
          downloaddir=Library+date+Item[1]
        else:
          os.mkdir(Library+date+Item[1])
          download=True
          downloaddir=Library+date+Item[1]
      elif format == "date":
        if not os.access(Library+date):
          os.mkdir(Library+date)
        download=True
        downloaddir=Library+date
      if download is True:
        if Item[3] == "audio/mpeg":
          (filename, headers) = urllib.urlretrieve(Item[2],downloaddir)
          Rss.update(RSSDB, ['recno'], [Item[0]], [filename], ['filename'])
    else:
      print "cant access db dir"
    
    
