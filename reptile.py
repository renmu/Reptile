#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import store
import urllib2
import urllib
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
    """
    解析命令行参数
    """
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
    self.domain   = self.getDomainByUrl(self.opts.url)
    self.unProcessURLS.append([self.opts.url, 1])
    print self.domain
  
  def getDomainByUrl(self, url):
    """
    通过url获取域名
    """
    proto, rest = urllib.splittype(url)
    host, rest = urllib.splithost(rest)
    host, port = urllib.splitport(host)
    return host   

  def urlIsOutLinkStation(self, url):
    """
    判断是否为站外链接
    """
    host = self.getDomainByUrl(url)
    #if host.find(self.domain):
    #  return True
    return False

  def getOneRecord(self, url):
    """
    读取url爬取记录，如果已经爬取则获返回记录条目
    """
    if not os.path.exists(self.indexfile):
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
    """
    判断改url是否已经爬取过了
    """
    line = self.getOneRecord(url)
    if len(line) == 0:
      return False
    else:
      return True

  def listUrl(self, url):
    """
    显示指定的url 对应的文件
    """
    line = self.getOneRecord(url)
    if len(line) == 0:
      print "url:%s is not Crawled or Crawl Failed"% (url)
    else:
      print "url: %s --> file: %s " % (line[41:-1], store.getFullNameByHash(line[0:41]))

  def listAUrl(self):
    """
    显示所有的url 以及对应的文件
    """
    if not os.path.exists(self.indexfile):
      print "index file not found"
      return None
    f = open(self.indexfile, "r")
    line = f.readline()
    while len(line) != 0:
      print "url: %s --> file: %s " % (line[41:-1], store.getFullNameByHash(line[0:41]))
      line = f.readline()

  def addWebFailed(self, errorMsg):
    """
    记录网页抓取错误的log 
    """
    self.fileLock.acquire()
    store.storeLogFile("errorlog", errorMsg + "\n")
    self.fileLock.release()

  def getUrlByString(self, webPage, depth):
    """
    从页面获取url
    """
    if depth < self.opts.depth and self.pageCnts < self.maxnum:
      links = re.findall('"((http|ftp)s?://.*?)"', webPage)
      self.listLock.acquire()
      for link in links:
        # 如果站外链接定定义需要修改的话只修改站外链接判断函数即可
        if not self.urlIsOutLinkStation(link[0]):
          self.unProcessURLS.append([link[0], depth + 1])
      self.listLock.release()

  def getWebByUrl(self, url):
    """
    通过url获取页面
    """
    try:
      html = urllib2.urlopen(url, timeout = self.opts.timeout)
      webPage =  html.read()
    except Exception,e: 
      errorMsg = time.ctime(time.time()) + " " + url + " " + str(e)
      self.addWebFailed(errorMsg) 
      print errorMsg
      webPage = None
    
    return webPage

  def getHashValue(self, url):
    """
    将url转换成hash值
    """
    return store.getHashValue(url)

  def storeWeb(self, hashValue, webPage):
    """
    保存页面
    """
    store.saveFile(hashValue, webPage)

  def urlProcTask(self, url, depth):
    """
    抓取工作任务，多线程实例
    """
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
    """
    主处理流程，控制线程数量，启动抓取url线程抓取
    """
    while len(self.unProcessURLS) > 0 or self.threadCnts > 0:
      if len(self.unProcessURLS) > 0:
        if self.threadCnts < self.maxThreads:
          self.listLock.acquire()
          unURL = self.unProcessURLS.pop(0)
          self.threadCnts += 1
          self.listLock.release()
          thread.start_new_thread( self.urlProcTask, (unURL[0], unURL[1]) )

  def updateIndex(self, indexMsg):
    """
    抓取页面保存后更新index文件，多线程操作需要锁保护
    """
    self.fileLock.acquire()
    store.storeFileAppend(self.indexfile, indexMsg)
    self.fileLock.release()

  def cmdProc(self):
    """
    命令行启动处理入口
    """
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

