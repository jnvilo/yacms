#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2009-2011 by Jason Viloria , see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import division, absolute_import, print_function, unicode_literals
import os
import sys

from setuptools import setup, find_packages, Command

VERSION_STRING="0.0.1"


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_authors():
    try:
        f = file(os.path.join(PACKAGE_ROOT, "AUTHORS"), "r")
        authors = [l.strip(" *\r\n") for l in f if l.strip().startswith("*")]
        f.close()
    except Exception:
        evalue = sys.exc_info()[1]
        authors = "[Error: %s]" % evalue
    return authors


setup(
    name='yacms',
    version=VERSION_STRING,
    description='Yet another CMS. This one for django.',
    author=get_authors(),
    author_email="jnvilo@gmail.com",
    maintainer="Jason Viloria",
    url='http://bitbucket.org/jnvilo/yacms.git',
    packages=find_packages(),
    include_package_data=True, # include package data under svn source control
   install_requires=["djangorestframework", "django-filter", "beautifulsoup4","sh", "pathlib", "loremipsum"],
    data_files=[("", ["README.txt"])], # README used in unittest test_setup_utils.py
    #entry_points={
    #    "console_scripts": [
    #        "creole2html = creole.cmdline:cli_creole2html",
    #        "html2creole = creole.cmdline:cli_html2creole",
    #        "html2rest = creole.cmdline:cli_html2rest",
    #        "html2textile = creole.cmdline:cli_html2textile",
    #    ],
    #},
    zip_safe=True, # http://packages.python.org/distribute/setuptools.html#setting-the-zip-safe-flag
    keywords="django cms",
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
#        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.2",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    #test_suite="yacms.tests.get_test_suite",
)
