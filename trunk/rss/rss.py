import gtk
import gtk.glade
import feedparser
import urllib
import os
import datetime
import app
import tempfile
from conf import GLADEFILE,CONFIG,CASTDB,RSSDB
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
      urlgood = DownloadTestRSS(cast[1])
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

def DownloadTestRSS(url):
  try:
    urlgood=True
    dl=urllib.urlopen(url)
    dl.close()
  except IOError:
    urlgood=False
  return urlgood
