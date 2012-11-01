#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup
import realtime_web

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
src_dir = 'realtime_web'

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for dirpath, dirnames, filenames in os.walk(src_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
         packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name             = 'realtime_web',
    version          = realtime_web.__version__,
    author           = u'Bastian Kuberek',
    author_email     = 'bkuberek@gmail.com',
    maintainer       = u'Bastian Kuberek',
    maintainer_email = 'bkuberek@gmail.com',
    url              = 'https://github.com/bkuberek/realtime_web_test',
    description      = u'Exploring websockets and messaging. This test project combines code samples found on the web.',
    packages         = packages,
    data_files       = [] + data_files,
)
