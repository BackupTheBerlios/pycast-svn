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
import socket  # so we can catch timeouts
import feedparser
from urllib import urlopen, urlretrieve
from tempfile import mkstemp # temp file
from threading import Lock
import Queue
from kirbybase import KirbyBase, KBError

class podcasts:
 
  ''' class of podcast manipulative stuff '''
  
  def __init__(self,db_dir):
  
    ''' constructor for podcasts.. '''
    
    # open objects for our dbs and locks for them
    self.Rss = KirbyBase()
    self.RssLock = Lock()
    self.Casts = KirbyBase()
    self.CastsLock = Lock()

    # simple config stuff
    self.db_dir = db_dir
    self.cdb = db_dir+'casts.db'
    self.rdb =db_dir+'rss.db'
    
    # error checkin n stuff
    # CHECK IF NEEDED ......
    self.rsserror = []
    self.casterror = []
    socket.setdefaulttimeout(30)

    # RSS updating vars.
    self.RSSUpdates = Queue.Queue()
    # do i need this? rewrite with lock if so
    self.RSSUpdateLock = False
    
    # really should be in pycast2.py...
    self.Descriptions = [] 
    self.Itemlist = [] 
    
    # checking for connection to internet
    # such an easy way out :)
    if checkurl('www.google.com'): 
      self.connection = True
    else:
      self.connection = False
    

    # checks for existance of databases and creates if not existing
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
                         'downloaded:int',
                         'filename:str',
                         'opml:str'])
    
    # create some vars with some usefull info on the casts.. 
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
   
  def AppendRSS(self,name):
    
    ''' Add an RSS item to the queue to be updated '''
    
    appendable = self.Casts.select(self.cdb,['name','url'],['^'+name+'$',''],['name','url'])[0]
    self.RSSUpdates.put(appendable)
    print appendable

  def UpdateRSS(self):
    
    ''' Download/Rss of name 'name' '''
    
    # Function declared, new, clean, fixed and complete.. I wish :) 
    # By god joe, i think this function is Threadsafe!
     
    # if process not already running...
    if not self.RSSUpdateLock:
      # mark as running
      self.RSSUpdateLock = True
      
      # and go forever.....
      while True:  
        # get our first item, get temp item, check item, then download
        cast = self.RSSUpdates.get(block=True,timeout=None)
        (handle, tmp) = mkstemp()
        urlgood = checkurl(cast[1])
         
        if urlgood:
          # url's good, im downloading
          try:
            urlretrieve(cast[1],tmp)
          except socket.timeout, ex:
            self.rsserror.append({ 'name' : cast[0], 'url': cast[1]}) 
          except socket.gaierror, ex:
            self.rsserror.append({ 'name' : cast[0], 'url': cast[1]})
          
          # load it into feedparser :D
          rssfile=feedparser.parse(tmp)

          # lotsa try's here >.< just in case objects arent in cast.
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

            # if we made it through there, we create the new entry
            NewEntry=NewEntry+[str(enclosureurl),str(enclosuretype),0,'na','na']
            NewEntryCut = [NewEntry[0]]+NewEntry[2:6]  
            ExistingEntries = self.Rss.select(self.rdb,['name','title','description','link','enclosure',],  
                                                         ['','','','',''],['name','title','description','link','enclosure',])
            # check its not already existing
            if NewEntryCut not in ExistingEntries:
              # get lock and add :D
              self.RssLock.acquire(True)
              self.Rss.insert(self.rdb,NewEntry)
              self.RssLock.release()
              # yay!!!!
              print "Added: "+NewEntry[2] 
        else:
          # bad url!!!
          print "well the url "+cast[0]+" went bad, offer to remove later..."    
        
   
  def DownloadCast(self,Item):
    
    ''' Download all the items of the cast 'name' '''
    
    # Question 1 ) how is the data going to be passed?? by a covering function
    # Question 2 ) use a stack for this function! yep!!!
    # load up some config
    # ['recno','name','url','urltype']
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
            (filename, headers) = urlretrieve(Item[2],downloaddir)
            self.RssLock.acquire(True)
            self.Rss.update(self.rdb, ['recno'], [Item[0]], [filename], ['filename'])
            self.RssLock.release()
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
      self.CastsLock.acquire(True)
      self.Casts.insert(self.cdb, [name,url,update])
      self.CastsLock.release()
      # todo - add a threadsafe update here.
      self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
      self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
      return 0


  def EditCast(self,oldname,newname,url,update):
    
    '''Edit a cast'''
    
    recno = self.Casts.select(self.cdb,['name'],[oldname],['recno'])[0]
    if newname not in self.AllCasts or newname == oldname:
      self.CastLock.acquire(True)
      self.Casts.update(self.cdb,['recno'],[recno[0]],{ 'name' : newname, 
                                                     'url' : url, 
                                                     'update' : update })
      self.CastLock.release()
    else:
      return 1
    recnos = self.Rss.select(self.rdb,['name'],[oldname],['recno'])
    for recno in recnos:
      self.RssLock.acquire(True)
      self.Rss.update(self.rdb,['recno'],[recno],{ 'name' : newname })
      self.RssLock.release()
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])

  def RssCull(self,name):
    
    '''Remove old stuff, thats past user desired date'''
    
    date = datetime.date.today()-datetime.timedelta(conf.get('keepdays'))
    old = self.Rss.select(self.rdb,['name','date'],[name,'<%s' % date],['recno','filename'])
    for item in old:
      self.RemoveItem(item)

        
  def CastField(self,recno=None,name=None,field=None):
    
    ''' Get specific fields from the cast '''
    
    if recno is not None:
      return self.Rss.select(self.rdb,['recno'],[recno])
    if name is not None and field is not None:
      return self.Rss.select(self.rdb,['name'],[name],fields)
    else:
      return self.Rss.select(self.rdb,['recno'],['*'])

  
  def CastItems(self,name):
    
    ''' Get description fields from the cast '''
    
    joe = self.Rss.select(self.rdb,['name'],[name],['recno','title','downloaded'])
    print joe
    return joe

  def RemoveItem(self,entry):
    
    ''' does dirty job of removing item '''
    
    if entry[1] != '':
      if os.access(entry[1],os.W_OK):
        os.remove(entry[1])
    self.RssLock.acquire(True)
    self.Rss.delete(self.rdb, ['recno'],[entry[0]])
    self.RssLock.release()
    
  def RemoveCast(self,name):
    
    '''Removes a whole cast of 'name' '''
    
    # pretty simple, get lock, remove stuff, release
    self.CastLock.acquire(True)
    self.Casts.delete(self.cdb,['name'],['^'+name+'$'])
    self.CastLock.release()
    # remove rss items now
    for entry in self.Rss.select(self.rdb,['name'],[name],['recno','filename']):
      self.RemoveItem(entry)
    # reload some vars
    self.AllCasts = delistify(self.Casts.select(self.cdb, ['name'],[''],['name']))
    self.AllCastDetails = self.Casts.select(self.cdb, ['recno'],['*'])
    
    
def checkdb(location,table):
  
  ''' checks if file of db exists - needs further checking '''
  
  if os.access(location,os.F_OK) is True:
    try:
      configsql = sqlite.connect(location)
      sqlcursor = configsql.cursor()
      sqlcursor.execute("select * from "+table+) 
    except:
      return False
  else:
    return False

def delistify(tehlist):
  
  ''' lazy function to convert [[1],[2],[3]] to [1,2,3] '''
  
  x=0
  while x<len(tehlist):
    tehlist[x]=tehlist[x][0]
    x=x+1
  return tehlist

def checkurl(url):
  
  ''' Checks to see if url is still all good '''
  
  # CHECK THIS -- maybe socket borke method?
  try:
      dl=urlopen(url)
      urlgood=True
      dl.close()
  except IOError:
      urlgood=False
  return urlgood


