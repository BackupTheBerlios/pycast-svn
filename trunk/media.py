#! /usr/bin/python
# media.py - downloading, playing and manipulation of casts.
# -*- coding: utf-8 -*-
# vim:ts=2:sw=2:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-24

def DownloadClick(self,widget,pyCast):
  ''' we've clicked the download button, lets download it '''
  pyCast=pyCast.pyCast
  podCast=pyCast.podCast


      self.Rss.create(self.rdb, ['name:str',
                         'date:datetime.datetime',
                         'title:str',
                         'description:str',
                         'link:str',
                         'enclosure:str',
                         'enclosuretype:str',
                         'downloaded:int',
                         'filename:str',
                         'opml:str'])

    # ['recno','name','url','urltype']
    
  treeSelection = treeCastList.get_selection()
  (model, iter) = treeSelection.get_selected()
  
  treeCastList=pyCast.get_widget("podcastitems")
  treeSelection = treeCastList.get_selection()
  (model, iter) = treeSelection.get_selected()
  if podCast.AllCasts !=[]:
    selected = model.get_value(iter,0)
    location = model.get_string_from_iter(iter)
    recno = podCast.ListItems[location][0]
    field = podCast.CastField(podCast.ListItems[location][0]) 
  parameter = [recno,field[0],field[5],field[6]]
  podCast.Download
