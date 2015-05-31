#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  

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

print opt.url
