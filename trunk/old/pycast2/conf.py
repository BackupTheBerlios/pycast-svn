import os
import app
import thread
import gtk
from kirbybase import KirbyBase, KBError

if os.name is 'posix': 
  CONFIG=os.getenv('HOME')+'/.pycast/'
elif os.name is 'nt': 
  print 'windows aint supported *quite* yet'
else: 
  print 'what are you using? email me, iphitus@gmail.com'

CASTDB=CONFIG+'cast.tbl'
RSSDB=CONFIG+'rss.tbl'
CONFDB=CONFIG+'conf.tbl'
GLADEFILE='glade/pycast.glade'

def Load():
  Conf = KirbyBase()
  if not app.checkdb(CONFDB):
    Conf.create(CONFDB, ['name:str', 'value:str'])
    if os.name == 'posix':
      LIBRARY=os.getenv('HOME')+'/podcasts/'
    elif os.name == 'nt':
      LIBRARY='My Documents/My Podcasts/'
    Conf.insert(CONFDB, ['LIBRARY',LIBRARY])
    Conf.insert(CONFDB, ['KEEPDAYS','7'])
    Conf.insert(CONFDB, ['KEEPNUM','5'])
    Conf.insert(CONFDB, ['DATE','%D%m%Y'])
    Conf.insert(CONFDB, ['LIBFORMAT','date/name'])


def Get(entry):
  return Conf.select(CONFDB,['name','value'],[entry,''],['name','value'])
  
