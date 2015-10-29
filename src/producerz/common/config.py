'''
Created on July 29th, 2013

@author: marty
'''

"""

PyNOC Config Class

Implements a single method to return a ConfigParser object
of the PyNOC config file.  This should be the only place
we ever hard code anything (the path to the config file).

"""

import ConfigParser
import os

# hard code config path
PATH_CONFIG = ('/etc/gogrid/zuora-producer/',
               '/opt/projects/gogrid/reg/zuora/producerz/conf/')

CONFIG_FILES = (
    'local.zuora-producer.conf',
    'local.export.conf',
    'zuora-producer.conf',
    'export.conf',    
    )

def config():
    """Load and return config file as a ConfigParser object"""

    config = ConfigParser.SafeConfigParser()

    config.read(os.path.join(os.path.abspath(path), filename)
            for path in PATH_CONFIG for filename in CONFIG_FILES)

    return config