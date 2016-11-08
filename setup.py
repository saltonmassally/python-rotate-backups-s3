
#!/usr/bin/env python

# Setup script for the `rotate-backups' package.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: March 21, 2016
# URL: https://github.com/xolox/python-rotate-backups


"""
Setup script for the ``rotate-backups-s3`` package.

**python setup.py install**
  Install from the working directory into the current Python environment.

**python setup.py sdist**
  Build a source distribution archive.
"""

# Standard library modules.
import codecs
import os
import re

# De-facto standard solution for Python packaging.
from setuptools import setup, find_packages

# Find the directory where the source distribution was unpacked.
source_directory = os.path.dirname(os.path.abspath(__file__))

# Find the current version.
module = os.path.join(source_directory, 'rotate_backups_s3', '__init__.py')
for line in open(module):
    match = re.match(r'^__version__\s*=\s*["\']([^"\']+)["\']$', line)
    if match:
        version_string = match.group(1)
        break
else:
    raise Exception("Failed to extract version from %s!" % module)

# Fill in the long description (for the benefit of PyPI)
# with the contents of README.rst (rendered by GitHub).
readme_file = os.path.join(source_directory, 'README.rst')
with codecs.open(readme_file, 'r', 'utf-8') as handle:
    readme_text = handle.read()

setup(name='rotate-backups-s3',
      version=version_string,
      description="Simple command line interface for S3 backup rotation",
      long_description=readme_text,
      url='https://github.com/tarzan0820/python-rotate-backups-s3',
      author='Salton Massally',
      author_email='salton.massally@gmail.com',
      packages=find_packages(),
      entry_points=dict(console_scripts=[
          'rotate-backups-s3 = rotate_backups_s3.cli:main'
      ]),
      install_requires=[
          'rotate-backups==4.3',
          'boto',
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development',
          'Topic :: System :: Archiving :: Backup',
          'Topic :: System :: Systems Administration',
      ])
