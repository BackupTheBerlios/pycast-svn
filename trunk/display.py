#! /usr/bin/python
# display.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-13
 
import gtk
import gtk.glade
import gobject
import podcast

def ListCasts(pyCast,podCast):
  '''Lists all the casts into their container'''
  treeCastList=pyCast.get_widget("podcastlist")
  modlCastList=gtk.TreeStore(gobject.TYPE_STRING)
  
  treeCastList.set_model(modlCastList)  
  treeCastList.set_headers_visible(gtk.TRUE)    

  # Set the columns
  column=gtk.TreeViewColumn("Podcast",gtk.CellRendererText(), text=0)
  column.set_resizable(gtk.TRUE)
  treeCastList.append_column(column)
 
     
  # Loop through and add the casts
  newlist=[]
  for name in podCast.AllCasts:
    namelist = [name] 
    newlist=namelist+newlist
    
  for name in newlist:  
    position=modlCastList.insert_after(None,None)
    modlCastList.set_value(position, 0, name)

  selection=treeCastList.get_selection()
  selection.select_path(0)
      
def UpdateCastDisplay(pyCast,podCast):
  '''Update the cast treelist'''
  ## EXTRA CODE??
  
  treeCastList=pyCast.get_widget("podcastlist")
  modlCastList=gtk.TreeStore(gobject.TYPE_STRING)
  treeCastList.set_model(modlCastList)    

  for name in podCast.AllCasts:
    position=modlCastList.insert_after(None,None)
    modlCastList.set_value(position,0,name) 
def InitItemList(pyCast):
  treeCastItems=pyCast.get_widget("podcastitems")
  modlCastItems=gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
  
  treeCastItems.set_model(modlCastItems)  
  treeCastItems.set_headers_visible(gtk.TRUE)    
  column=gtk.TreeViewColumn("Item",gtk.CellRendererText(), text=0)
  column.set_resizable(gtk.TRUE)
  treeCastItems.append_column(column)

  column=gtk.TreeViewColumn("Downloaded",gtk.CellRendererText(), text=1)
  column.set_resizable(gtk.FALSE)
  treeCastItems.append_column(column)

def DisplayItems(pyCast,podCast):
  '''Lists all the casts into their container'''
  treeCastItems=pyCast.get_widget("podcastitems")
  modlCastItems=gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
  
  treeCastItems.set_model(modlCastItems)  
  treeCastItems.set_headers_visible(gtk.TRUE)    

  # Set the columns

  treeCastList=pyCast.get_widget("podcastlist")
  treeSelection = treeCastList.get_selection()
  (model, iter) = treeSelection.get_selected()
  if podCast.AllCasts !=[]:
    selected = model.get_value(iter,0)
    location = model.get_string_from_iter(iter)
    print "hi", location
    print podCast.AllCasts[int(location)]
  # Loop through and add the casts
    podCast.ListItems = []
    newlist=[]
    for name in podCast.CastItems(selected):
      namelist = [name] 
      newlist=namelist+newlist
    for name in newlist:
      podCast.ListItems=[[name[0],name[1]]]+podCast.ListItems
      print podCast.ListItems
      position=modlCastItems.insert_after(None,None)
      modlCastItems.set_value(position, 0, name[1])
      if name[2] is True:
        modlCastItems.set_value(position, 1, 'Yes')
      else:
        modlCastItems.set_value(position, 1, 'No')


   # selection=treeCastItems.get_selection()
   # selection.select_path(0)

def CastlistClick(treeview, event, pyCast):
  '''What to do when the Castlist is clicked'''
  # Right Click
  # WARNING: Below is a dirty copy paste, clean it up sometime!
  if event.button == 3:
    x, y = int(event.x), int(event.y)
    time = event.time
    pthinfo = treeview.get_path_at_pos(x, y)
    if pthinfo != None:
      path, col, cellx, celly = pthinfo
      treeview.grab_focus()
      treeview.set_cursor( path, col, 0)  
      popup=gtk.glade.XML(GLADEFILE,"CastsMenu").get_widget("CastsMenu")
      popup.popup( None, None, None, event.button, time)
      dic = { "on_editcast" : EditCastDialog }
      #popup.signal_autoconnect (dic) 
    return 1
  elif event.button == 1:  
    DisplayItems(pyCast.pyCast,pyCast.podCast)





