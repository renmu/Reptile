#!/usr/bin/python
#coding=utf-8

import urllib2
import re
import parsers

def getWebByUrl(url):
  website = urllib2.urlopen(url)
  #read html code
  html = website.read()
  return html

def findUrlByWeb(html):
  #use re.findall to get all the links
  links = re.findall('"((http|ftp)s?://.*?)"', html)
  return links

if __name__ == "__main__":
  url = "http://www.baidu.com" 
  
  html = webGet(url)
  links = webFindUrl(html)

  b = []
  for a in links:
    b.append(a)
    print a
  print "#######################################"
  print b
