#! /usr/bin/python
# prefs.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-26

class Prefs:
  def __init__(self,pyCast):
    '''Opens the Add Cast Dialog'''
    self.mainWindow=pyCast.pyCast
    self.podCast=pyCast.podCast
    self.prefsWindow=gtk.glade.XML (GLADEFILE,"preferences")
    self.wprefsWindow=self.AddCast.get_widget("preferences")
    dic = { "on_addcastok" : (self.Ok),  
            "on_addcastcancel" : (self.Cancel)}
    self.AddCast.signal_autoconnect (dic) 

    pass

  def Ok():
    
    self
    pass

  def Cancel():
    pass
    
  def Browse():
    pass

class Browse:
  def __init__(self,pyCast):
    pass
    
  def Ok():
    pass

  def Cancel():
    pass
    
