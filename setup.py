#!/usr/bin/env python

import re
import sys
import subprocess
import sys

from setuptools import setup, find_packages, Extension
try:
    from Cython.Build import cythonize
except ImportError:
     def cythonize(*args, **kwargs):
         from Cython.Build import cythonize
         return cythonize(*args, **kwargs)

def version():
    with open('naminggamesal/_version.py') as f:
        return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read()).group(1)

def requirements():
    with open('requirements.txt') as f:
        return f.readlines()

setup(name='naminggamesal',
      version=version(),
      packages=find_packages(),
      install_requires=[requirements()],
      setup_requires=['setuptools>=18.0','Cython'],
      author='William Schueller',
      author_email='william.schueller@gmail.com',
      description='Using Active Learning in Naming Games',
      url='https://github.com/flowersteam/naminggamesal',
      license='GNU AFFERO GENERAL PUBLIC LICENSE Version 3',
      #ext_modules = cythonize(['naminggamesal/ngmeth_utils/csrtheo_utils.pyx','naminggamesal/ngvoc/c2dictdict.pyx']),
      ext_modules=
        [Extension(name='naminggamesal.ngmeth_utils.csrtheo_utils',sources=['naminggamesal/ngmeth_utils/csrtheo_utils.pyx']),
        Extension(name='naminggamesal.ngvoc.c2dictdict',sources=['naminggamesal/ngvoc/c2dictdict.pyx']),
        ]
    )

