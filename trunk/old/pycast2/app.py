#!/usr/bin/env python
# Some program stuff, program 
# config file loading and writing
# adding and removing casts
# config dir management
from datetime import datetime
import os
import os.path

CastConfig="/home/iphitus/.pycast/casts"
def delistify(tehlist):
  x=0
  while x<len(tehlist):
    tehlist[x]=tehlist[x][0]
    x=x+1
  return tehlist


def checkdb(location):
  if os.access(location,os.F_OK) is True:
    return True
  else:
    return False
