#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import web
from api import store
import os
import sys

class WebCrawler:
  startURL = []
  unProcessURLS =[]
  processURLS = []
  def __init__(self, usage):
    self.usage  = usage
    self.parser = OptionParser(usage)
    self.depth  = 1
    self.number = 1
    self.parser.add_option("-t", "--timeout",
                           action = "store",
                           type = 'int',
                           dest = "timeout",
                           default = None,
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
                           default = None,
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
    
    self.startURL.append( [(self.opts.url, "http"), 1])

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

  def getUrlByString(self, url, depth):
    print url
    html = web.webGet(url)
    links = web.webFindUrl(html)
    for l in links:
      self.startURL.append([l, depth + 1])
    pass

  def getWebByUrl():
    pass

  def getHashValue():
    pass


if __name__ == "__main__":
  usage="%prog { -u http://url [ -t timeout ] [ -n maxnum ] [ -d maxdepth ] | -l } |  [ -p storysite ] "
  myObj = WebCrawler(usage) 
  myObj.ParseArgs()
  myObj.PraseProc()

  a = myObj.startURL[0]
  url = a[0][0]
  depth = a[1]
  myObj.getUrlByString(url, depth)

  for a in myObj.startURL:
    print a
  #print links
  #store.saveFile(store.getHashValue(myObj.opts.url), html)
