#!/usr/bin/env python

import os
import sys

import fn

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

short = 'Implementation of missing features to enjoy functional programming in Python'
descr = open('README.md').read() + '\n\n' + open('HISTORY.md').read()
license = open('LICENSE').read()

setup(
    name = 'fn',
    version = fn.__version__,
    description = short,
    long_description = descr,
    author='Alexey Kachayev',
    author_email='kachayev@gmail.com',
    url='https://github.com/kachayev/fn.py',
    packages=['fn'],
    package_data={'': ['LICENSE']},
    package_dir={'fn': 'fn'},
    include_package_data=True,
    install_requires=[],
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)
