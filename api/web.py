#!/usr/bin/python
#coding=utf-8

import urllib2
import re
import parsers

def webGet(url):
  website = urllib2.urlopen(url)
  #read html code
  html = website.read()
  return html

def webFindUrl(html):
  #use re.findall to get all the links
  links = re.findall('"((http|ftp)s?://.*?)"', html)
  return links

if __name__ == "__main__":
  url = parsers.MyParser() 
  
  html = webGet(url)
  links = webFindUrl(html)
  print links
