#! /usr/bin/python
# pycast/pycast2.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et:ft=python:
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

import conf

import castdlgs
import miscdlgs
import casttree
import casts
import thread


def main():

  pyCast=gtk.glade.XML (conf.GLADEFILE,"pycast")
  
  dic = { "on_pycast_destroy" : (Exit),
              "on_addcast" : (castdlgs.AddCast,pyCast),
              "on_aboutdialog" : miscdlgs.About, 
              "on_castlist_click" : casttree.CastlistClick, 
              "on_removecast" : (castdlgs.RemoveCast,pyCast)}

  pyCast.signal_autoconnect (dic)

  casttree.ListCasts(pyCast)
  gtk.threads_init()  
  conf.Load()
  thread.start_new_thread(casts.DownloadRSS,(pyCast,''))

  gtk.threads_enter()
  gtk.main()
  gtk.threads_leave()

  
def Exit(widget):
  thread.exit()
  gtk.main_quit()
        
if __name__ == "__main__":
  main()




