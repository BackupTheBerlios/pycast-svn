#! /usr/bin/python
# casts.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-08
  
import os
import time 
import datetime
import socket # so we can catch timeouts
import feedparser
import urllib
import tempfile 
from kirbybase import KirbyBase, KBError

class podcasts:
  def __init__(self,db_dir):
    
    self.Rss = KirbyBase()
    self.Casts = KirbyBase()

    # simple config stuff
    self.db_dir = db_dir
    self.cdb = db_dir+'casts.db'
    self.rdb =db_dir+'rss.db'

    # error checkin n stuff
    self.rsserror = []
    self.casterror = []
    socket.setdefaulttimeout(30)

    # RSS updating vars.
    self.RSSUpdateList = []
    self.RSSUpdateLock = False

    
    # checking for connection to internet
    # such an easy way out :)
    if checkurl('www.google.com'): 
      self.connection = True
    else:
      self.connection = False
    
    # Names of all casts.
    if not checkdb(self.cdb):
      self.Casts.create(self.cdb, ['name:str',  
                         'url:str',
                         'update:bool'])

    if not checkdb(self.rdb):
      self.Rss.create(self.rdb, ['name:str',
                         'date:datetime.datetime',
                         'title:str',
                         'description:str',
                         'link:str',
                         'enclosure:str',
                         'enclosuretype:str',
                         'downloaded:bool',
                         'filename:str',
                         'opml:str'])
    
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
   
  def AppendRSS(self,name):
    
  
  def UpdateRSS(self,name=None):
    ''' Download/Rss of name 'name' '''
    print "hello world"
    # Function declared, new, clean, fixed and complete.. I wish :) 
    # By god joe, i think this function is Threadsafe!
    
    if self.RSSUpdateLock:
      if name is None:
        # ok, we gotta make sure we dont double requests.
        objects = self.Casts.select(self.cdb,['name','url'],['',''],['name','url'])
        for object in objects:
          if object not in self.RSSUpdateList:
            print "hi jo"
            self.RSSUpdateList = self.RSSUpdateList.append(object)
      else:
        if name not in self.RSSUpdateList:
          appendage=self.Casts.select(self.cdb,['name'],[name],['name','url'])
          self.RSSUpdateList = self.RSSUpdateList.append(appendage)
    else:
      print 1
      # and on we go!
      if name is None:
        self.RSSUpdateList=self.RSSUpdateList+self.Casts.select(self.cdb,['name','url'],['',''],['name','url'])
        self.RSSUpdateLock = True
      else:
        # they specified a name...
        appendage=self.Casts.select(self.cdb,['name'],[name],['name','url'])
        self.RSSUpdateList = self.RSSUpdateList.append(appendage)
    print 2
    for cast in self.RSSUpdateList:
      print cast
      print name
      print 3
      self.RSSUpdateList.pop()
      if cast[0] == name and name != None or name == None:
        print 4
        (handle, tmp) = tempfile.mkstemp()
        urlgood = checkurl(cast[1])
        print urlgood
        print "ok",cast
        if urlgood:
          print 5
          print cast
          try:
            urllib.urlretrieve(cast[1],tmp)
          except socket.timeout, ex:
            self.rsserror.append({ 'name' : cast[0], 'url': cast[1]}) 
          except socket.gaierror, ex:
            self.rsserror.append({ 'name' : cast[0], 'url': cast[1]})
          
          rssfile=feedparser.parse(tmp)
          for entry in rssfile.entries:
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
            print NewEntry
            ExistingEntries = self.Rss.select(self.rdb,['name','title','description','link','enclosure',],  
                                                       ['','','','',''],['name','title','description','link','enclosure',])
            if NewEntryCut not in ExistingEntries:
              self.Rss.insert(self.rdb,NewEntry)
              print "Added: "+NewEntry[2] 
        else:
          print "well the url "+cast[0]+" went bad, offer to remove later..."     
    self.RSSUpdateLock=False
    
  def DownloadCast(self,Item):
    ''' Download all the items of the cast 'name' '''
    # Question 1 ) how is the data going to be passed?? by a covering function
    # Question 2 ) use a stack for this function! yep!!!
    # load up some config
    config = conf.config()
    format = config.get('libformat')
    Library = config.get('library')
    date = time.strftime(config.get('date'))
    download = False
            
    if checkurl(Item[2]):
      # check the url is good
      if os.access(library,os.W_OK):
        # does db directory exist?

        # now check which format >.< this is soo ugly
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
            self.Rss.update(self.rdb, ['recno'], [Item[0]], [filename], ['filename'])
          elif Item[3] == "bittorrent":
            self.DownloadBTCast(Item[2],downloaddir)
            print "This elif will never be thrown"
          else:
            print "somethin bad happened, email me the podcast url to iphitus@gmail.com"
            print "thankyou for your help and support, you may now resume using pycast."
      else:
        print "cant access db dir"       

  def DownloadBTCast(self,url,dldir):
    ''' Download a bittorrent cast '''
    # get this supported asap dude!
    print "Bittorrent not supported just *yet*. coming soon. "

  def AddCast(self,name,url,update):
    '''Add Cast to db'''

    if name in self.AllCasts:
      return 1 
    if not checkurl(url):
      # check url.
      return 2
    else:
      # all good, insert the cast.
      self.Casts.insert(self.cdb, [name,url,update])
      # todo - add a threadsafe update here.
      self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
      self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
      return 0


  def EditCast(self,oldname,newname,url,update):
    '''Edit a cast'''
    recno = self.Casts.select(self.cdb,['name'],[oldname],['recno'])[0]
    if newname not in self.AllCasts or newname == oldname:
      self.Casts.update(self.cdb,['recno'],[recno[0]],{ 'name' : newname, 
                                                     'url' : url, 
                                                     'update' : update })
    else:
      return 1
    recnos = self.Rss.select(self.rdb,['name'],[oldname],['recno'])
    for recno in recnos:
      self.Rss.update(self.rdb,['recno'],[recno],{ 'name' : newname })
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])

  def RssCull(self,name):
    '''Remove old stuff, thats past user desired date'''
    date = datetime.date.today()-datetime.timedelta(conf.get('keepdays'))
    old = self.Rss.select(self.rdb,['name','date'],[name,'<%s' % date],['recno','filename'])
    for item in old:
      self.RemoveItem(item)

        
  def CastField(self,name,field):
    ''' Get specific fields from the cast '''
    return self.Rss.select(self.rdb,['name'],[name],[field])
  
  def CastItems(self,name):
    ''' Get description fields from the cast '''
    return self.Rss.select(self.rdb,['name'],[name],['title'])
 
  def RemoveItem(self,entry):
    ''' does dirty job of removing item '''
    if entry[1] != '':
      if os.access(entry[1],os.W_OK):
        os.remove(entry[1])
    self.Rss.delete(self.rdb, ['recno'],[entry[0]])
                                      
  def RemoveCast(self,name):
    '''Removes a whole cast of 'name' '''
    self.Casts.delete(self.cdb,['name'],['^'+name+'$'])
    for entry in self.Rss.select(self.rdb,['name'],[name],['recno','filename']):
      self.RemoveItem(entry)
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
    
    
def checkdb(location):
  if os.access(location,os.F_OK) is True:
    return True
  else:
    return False

def delistify(tehlist):
  x=0
  while x<len(tehlist):
    tehlist[x]=tehlist[x][0]
    x=x+1
  return tehlist

def checkurl(url):
  try:
      dl=urllib.urlopen(url)
      urlgood=True
      dl.close()
  except IOError:
      urlgood=False
  return urlgood


