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
print sqlcursor.execute("select ")
try:
  print sqlcursor.execute("select * from *;")
  print sqlcursor.fetchall()

  print sqlcursor.execute("insert into configs (firstname, age) values ('Joe', 21);")
  configsql.commit()
  print sqlcursor.execute("select age from configs;") 
  print sqlcursor.fetchone()
  #print sqlcursor.execute(".table")
except:
  print "Not existing, creating."
  print sqlcursor.execute("create table configs (firstname UNICODE, age INT)")
  configsql.commit()
  print sqlcursor.execute("insert into configs (firstname, age) values ('Joe', 21)")
  configsql.commit()
