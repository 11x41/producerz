#!/usr/bin/env python2.7
"""
reg-admin package
"""
from setuptools import setup, find_packages
import subprocess
import os.path

setup(
    author='Business Services',
    author_email='sw-business-svcs@gogrid.com',
    description='Zuora Producer for BI',
    name = 'zuora_producer',
    version = '1.0',
    zip_safe = False,
    url='http://code.gogrid.com/zuora/producerz',
    install_requires = [
        'gg_deploy >=0.2',
        'argparse',
        'zuora-python-toolkit>=1.2.0',
    ],
    data_files = [('/etc/gogrid/zuora-producer', ['conf/zuora-producer.conf', 'conf/export.conf', 'conf/prod.zuora.a.39.0.wsdl'])],
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'': 'src'},
)

# ex: set tabstop=4 expandtab:
# -*- Mode: Python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-