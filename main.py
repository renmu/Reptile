#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import parsers
from api import web

opt = parsers.MyParser()

html = web.webGet(opt.url)
links = web.webFindUrl(html)
print links
