#! /usr/bin/python
# pycast/tests/sqlite.py - <description>
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:et:ft=python:
# $Id:$
# $Source:$
# 2005-02-07
import sqlite
import time
import os

def checkdb(location,table):
  
  ''' checks if file of db exists - needs further checking '''
  
  if os.access(location,os.F_OK) is True:
    try:
      configsql = sqlite.connect(location)
      sqlcursor = configsql.cursor()
      sqlcursor.execute("select * from "+table) 
    except:
      return False
  else:
    return False



       
dbObject = sqlite.connect("/home/iphitus/data.db",encoding='utf-8',autocommit=1)
dbCursor = dbObject.cursor()
#if not checkdb("/home/iphitus/data.db","info"):
#    dbCursor.execute("create table info (name UNICODE, details UNICODE, number INT, date UNICODE)")
                                         
while True:

    command = raw_input(u"What do you want to do?")
    if command == "add":
        name = raw_input (u"What the name?")
        details = raw_input (u"Whats the detail?")
        number = raw_input (u"whats the number?")
        date = time.strftime("%d-%m-%Y")

        dbCursor.execute("insert into info values (%s, %s, %s, %s)",
                    (name,details,int(number),date))
    elif command == "list":
        dbCursor.execute("select * from info")
        print dbCursor.fetchall()

