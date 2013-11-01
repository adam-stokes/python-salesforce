#!/usr/bin/env python

import os
import sys

import sforce

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'sforce',
]

requires = ['requests-oauthlib', 'PyYAML', 'bottle', 'CherryPy', 'pyOpenSSL']

setup(
    name='python-salesforce',
    version=sforce.__version__,
    description='Python Salesforce auth/authorization client.',
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Adam Stokes',
    author_email='adam.stokes@ubuntu.com',
    url='https://github.com/debugmonkey/python-salesforce',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'sforce': 'sforce'},
    scripts=['scripts/sf-exchange-auth', 'scripts/sf-cli'],
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
)
