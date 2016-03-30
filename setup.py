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
setup(
    name='fn.py',
    version=fn.__version__,
    description=short,
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    author='fnpy team',
    author_email='vash0the0stampede@gmail.com',
    url='https://github.com/fnpy/fn.py',
    packages=['fn', 'fn.immutable'],
    package_data={'': ['LICENSE', 'README.rst', 'HISTORY.rst']},
    include_package_data=True,
    install_requires=[],
    license=open('LICENSE').read(),
    zip_safe=False,
    keywords=['functional', 'fp', 'utility'],
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
