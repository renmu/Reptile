#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import web
from api import store
import os
import sys

class MyOptionParser:
  def __init__(self, usage):
    self.usage  = usage
    self.parser = OptionParser(usage)
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
      #print self.usage % os.path.basename(os.path.realpath(sys.argv[0])) 
      print os.path.basename(os.path.realpath(sys.argv[0])) + self.usage[5:] 
      exit()

  def PraseProc(self):
    print self.opts.url 


if __name__ == "__main__":
  usage="%prog { -u http://url [ -t timeout ] [ -n maxnum ] [ -d maxdepth ] | -l } |  [ -p storysite ] "
  myObj = MyOptionParser(usage) 
  myObj.ParseArgs()
  myObj.PraseProc()

  html = web.webGet(myObj.opts.url)
  links = web.webFindUrl(html)

  store.saveFile(store.getHashValue(myObj.opts.url), html)
