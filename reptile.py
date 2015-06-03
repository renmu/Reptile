#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import store
import urllib2
import re
import os
import sys

class WebCrawler:
  unProcessURLS =[]
  processedURLS = []
  failedURLS = []
  def __init__(self, usage):
    self.usage  = usage
    self.parser = OptionParser(usage)
    self.depth  = 1
    self.number = 1
    self.parser.add_option("-t", "--timeout",
                           action = "store",
                           type = 'int',
                           dest = "timeout",
                           default = 10,
                           help="Specify connection time limit"
                           )
    self.parser.add_option("-u", "--url",
                           action = "store",
                           dest = "url",
                           default = None,
                           help = "Specify the target URL"
                           )
    self.parser.add_option("-n", "--number",
                           action = "store",
                           type = 'int',
                           dest = "maxnum",
                           default = None,
                           help = "Specify the max numbers of target pages"
                           )
    self.parser.add_option("-d", "--depth",
                           action = "store",
                           type = 'int',
                           dest = "depth",
                           default = 2,
                           help = "Specify the max depth of target pages"
                           )
    self.parser.add_option("-p", "--path",
                           action = "store",
                           dest = "path",
                           default = "~/reptile",
                           help = "Specify the pathsite to store pages"
                           )
    self.parser.add_option("-l", "--list",
                           action = "store_true",
                           dest = "show",
                           default = False,
                           help = "list every url mapping to which file."
                           )

  def ParseArgs(self):
    (opts, args) = self.parser.parse_args()
    self.opts = opts
    self.args = args
    if None == opts.url:
      print "You must provide the --url option."
      print os.path.basename(os.path.realpath(sys.argv[0])) + self.usage[5:] 
      exit()
    
    self.startURL = [self.opts.url, 1]
    self.unProcessURLS.append([self.opts.url, 1])

  def PraseProc(self):
    print self.opts.url 
   
  def addReport(reportMsg):
    print reportMsg
  
  def addWebFailed():
    pass

  def addWebSuccessed():
    pass
  
  def getAUrl():
    pass

  def getUrlByString(self, webPage, depth):
    if depth < self.opts.depth:
      links = re.findall('"((http|ftp)s?://.*?)"', webPage)
      for link in links:
        self.unProcessURLS.append([link[0], depth + 1])

  def getWebByUrl(self, url):
    try:
      webPage = urllib2.urlopen(url, timeout = self.opts.timeout).read()
    except urllib2.HTTPError:
      print url
      webPage = None
      pass
    
    return webPage

  def getHashValue(self, url):
    return store.getHashValue(url)

  def storeWeb(self, hashValue, webPage):
    store.saveFile(hashValue, webPage)

  def urlProcTask(self, url, depth):
    webPage = self.getWebByUrl(url)
    if webPage != None:
      hashValue = self.getHashValue(url)
      self.storeWeb(hashValue, webPage)
      self.getUrlByString(webPage, depth) 
      self.updateIndex(hashValue + " " + url + "\n")

  def mainProc(self):
    while len(self.unProcessURLS) > 0:
      unURL = self.unProcessURLS.pop(0)
      self.urlProcTask(unURL[0], unURL[1])

  def updateIndex(self, indexMsg):
    indexfile = os.environ['HOME'] + '/reptile/objs/index'
    store.storeFileAppend(indexfile, indexMsg)
    pass


if __name__ == "__main__":
  usage="%prog { -u http://url [ -t timeout ] [ -n maxnum ] [ -d maxdepth ] | -l } |  [ -p storysite ] "
  myObj = WebCrawler(usage) 
  myObj.ParseArgs()
  myObj.PraseProc()

  myObj.mainProc()
  for a in myObj.unProcessURLS:
    print a
  #print links
  #store.saveFile(store.getHashValue(myObj.opts.url), html)
