#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import logging
import sys
import argparse
import time

from producers.producer.export import Export
from producers.common.config import config

logger = logging.getLogger(__name__)
class ProducerManager():
    """ProducerManager manages the calls to Zuora"""
    logger = logger
    
    zobjects = []
    infoDict = {}
    
    username = None
    password = None
    wsdl = None
    server = None
    days = None
    droppath = None
    ids_only = False
    now = False
    
    def __init__(self, zoptions=[], days=1, ids_only=False, now=False):
        """Initialize ProducerManager with options from the command line
            zoptions is a list of objects from the config/export.conf
            days is the # of days to subtract from yesterday @ midnight
            (UpdatedDate <= yesterday-midnight - days) unless specified with
            the -n / --now parameter, then it run as UpdatedDate <= now - days
        """
        conf = config()

        for section in conf.sections():
            for (name, value) in conf.items(section):
                self.infoDict[section + "." + name] = value
    
        self.logger.debug("Initializing ProducerManager")
        
        self.username = self.infoDict['ZUORA_PRODUCER.username']
        self.password = self.infoDict['ZUORA_PRODUCER.password']
        self.wsdl = self.infoDict['ZUORA_PRODUCER.wsdl']
        self.server = self.infoDict['ZUORA_PRODUCER.server']
        self.droppath = self.infoDict['ZUORA_PRODUCER.droppath']
        self.days = days
        self.ids_only = ids_only
        self.now = now
        
        z = eval(self.infoDict['Z.objects'])
        for item in z:
            fields = eval(self.infoDict['%s.fields' % item.upper()])
            if ids_only:
                fields = ['Id']
            if zoptions is not None:
                if item.lower() in zoptions:
                    self.zobjects.append((item, fields))
            else:
                self.zobjects.append((item, fields))
    
    def run(self):
        """Call Export for all zobjects"""
        for zobject in self.zobjects:
            export = Export(zobject, self.username, self.password, self.wsdl, self.server, self.days, self.ids_only, self.droppath, self.now)
            export.run()

def main():
    parser = argparse.ArgumentParser(description='Zuora Producer Manager ArgParser')
    parser.add_argument('z', nargs='*', default=None, help='A list of Zuora objects.  These are the same names as in the config.  Example: account which maps to [ACCOUNT] in config')
    parser.add_argument('-d', '--days', default=5, type=int, nargs=1, help='The number of days to go back.  Example:  SELECT BLAH WHERE UpdatedDate < now() - 5')
    parser.add_argument('-i', '--ids', action='store_true', default=False, help='Only grab the IDs for the objects')
    parser.add_argument('-n', '--now', action='store_true', default=False, help='Run with date range starting NOW.  Default is midnight of previous day')
    args = parser.parse_args()
    logger.debug("args: %s" % args)
    
    if args.z not in (None, []):
        pm = ProducerManager([z.lower() for z in args.z], args.days[0], args.ids, args.now)
    else:
        pm = ProducerManager(None, args.days if isinstance(args.days, int) else args.days[0], args.ids, args.now)
    pm.run()

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    #logging.getLogger( "suds.client" ).setLevel( logging.DEBUG )
    logging.getLogger( "_zuora.base" ).setLevel( logging.DEBUG )
    logging.getLogger( __name__ ).setLevel( logging.DEBUG )
    logging.getLogger( Export.__module__ ).setLevel( logging.DEBUG )
    main()
