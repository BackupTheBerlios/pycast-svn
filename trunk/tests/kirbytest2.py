#!/usr/bin/env python

from conf import glade,gladefile,config,castdb
from kirbybase import KirbyBase, KBError
import datetime
import app


Casts = KirbyBase()
#Casts.create(castdb, ['name:str','url:str','update:bool','utime:datetime.datetime'])
#x=0
#while x<len(OCast.names):
 # 
  #if OCast.update[x] == '0':
 #   udatev=False
 # else:
 #   udatev=True
 # Casts.insert(castdb, [OCast.names[x],OCast.urls[x],udatev,datetime.datetime.now()])
 # x=x+1
joe= Casts.select(castdb, ['name'],[''],['name'])
x=0
while x<len(joe):
  joe[x]=joe[x][0]
  x=x+1
print joe
