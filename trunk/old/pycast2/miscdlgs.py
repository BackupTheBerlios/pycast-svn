import gtk
import gtk.glade

from conf import GLADEFILE

class About:
  def __init__(self,widget):
    '''Opens the About Dialog'''
    self.wAbout=gtk.glade.XML (GLADEFILE,"about")
    dic = { "on_about_ok" : (self.AboutClose) }
    self.wAbout.signal_autoconnect (dic)    
    
  def AboutClose(self,widget):
    window=self.wAbout.get_widget("about")
    window.destroy() 
