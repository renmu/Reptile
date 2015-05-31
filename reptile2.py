#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  

class MyOptionParser:
  def __init__(self, usage):
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

  def ParseArgs(self):
    (options, args) = self.parser.parse_args()
    self.options = options
    self.args    = args

  def PraseProc(self):
    print self.options.url 

def MyParser():
  usage="usage:%prog -u http://url [ -t timeout ] -n maxnum -d maxdepth -p storysite " 
   
  parser = OptionParser(usage)
  parser.add_option("-t", "--timeout",  
                  action = "store",  
                  type = 'int',  
                  dest = "timeout",  
                  default = None,  
                  help="Specify connection time limit"  
                  )  
  parser.add_option("-u", "--url",  
                  action = "store",  
                  dest = "url",  
                  default = None,  
                  help = "Specify the target URL"  
                  )  
  parser.add_option("-n", "--number",  
                  action = "store",  
                  type = 'int',  
                  dest = "maxnum",  
                  default = None,  
                  help = "Specify the max numbers of target pages"  
                  )  
  parser.add_option("-d", "--depth",  
                  action = "store",  
                  type = 'int',  
                  dest = "depth",  
                  default = None,  
                  help = "Specify the max depth of target pages"  
                  )  
  parser.add_option("-p", "--path",  
                  action = "store",  
                  dest = "path",  
                  default = "~/reptile",  
                  help = "Specify the pathsite to store pages"  
                  )  
  (options, args) = parser.parse_args()  
    
  if None == options.url:
     print "You must provide the --url option."
     exit()
  return options 

if __name__ == "__main__":
  usage="usage:%prog -u http://url [ -t timeout ] -n maxnum -d maxdepth -p storysite "
  myObj = MyOptionParser(usage) 
  myObj.ParseArgs()
  myObj.PraseProc()
