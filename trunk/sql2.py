#! /usr/bin/python
# sql.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et:ft=python:
# $Id:$
# $Source:$
# 2005-01-28
 
import sqlite
configsql = sqlite.connect("/home/iphitus/conf.db")
sqlcursor = configsql.cursor()

try:
  print sqlcursor.execute("select * from configs;")
  print sqlcursor.fetchall()
  print "hihihi"
  print sqlcursor.execute("insert into configs (firstname, age) values ("J\"es gonna mess this up :(", 21);")
  print "hihihi2i"
  configsql.commit()
  print sqlcursor.execute("select age from configs;") 
  print sqlcursor.fetchone()
  
except:
  print "Not existing, creating."
  print sqlcursor.execute("create table configs (firstname UNICODE, age INT)")
  configsql.commit()
  print sqlcursor.execute("insert into configs (firstname, age) values ('Joe', 21)")
  configsql.commit()
