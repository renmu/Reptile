#!/usr/bin/python
#coding=utf-8

import os
import hashlib

def getHashValue(url):
  return hashlib.sha1(url).hexdigest()

def storeProc(fun1, fun2, f1arg1, f2arg1, f2arg2):
  if fun1(f1arg1):
    fun2(f2arg1, f2arg2)
  else:
    pass  # log

def myMkdir(path):
  if os.path.exists(path):
    if os.path.isdir(path):
      pass 
    else:
      print "error"
      return None
  else:
    os.makedirs(path)
  return path

def storeFile(filename, msg):
  fo = open(filename, "wb")
  fo.write(msg)
  fo.close()  

def storeFileAppend(filename, msg):
  fo = open(filename, "a")
  fo.write(msg)
  fo.close()

def getFullName(basepath, filename):
  if os.path.isabs(basepath):
    fullName = os.path.join(basepath, filename[0:2], filename[2:]) 
  else:
    fullName = os.path.join(os.getcwd(), basepath, filename[0:2], filename[2:])
  return fullName

def saveFile(filename, msg, basepath=(os.environ['HOME'] + '/reptile/objs')):
  fullName = getFullName(basepath, filename)
  storeProc(myMkdir, storeFile, os.path.dirname(fullName), fullName, msg) 

if __name__ == "__main__": 
   saveFile(getHashValue("http://www.baidu.com"), "msg\n", "abc/def")
