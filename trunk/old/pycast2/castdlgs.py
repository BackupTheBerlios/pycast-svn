import gtk
import gtk.glade
import gobject
import datetime
import casts

from conf import GLADEFILE,CONFIG,CASTDB
from kirbybase import KirbyBase, KBError
from app import delistify
from casttree import UpdateCastDisplay

class AddCast:
  def __init__(self,widget,pyCast):
    '''Opens the Add Cast Dialog'''
    self.pyCast=pyCast
    self.AddCast=gtk.glade.XML (GLADEFILE,"addcast")
    self.wAddCast=self.AddCast.get_widget("addcast")
    dic = { "on_addcastok" : (self.Ok),
            
            "on_addcastcancel" : (self.Cancel)}
    self.AddCast.signal_autoconnect (dic) 
         
  def Ok(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
    Casts = KirbyBase()
    CloseWindow=True
        
    AddCastName = self.AddCast.get_widget("tAddCastName")
    AddCastUrl = self.AddCast.get_widget("tAddCastUrl")
    AddCastUpdate= self.AddCast.get_widget("cAddCastUpdate") 
    
    for name in delistify(Casts.select(CASTDB, ['name'],[''],['name'])):
      if AddCastName.get_text()== name:
        AddCastName.set_text("Name Already Used") 
        CloseWindow=False

    if CloseWindow is True:
      if casts.DownloadTestRSS(AddCastUrl.get_text()):
        Casts.insert(CASTDB, [AddCastName.get_text(),
                                            AddCastUrl.get_text(),
                                            AddCastUpdate.get_mode(),
                                            datetime.datetime.now()])
        casts.DownloadRSS(self.pyCast,AddCastUrl.get_text())
        UpdateCastDisplay(self.pyCast)
        self.wAddCast.destroy()
      

  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    self.wAddCast.destroy()

class EditCast:
  def __init__(self,widget,pyCast):
    '''Opens the Add Cast Dialog'''
    self.pyCast=pyCast
    self.EditCast=gtk.glade.XML (GLADEFILE,"editcast")
    self.wEditCast=self.EditCast.get_widget("editcast")
    dic = { "on_addcastok" : (self.Ok),
            "on_addcastcancel" : (self.Cancel)}
    self.EditCast.signal_autoconnect (dic) 

         
  def Ok(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
    Casts = KirbyBase()
    CloseWindow=True
        
    EditCastName = self.EditCast.get_widget("tEditCastName")
    EditCastUrl = self.EditCast.get_widget("tEditCastUrl")
    EditCastUpdate= self.EditCast.get_widget("cEditCastUpdate") 
    
    for name in delistify(Casts.select(CASTDB, ['name'],[''],['name'])):
      if EditCastName.get_text()== name:
        EditCastName.set_text("Name Already Used") 
        CloseWindow=False
        
    if CloseWindow is True:
      UpdateCastDisplay(self.pyCast)
      self.wEditCast.destroy()

  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    self.wEditCast.destroy()

class RemoveCast:
  def __init__(self,widget,pyCast):
    '''Opens the Add Cast Dialog'''
    self.pyCast=pyCast
    self.RemoveCast=gtk.glade.XML (GLADEFILE,"removecast")
    self.wRemoveCast=self.RemoveCast.get_widget("removecast")
    dic = { "on_removecastok" : (self.Ok),
            "on_removecastcancel" : (self.Cancel)}
    self.RemoveCast.signal_autoconnect (dic) 

         
  def Ok(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
    Casts = KirbyBase()
    treeCastList = self.pyCast.get_widget("podcastlist")
    treeSelection = treeCastList.get_selection()
    (model, iter) = treeSelection.get_selected()
    selected = model.get_value(iter,0)
    print selected
    Casts.delete(CASTDB,['name'],['^'+selected+'$'])
    UpdateCastDisplay(self.pyCast)
    self.wRemoveCast.destroy()

  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    self.wRemoveCast.destroy()
    
