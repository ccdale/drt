#
# Copyright (c) 2018, Christopher Allison
#
#     This file is part of drt.
#
#     drt is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     drt is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with drt.  If not, see <http://www.gnu.org/licenses/>.
"""
setup module for drt application
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from drt import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name = "drt",
        version = __version__,
        description = "dvd copying and ripping management tool",
        long_description = long_description,
        url = "https://github.com/ccdale/drt",
        author = "Christopher Allison",
        author_email = "chris.charles.allison+drt@gmail.com",
        classifiers = [
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Topic :: Multimedia :: Video :: Conversion",
            "Topic :: System :: Archiving",
            "Topic :: System :: Archiving :: Backup",
            "Topic :: System :: Archiving :: Compression",
            "Topic :: System :: Archiving :: Mirroring",
            "Topic :: Utilities"
            ],
        keywords = "dvd copying ripping conversion",
        packages = ["drt"],
        install_requires=["docopt"],
        project_urls = {
            "Source": "https://github.com/ccdale/drt",
            "Bug Reports": "https://github.com/ccdale/drt/issues"
            },
        python_requires = ">=3",
        entry_points ={
            "console_scripts": [
                "dvdcopy = drt.drt:main",
                "dvdprocess = drt.drtp:main"
                ]
            }
        )
