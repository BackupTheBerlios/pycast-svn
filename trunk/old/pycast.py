#!/usr/bin/env python

import sys
try:
  import pygtk
  #tell pyGTK, if possible, that we want GTKv2
  pygtk.require("2.0")
except:
  print "You need to install pyGTK or GTKv2 or set your PYTHONPATH correctly"
  print "try: export PYTHONPATH=/usr/local/lib/python2.3/site-packages/"
  sys.exit(1)
  
import gtk
import gtk.glade
import gobject
import flatdb

sCastConfig="/home/iphitus/.pycast/casts"
Casts=app.CastList(sCastConfig)
Casts.load()

class appgui:
  def __init__(self):
    '''Create App window'''
    self.wPyCast=gtk.glade.XML ("pycast.glade","pycast")

    dic = { "on_pycast_destroy" : (gtk.main_quit),
            "on_addcast" : self.AddCastDialog,
            "on_aboutdialog" : self.AboutDialog, 
            "on_castlist_click" : self.CastlistClick, 
            "on_editcast" : self.EditCastDialog }

    self.wPyCast.signal_autoconnect (dic)
    self.ListCasts()  
    
 
      
  ###################
  # Cast list stuff #
  ###################

  def ListCasts(self):
    '''Lists all the casts into their container'''
    # Create objects for the treelist of casts
    self.treeCastList=self.wPyCast.get_widget("podcastlist")
    self.modlCastList=gtk.TreeStore(gobject.TYPE_STRING,
                             gobject.TYPE_STRING)
    self.treeCastList.set_model(self.modlCastList)  
    self.treeCastList.set_headers_visible(gtk.FALSE)    

    # Set the columns
    column=gtk.TreeViewColumn("Podcast",gtk.CellRendererText(), text=0)
    column.set_resizable(gtk.TRUE)
    self.treeCastList.append_column(column)
    x=0  
     
    # Loop through and add the casts
    while x<len(Casts.names):
      position=self.modlCastList.insert_after(None,None)
      self.modlCastList.set_value(position, 0, Casts.names[x])
      x=x+1
    selection=self.treeCastList.get_selection()
    selection.select_path(0)
      
  def UpdateCastDisplay(self):
    '''Update the cast treelist'''
    ## EXTRA CODE??
    self.treeCastList=self.wPyCast.get_widget("podcastlist")
    self.modlCastList=gtk.TreeStore(gobject.TYPE_STRING,
                             gobject.TYPE_STRING)
    self.treeCastList.set_model(self.modlCastList)  
    self.treeCastList.set_headers_visible(gtk.FALSE)    
    x=0
    while x<len(Casts.names):
      position=self.modlCastList.insert_after(None,None)
      self.modlCastList.set_value(position,0,Casts.names[x])
      x=x+1    

  def CastlistClick(self, treeview, event):
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
            self.popup=gtk.glade.XML("pycast.glade","CastsMenu").get_widget("CastsMenu")
            self.popup.popup( None, None, None, event.button, time)
            dic = { "on_editcast" : self.EditCastDialog }
            self.popup.signal_autoconnect (dic) 
        return 1

  def RemoveCast(self,widget):
    


  ###########
  # Dialogs #
  ###########


  ### Edit Cast Dialog        
  def EditCastDialog(self,widget):
    '''Opens the Edit Cast dialog'''
    self.wEditCast=gtk.glade.XML ("pycast.glade","editcast")
    dic = { "on_editcastok" : (self.EditCastDialogOk),
            "on_editcastcancel" : (self.EditCastDialogCancel)}
    self.wEditCast.signal_autoconnect (dic) 
                
                                
  def EditCastDialogOk(self,widget):
    '''Actions when OK is hit on the Edit Cast Dialog'''
    window=self.wEditCast.get_widget("editcast")
    window.destroy()


  def EditCastDialogCancel(self,widget):
    '''Actions when Cancel is hit on the Edit cast dialog'''
    window=self.wEditCast.get_widget("editcast")
    window.destroy()



  ### Add Cast Dialog     
  def AddCastDialog(self,widget):
    '''Opens the Add Cast Dialog'''
    self.wAddCast=gtk.glade.XML ("pycast.glade","addcast")
    dic = { "on_addcastok" : (self.AddCastDialogOk),
            "on_addcastcancel" : (self.AddCastDialogCancel)}
    self.wAddCast.signal_autoconnect (dic) 
           
  def AddCastDialogOk(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
    window=self.wAddCast.get_widget("addcast")
    txtAddCastName = self.wAddCast.get_widget("tAddCastName").get_text()
    txtAddCastUrl = self.wAddCast.get_widget("tAddCastUrl").get_text()
    close=True
    for name in Casts.names:
      if self.wAddCast.get_widget("tAddCastName").get_text() == name:
        self.wAddCast.get_widget("tAddCastName").set_text("Name Already Used") 
        close=False
    if close is True:
      if self.wAddCast.get_widget("cAddCastUpdate").get_mode() is True: 
        val="1"
      else:
        val="0"
      Casts.add_cast(txtAddCastName,txtAddCastUrl,val)
      Casts.write()
      self.UpdateCastDisplay()
      window.destroy()

  def AddCastDialogCancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    window=self.wAddCast.get_widget("addcast")
    window.destroy()
    
       
               
  ### About Dialog
  def AboutDialog(self,widget):
    self.wAbout=gtk.glade.XML ("pycast.glade","about")
    dic = { "on_about_ok" : (self.AboutClose) }
    self.wAbout.signal_autoconnect (dic)    
    
  def AboutClose(self,widget):
    window=self.wAbout.get_widget("about")
    window.destroy()  


### Start the program!
app=appgui()
gtk.main()



