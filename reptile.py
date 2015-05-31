#!/usr/bin/python
#coding=utf-8

from optparse import OptionParser  
from api import parsers
from api import web
from api import store

opt = parsers.MyParser()

html = web.webGet(opt.url)
links = web.webFindUrl(html)

store.saveFile(store.getHashValue(opt.url), html)
