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
import sqlite
from urllib import urlopen, urlretrieve
from tempfile import mkstemp # temp file
from threading import Lock
import Queue


class podcasts:
 
  ''' class of podcast manipulative stuff '''
  
  def __init__(self,db_dir):
  
    ''' constructor for podcasts.. '''
    
    # open objects for our dbs and locks for them
    
    self.dbFile = os.getenv('HOME') + "/.pycast/pycast.db"
    self.dbObject = sqlite.connect(self.database,encoding='utf-8',autocommit=1)
    self.dbCursor = self.dbObject.cursor()
    self.dbLock = Lock()
    
    # error checkin n stuff
    # CHECK IF NEEDED ......
    self.RSSError = []
    self.CastError = []
    socket.setdefaulttimeout(30)

    # RSS updating vars.
    self.RSSUpdates = Queue.Queue()
    self.RSSUpdateLock = False
    
    # really should be in pycast2.py...
    self.Descriptions = [] 
    self.Itemlist = [] 
    
    # checking for connection to internet
    # such an easy way out ... you need a better way iph!
    if checkurl('www.google.com'): 
      self.Connection = True
    else:
      self.Connection = False
    

    # checks for existance of databases and creates if not existing
    if not checkdb(self.dbFile,'casts'):
      self.dbCursor.execute("create table casts (name UNICODE,
                                                 url INT, 
                                                 update INT)")
      
    if not checkdb(self.dbFile,'rss'):
      self.dbCursor.execute("create table rss (name UNICODE,
                                               date UNICODE, 
                                               title UNICODE,
                                               description UNICODE,
                                               link UNICODE,
                                               enclosure UNICODE,
                                               enclosuretype UNICODE,
                                               downloaded INT,
                                               filename UNICODE,
                                               opml UNICODE)")
                                                
    # create some vars with some usefull info on the casts.. 
    self.dbCursor.execute("select * from casts")
    self.AllCasts = self.dbCursor.fetchall()
    
    self.dbCursor.execute("select * from rss")
    self.AllCastDetails = self.dbCursor.fetchall()


  def AppendRSS(self,name):
    
    ''' Add an RSS item to the queue to be updated '''
    self.dbCursor.execute("select * from casts where name=%s" (name))
    self.RSSUpdates.put(self.dbCursor.fetchall())

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
            self.RSSError.append({ 'name' : cast[0], 'url': cast[1]}) 
          except socket.gaierror, ex:
            self.RSSError.append({ 'name' : cast[0], 'url': cast[1]})
          
          # load it into feedparser :D
          rssfile=feedparser.parse(tmp)

          # lotsa try's here >.< just in case objects arent in cast.
          for entry in rssfile.entries:
            try:
    
              NewEntry=[]
              NewEntry.append(cast[0])
              NewEntry.append(strftime("%d-%m-%y"))
              NewEntry.append(str(entry.title))
            except AttributeError:
              NewEntry.append("")   
            try:
              NewEntry.append(str(entry.summary))
            except AttributeError:
              NewEntry.append("")     
            try:
              NewEntry.append(str(entry.link))
            except AttributeError:
              NewEntry.append("")
            try:
              NewEntry.append(entry.enclosures[0].url)
              NewEntry.append(entry.enclosures[0].type)
            except AttributeError:
              NewEntry = NewEntry+["",""]
            
            NewEntry=NewEntry+[0."",""]
            NewEntryCut = [NewEntry[0]]+NewEntry[2:6]  
            self.dbCursor.execute('select name,title,description,link,enclosure from rss')
            
            # check its not already existing
            if NewEntryCut not in self.dbCursor.fetchall():
              ne=NewEntry
              # get lock and add :D
              self.RssLock.acquire(True)
              self.dbCursor.execute('insert into rss values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (ne[0],ne[1],ne[2],ne[3],ne[4],ne[5],ne[5],ne[6],ne[7],ne[8],ne[9]))
    if not checkdb(self.dbFile,'rss'):
      self.dbCursor.execute("create table rss (name UNICODE, date UNICODE, 
                             title UNICODE, description UNICODE,
                             link UNICODE, enclosure UNICODE,
                             enclosuretype UNICODE, downloaded INT,
                             filename UNICODE, opml UNICODE)")

              self.RssLock.release()
              # yay!!!!
              print "Added: "+NewEntry[2] 
        else:
          # bad url!!!
          print "well the url "+cast[0]+" went bad, offer to remove later..."    
        
  def UpdateSelf(self):
    ''' Updates self variables.... w00t '''
    self.dbCursor.execute("select * from casts")
    self.AllCasts = self.dbCursor.fetchall()
    
    self.dbCursor.execute("select * from rss")
    self.AllCastDetails = self.dbCursor.fetchall()
    
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
            print "This elif will never be thrown - scratch that, it will"
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
      self.UpdateSelf()
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
    self.UpdateSelf()

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
    
    bob = self.Rss.select(self.rdb,['name'],[name],['recno','title','downloaded'])
    return bob

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
    self.UpdateSelf()  
    
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


