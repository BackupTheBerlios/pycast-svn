#!/usr/bin/env python
import os; tl,f,g=0,os.listdir(os.getcwd()),0; 
for i in f:    
  if i[-3:]==".py":
    t=open(i,'r')
    l=t.readlines()
    tl=tl+len(l)
    t.close();g=g+1
    print tl-g*22
