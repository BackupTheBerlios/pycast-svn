#! /usr/bin/python
# pycast/pycast2.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id: pycast2.py,v 1.2 2005/01/07 11:09:58 iphitus Exp $
# $Source: /home/iphitus/pycast/pycast2.py,v $
# 2005-01-07

import sys
try:
  import pygtk
  pygtk.require("2.0")
except:
  sys.exit(1)
  
import gtk
import gtk.glade
import gobject
import gtkhtml2

import os
import conf
import podcast
import thread

import dialogs
import display
  
class app:
  def __init__(self):
    self.pyCast=gtk.glade.XML (conf.GLADEFILE,"pycast")
    
    if os.name == 'posix':
      self.podCast=podcast.podcasts(os.path.expanduser('~/.pycast/'))
    elif os.name == 'nt':
      print "windows not quite supported yet, but maybe it'll work :)"
      self.podCast=podcast.podcasts(os.path.expanduser('~/pyCast Config'))
      # ok.... win32 aint ready yet.
    dic = { "on_pycast_destroy" : (self.Exit),
            "on_addcast" : (dialogs.AddCast,self),
            "on_editcast" : (dialogs.EditCast,self),
            "on_removecast" : (dialogs.RemoveCast,self),
            "on_castlist_click" : (display.CastlistClick,self)} 
            
    view = gtkhtml2.View()
    #view.set_document(document)
    #view.connect('request_object', request_object)

    RssHtml = self.pyCast.get_widget("RssScrolledWindow")
    RssHtml.add(view)
    
    self.pyCast.signal_autoconnect (dic)
    

    display.ListCasts(self.pyCast,self.podCast)
    display.InitItemList(self.pyCast)
    display.DisplayItems(self.pyCast,self.podCast)
    gtk.threads_init()  
    
    thread.start_new_thread(self.podCast.UpdateRSS,())
    for cast in self.podCast.AllCasts:
     self.podCast.AppendRSS(cast)

    gtk.threads_enter()
    gtk.main()
    gtk.threads_leave()
  
  def Exit(widget,other):
    thread.exit()
    gtk.main_quit()

         
if __name__ == "__main__":
  pyCast = app()





