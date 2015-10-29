#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import logging
import sys
import argparse
import time
import datetime

try:
    import simplejson as json
except:
    import json

from _zuora.base import ZuoraBaseClient


logger = logging.getLogger(__name__)
class Export():
    """Calls Zuora"""
    logger = logger
    
    client = None
    username = None; password = None
    zobject = None; objects = []
    filename = None
    fields = None; filter=""
    urlclient = None
    server = ''
    days = 0
    ids_only = False
    droppath = None
    
    def __init__(self, zobject, username, password, wsdl, server, days, ids_only, 
                 droppath=None, now=False):
        """Initialize Export""" 
        self.logger.info("Initializing Export(%s)" % zobject[0])
        self.username = username
        self.password = password
        self.fields = zobject[1]
        self.zobject = zobject[0]
        self.wsdl = wsdl
        self.server = server
        self.days = days
        self.filename = self.zobject
        self.ids_only = ids_only
        self.droppath = droppath
        self.now = now
        
        self.object = []
        
        filterDate = datetime.datetime.now()
        if self.now:
            filterDate = filterDate + datetime.timedelta(days=1)
            self.logger.info("...filter 'now' (%s)" % (filterDate))

        if int(self.days) > 0:
            self.logger.info("...Filter on UpdatedDate (%s)" % self.days)
            lastUpdatedDate = datetime.timedelta(days=self.days)
            lastUpdatedDate = filterDate - lastUpdatedDate
            lastUpdatedDate = "%s/%s/%s" % (lastUpdatedDate.month, lastUpdatedDate.day, lastUpdatedDate.year)
            self.filter = "UpdatedDate >= '%s'" % (lastUpdatedDate)
        else:
            self.logger.info("...Query All")
            lastUpdatedDate = filterDate
            lastUpdatedDate = "%s/%s/%s" % (lastUpdatedDate.month, lastUpdatedDate.day, lastUpdatedDate.year)
            if not self.now:
                self.logger.info("...starting yesterday midnight")
                self.filter = "UpdatedDate <= '%s'" % (lastUpdatedDate)
        
        kwargs = {
                  "username" : self.username, 
                  "password" : self.password, 
                  "sessionLengthMillis" : 600000,
                   }   
        self.client = ZuoraBaseClient(self.wsdl, **kwargs)
        self.logger.info("Zuora Client Initialized")

    def _export(self):
        self.logger.info("Getting %ss" % self.zobject)
        self.logger.info("Filtering on %s" % self.filter)
        fileId = self.client.export(self.zobject, self.fields, self.filter)
        return fileId
    
    def _download(self, fileId):
        self.logger.info("Requesting download ....")
        
        filename = self.filename
        if self.ids_only:
            filename = '%sID' % self.filename 
        self.client.download(fileId, filename, self.droppath)     

    def run(self):
        fileId = self._export()
        if fileId is not None:
            self._download(fileId)

            self.logger.info("%s.csv exported" % self.zobject) 
        else:
            self.logger.error('An error occurred')