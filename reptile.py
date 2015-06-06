#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import store
import urllib2
import time
import thread
import re
import os
import sys

class WebCrawler:
  unProcessURLS =[]
  processedURLS = []
  failedURLS = []
  listLock = thread.allocate_lock()
  fileLock = thread.allocate_lock()
  threadCnts = 0
  maxThreads = 5
  pageCnts = 0
  indexfile = os.environ['HOME'] + '/reptile/objs/index'
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
                           default = 100,
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
    if False == opts.show and None == opts.url:
      print "You must provide the --url option."
      print os.path.basename(os.path.realpath(sys.argv[0])) + self.usage[5:] 
      exit()
    
    self.maxnum   = opts.maxnum
    self.depth    = opts.depth
    self.show     = opts.show
    self.path     = opts.depth
    self.timeout  = opts.timeout
    self.startURL = [self.opts.url, 1]
    self.unProcessURLS.append([self.opts.url, 1])

  def getOneRecord(self, url):
    if False == os.path.exists(self.indexfile):
      return "" 
    f = open(self.indexfile, "r")
    line = f.readline()
    bIsCrawl = False
    while len(line) != 0:
      hashValue = self.getHashValue(url)
      if line.find(hashValue) == -1:
        line = f.readline()
      else:
        bIsCrawl = True
        break
    f.close()
    if True == bIsCrawl:
       return line
    else:
       return ""

  def urlIsCrawlOver(self, url):
    line = self.getOneRecord(url)
    if len(line) == 0:
      return False
    else:
      return True

  def listUrl(self, url):
    line = self.getOneRecord(url)
    if len(line) == 0:
      print "url:%s is not Crawled or Crawl Failed"% (url)
    else:
      print "url: %s --> file: %s " % (line[41:-1], store.getFullNameByHash(line[0:41]))

  def listAUrl(self):
    if False == os.path.exists(self.indexfile):
      print "index file not found"
      return None
    f = open(self.indexfile, "r")
    line = f.readline()
    while len(line) != 0:
      print "url: %s --> file: %s " % (line[41:-1], store.getFullNameByHash(line[0:41]))
      line = f.readline()

  def addReport(reportMsg):
    print reportMsg
  
  def addWebFailed(self, errorMsg):
    self.fileLock.acquire()
    store.storeLogFile("errorlog", errorMsg + "\n")
    self.fileLock.release()

  def getUrlByString(self, webPage, depth):
    if depth < self.opts.depth and self.pageCnts < self.maxnum:
      links = re.findall('"((http|ftp)s?://.*?)"', webPage)
      self.listLock.acquire()
      for link in links:
        self.unProcessURLS.append([link[0], depth + 1])
      self.listLock.release()

  def getWebByUrl(self, url):
    try:
      html = urllib2.urlopen(url, timeout = self.opts.timeout)
      webPage =  html.read()
    except Exception,e: 
      errorMsg = time.ctime(time.time()) + " " + url + " " + str(e)
      self.addWebFailed(errorMsg) 
      print errorMsg
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
      self.getUrlByString(webPage, depth) 
      if False == self.urlIsCrawlOver(url) and self.pageCnts < self.maxnum:
        self.listLock.acquire()
        self.pageCnts += 1
        self.listLock.release()
        hashValue = self.getHashValue(url)
        self.storeWeb(hashValue, webPage)
        self.updateIndex(hashValue + " " + url + "\n")
    self.listLock.acquire()
    self.threadCnts -= 1
    self.listLock.release()

  def mainProc(self):
    while len(self.unProcessURLS) > 0 or self.threadCnts > 0:
      if len(self.unProcessURLS) > 0:
        if self.threadCnts < self.maxThreads:
          self.listLock.acquire()
          unURL = self.unProcessURLS.pop(0)
          self.threadCnts += 1
          self.listLock.release()
          thread.start_new_thread( self.urlProcTask, (unURL[0], unURL[1]) )

  def updateIndex(self, indexMsg):
    self.fileLock.acquire()
    store.storeFileAppend(self.indexfile, indexMsg)
    self.fileLock.release()

  def cmdProc(self):
    self.ParseArgs()
    if True == self.show:
      if None == self.opts.url:
        self.listAUrl()
      else:
        self.listUrl(self.opts.url)
    else:
      self.mainProc()

if __name__ == "__main__":
  usage="%prog { -u http://url [ -t timeout ] [ -n maxnum ] [ -d maxdepth ] | -l } |  [ -p storysite ] "
  myObj = WebCrawler(usage) 
  myObj.cmdProc()

