#! /usr/bin/python
# pycast/dialogs.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-17
 
import gtk
import gtk.glade
import gobject
import datetime
import thread
from conf import GLADEFILE

import display

class AddCast:
  def __init__(self,widget,pyCast):
    '''Opens the Add Cast Dialog'''
    self.pyCast=pyCast.pyCast
    self.podCast=pyCast.podCast
    self.AddCast=gtk.glade.XML (GLADEFILE,"addcast")
    self.wAddCast=self.AddCast.get_widget("addcast")
    dic = { "on_addcastok" : (self.Ok),  
            "on_addcastcancel" : (self.Cancel)}
    self.AddCast.signal_autoconnect (dic) 
         
  def Ok(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
 
    CloseWindow=True
        
    AddCastName = self.AddCast.get_widget("tAddCastName")
    AddCastUrl = self.AddCast.get_widget("tAddCastUrl")
    AddCastUpdate= self.AddCast.get_widget("cAddCastUpdate") 
    
    result = self.podCast.AddCast(AddCastName.get_text(),
                       AddCastUrl.get_text(),
                       AddCastUpdate.get_mode())
    if result == 1:
      AddCastName.set_text("Name Already Used") 
      CloseWindow = False

    if CloseWindow is True:
      display.UpdateCastDisplay(self.pyCast,self.podCast)
      self.podCast.AppendRSS(AddCastName.get_text())
      display.UpdateCastDisplay(self.pyCast,self.podCast)
      self.wAddCast.destroy()
      

  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    self.wAddCast.destroy()

class EditCast:
  def __init__(self,widget,pyCast):
    '''Opens the Add Cast Dialog'''
    self.pyCast=pyCast.pyCast
    self.podCast=pyCast.podCast
    self.EditCast=gtk.glade.XML (GLADEFILE,"editcast")
    self.wEditCast=self.EditCast.get_widget("editcast")
    dic = { "on_editcastok" : (self.Ok),
            "on_editcastcancel" : (self.Cancel)}
    self.EditCast.signal_autoconnect (dic) 
    self.EditCastName = self.EditCast.get_widget("tEditCastName")
    self.EditCastUrl = self.EditCast.get_widget("tEditCastUrl")
    self.EditCastUpdate= self.EditCast.get_widget("cEditCastUpdate") 

    treeCastList = self.pyCast.get_widget("podcastlist")
    treeSelection = treeCastList.get_selection()
    (model, iter) = treeSelection.get_selected()
    self.OldName = model.get_value(iter,0)

    print "hi"
    for cast in self.podCast.AllCastDetails:
      print self.OldName,cast[1]
      if cast[1] == self.OldName:
        print self.OldName,cast[0]
        print "hi2"
        self.EditCastName.set_text(cast[1])
        self.EditCastUrl.set_text(cast[2])
        self.EditCastUpdate.set_active(True)

         
  def Ok(self,widget):
    CloseWindow = True            
    
    if self.podCast.EditCast(self.OldName, self.EditCastName.get_text(),
                                      self.EditCastUrl.get_text(),
                                      self.EditCastUpdate.get_active()) == 1:
        self.EditCastName.set_text("Name Already Used") 
        CloseWindow=False
        
    if CloseWindow is True:

      display.UpdateCastDisplay(self.pyCast,self.podCast)
      self.wEditCast.destroy()

  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    self.wEditCast.destroy()

class RemoveCast:
  def __init__(self,widget,pyCast):
    '''Opens the remove Cast Dialog'''
    self.pyCast = pyCast.pyCast
    self.podCast = pyCast.podCast
    self.RemoveCast = gtk.glade.XML (GLADEFILE,"removecast")
    self.wRemoveCast = self.RemoveCast.get_widget("removecast")
    dic = { "on_removecastok" : (self.Ok),
            "on_removecastcancel" : (self.Cancel)}
    self.RemoveCast.signal_autoconnect (dic) 
    
         
  def Ok(self,widget):
    '''When the Remove Cast Dialog's OK button is hit'''
    treeCastList = self.pyCast.get_widget("podcastlist")
    treeSelection = treeCastList.get_selection()
    (model, iter) = treeSelection.get_selected()
    selected = model.get_value(iter,0)
    self.podCast.RemoveCast(selected)
    display.UpdateCastDisplay(self.pyCast,self.podCast)
    self.wRemoveCast.destroy()

  def Cancel(self,widget):
    '''When the remove cast dialog's cancel button is hit'''
    self.wRemoveCast.destroy()
    
