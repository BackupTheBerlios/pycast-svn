import gtk
import gtk.glade

class AddCast:
  def __init__(self,Casts):
    '''Opens the Add Cast Dialog'''
    self.Casts=Casts
    self.wAddCast=gtk.glade.XML ("pycast.glade","addcast")
    dic = { "on_addcastok" : (self.Ok),
            "on_addcastcancel" : (self.Cancel)}
    self.wAddCast.signal_autoconnect (dic) 

           
  def Ok(self,widget):
    '''When the Add Cast Dialog's OK button is hit'''
    window=self.wAddCast.get_widget("addcast")
    txtAddCastName = self.wAddCast.get_widget("tAddCastName").get_text()
    txtAddCastUrl = self.wAddCast.get_widget("tAddCastUrl").get_text()
    close=True
    for name in self.Casts.names:
      if self.wAddCast.get_widget("tAddCastName").get_text() == name:
        self.wAddCast.get_widget("tAddCastName").set_text("Name Already Used") 
        close=False
    if close is True:
      if self.wAddCast.get_widget("cAddCastUpdate").get_mode() is True: 
        val="1"
      else:
        val="0"
      self.Casts.add_cast(txtAddCastName,txtAddCastUrl,val)
      self.Casts.write()
      appgui.UpdateCastDisplay()
      window.destroy()


  def Cancel(self,widget):
    '''When the add cast dialog's cancel button is hit'''
    window=self.wAddCast.get_widget("addcast")
    window.destroy()
