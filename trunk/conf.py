import os
import podcast
import thread
import gtk
import sqlite

GLADEFILE='glade/pycast.glade'
glade='glade/pycast.glade'

class config:
  def __init__ (confdir,librarydir):
    
     = sqlite.connect("confdir+'conf.db'")
    
    if not podcast.checkdb(self.config):
      Conf.create(self.config, ['name:str', 'value:str'])
      if os.name == 'posix':
        librarydir=os.getenv('HOME')+'/podcasts/'
      elif os.name == 'nt':
        librarydir='My Documents/My Podcasts/'
      Conf.insert(config, ['library',librarydir])
      Conf.insert(config, ['keepdays','7'])
      Conf.insert(config, ['keepnum','5'])
      Conf.insert(config, ['date','%D%m%Y'])
      Conf.insert(config, ['format','date/name'])    
     
  def set(self,name,value):
    '''Function to change/set a value - please test.'''
    if not self.Conf.update(self.config,['name'],[name],[value],['value']):
      if not self.Conf.add(self.insert,[name,value]):
        # this wont, EVER happen, but I allow it to all the same :)
        return 1
    return 0
 
  def get(self,name):
    '''function to get config'''
    self.Conf.select(self.config,['name','value'],['format',''],['name','value'])
    
