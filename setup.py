#!/usr/bin/env python3

# Imports #
from setuptools import setup, find_packages
import re

# Find version #
def find_version(package):
    init_file = open(package + "/__init__.py").read()
    rex = r'__version__\s*=\s*"([^"]+)"'
    return re.search(rex, init_file).group(1)

# Setup #
setup(
    name="galclass",
    description="GALaxy CLASSifier",
    long_description="A module for the morphological classification of galaxies.",
    author="Stavros Pastras",
    author_email="st.pastras@gmail.com",
    url="https://github.com/spastras/galclass",
    packages=find_packages(),
    version=find_version("galclass"),
    package_data={"galclass": ["resources/*.*"]},
    entry_points={
                  'console_scripts': [
                                      'galclass = galclass.__main__:main',
                                     ],
                 },
)