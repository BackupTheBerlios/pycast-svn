#!/usr/bin/env python
# Some program stuff, program 
# config file loading and writing
# adding and removing casts
# config dir management
from datetime import datetime
import os
import os.path

CastConfig="/home/iphitus/.pycast/casts"

class CastList:
  names=[]
  urls=[]
  update=[]
  utime=[] 
  
  def __init__(self,location):
    self.location = location
  
  def add_cast(self,name,url,update):
    '''Add a cast to the list'''
    for n in self.names:
      if n == name:
        return 1
    for u in self.urls:
      if u == url:
        return 1
    if update == "1" or update == "0":
        self.update.append(update)
    else:
        return 1
    self.names.append(name)
    self.urls.append(url)
    return 0
    
  
  def load(self):
    '''Load a cast from drive''' 
    directory = os.path.split(self.location)
    if os.access(self.location, os.R_OK) is True:
      temp=open(self.location,"r")
      for line in temp.readlines():
        print line
        index,indexs,item=0,0,0
        for y in line:
          if y == ",":  
            if item==0:
              print line[indexs:index]
              self.names.append(line[indexs:index])
            elif item==1:
              print line[indexs+1:index]
              self.urls.append(line[indexs+1:index])
            elif item==2:
              print line[indexs+1:index]
              self.update.append(line[indexs+1:index])
            indexs,item=index,item+1
          index=index+1   
        temp.close()
    elif os.access(self.location, os.F_OK) is True:
      return 1
    elif os.access(directory[0],os.W_OK) is True:
      os.mknod(self.location)

  def write(self):
    '''Write cast to drive'''
    directory=os.path.split(self.location)
    if os.access(self.location, os.W_OK) is True:
      temp=open(self.location,"r+")
      x=0
      while x<len(self.names):
          temp.write(self.names[x]+","+self.urls[x]+","+self.update[x]+","+"\n")
          x=x+1
      temp.close()  
    elif os.access(self.location, os.F_OK) is True:
      return 1
    elif os.access(directory[0],os.W_OK) is True:
      os.mknod(self.location)
