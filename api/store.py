#!/usr/bin/python
#coding=utf-8

import os
import hashlib

def getHashValue(url):
  """
  将url转换成hash字符串
  """
  return hashlib.sha1(url).hexdigest()

def storeProc(fun1, fun2, f1arg1, f2arg1, f2arg2):
  """
  保存文件回调函数的处理方式，尝试了一下还是OK的
  """
  if fun1(f1arg1):
    fun2(f2arg1, f2arg2)
  else:
    pass  # log

def myMkdir(path):
  """
  创建目录
  """
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
  """
  保存页面对象文件
  """
  fo = open(filename, "wb")
  fo.write(msg)
  fo.close()  

def storeFileAppend(filename, msg):
  """
  保存文件追加模式，用来记录index和log
  """
  fo = open(filename, "a")
  fo.write(msg)
  fo.close() 

def getObjFullName(basepath, filename):
  """
  获取保存对象的全名，如果是相对路径转换为绝对路径，将40位hash前两位转换为路径，后38位转换为文件名
  """
  if os.path.isabs(basepath):
    fullName = os.path.join(basepath, filename[0:2], filename[2:]) 
  else:
    fullName = os.path.join(os.getcwd(), basepath, filename[0:2], filename[2:])
  return fullName

def getFullName(basepath, filename):
  """
  获取文件全名，如果是相对路径转换为绝对路径
  """
  if os.path.isabs(basepath):
    fullName = os.path.join(basepath, filename)
  else:
    fullName = os.path.join(os.getcwd(), basepath, filename)
  return fullName

def storeLogFile(filename, msg, basepath=(os.environ['HOME'] + '/reptile/log')):
  """
  写log文件
  """
  fullName = getFullName(basepath, filename)
  storeProc(myMkdir, storeFileAppend, os.path.dirname(fullName), fullName, msg) 

def getFullNameByHash(hashValue, basepath=(os.environ['HOME'] + '/reptile/objs')):
  """
  通过hashvalue 获取全名
  """
  return getObjFullName(basepath, hashValue)

def saveFile(filename, msg, basepath=(os.environ['HOME'] + '/reptile/objs')):
  """
  保存文件，将文件名转换成保存页面对象名的形式，然后写入文件
  """
  fullName = getObjFullName(basepath, filename)
  storeProc(myMkdir, storeFile, os.path.dirname(fullName), fullName, msg) 


if __name__ == "__main__": 
   saveFile(getHashValue("http://www.baidu.com"), "msg\n", "abc/def")
