import gtk
import gtk.glade
import gobject

from conf import GLADEFILE,CASTDB
from kirbybase import KirbyBase, KBError
from app import delistify

def ListCasts(pyCast):
  '''Lists all the casts into their container'''
  treeCastList=pyCast.get_widget("podcastlist")
  modlCastList=gtk.TreeStore(gobject.TYPE_STRING)
  Casts = KirbyBase()
  
  treeCastList.set_model(modlCastList)  
  treeCastList.set_headers_visible(gtk.FALSE)    

    # Set the columns
  column=gtk.TreeViewColumn("Podcast",gtk.CellRendererText(), text=0)
  column.set_resizable(gtk.TRUE)
  treeCastList.append_column(column)
  x=0  
     
    # Loop through and add the casts
  for name in delistify(Casts.select(CASTDB, ['name'],[''],['name'])):
    position=modlCastList.insert_after(None,None)
    modlCastList.set_value(position, 0, name)
    x=x+1
  selection=treeCastList.get_selection()
  selection.select_path(0)
      
def UpdateCastDisplay(pyCast):
  '''Update the cast treelist'''
  ## EXTRA CODE??
  Casts = KirbyBase()
  treeCastList=pyCast.get_widget("podcastlist")
  modlCastList=gtk.TreeStore(gobject.TYPE_STRING)
  treeCastList.set_model(modlCastList)  
  treeCastList.set_headers_visible(gtk.FALSE)    
  x=0
  for name in delistify(Casts.select(CASTDB, ['name'],[''],['name'])):
    position=modlCastList.insert_after(None,None)
    modlCastList.set_value(position,0,name)
    x=x+1    


##########################################
def CastlistClick(treeview, event):
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
      popup.signal_autoconnect (dic) 
    return 1
  elif event.button == 1:  
    treeCastList = self.pyCast.get_widget("podcastlist")
    treeSelection = treeCastList.get_selection()
    (model, iter) = treeSelection.get_selected()
    selected = model.get_value(iter,0)
    Rss.(CASTDB,['name'],['^'+selected+'$'])
                    
