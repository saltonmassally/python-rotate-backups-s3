rotate-backups-s3: Simple command line interface for S3 backup rotation
=======================================================================

Commandline utility to rotate backup files stored in AWS S3.
Based on the excellent work of https://github.com/xolox/python-rotate-backups

.. contents::
   :local:

Features
--------
 

**Flexible rotation**
  Rotation with any combination of hourly, daily, weekly, monthly and yearly
  retention periods.

**Fuzzy timestamp matching in filenames**
  The modification times of the files and/or directories are not relevant. If
  you speak Python regular expressions, here is how the fuzzy matching
  works::

   # Required components.
   (?P<year>\d{4}) \D?
   (?P<month>\d{2}) \D?
   (?P<day>\d{2}) \D?
   (
      # Optional components.
      (?P<hour>\d{2}) \D?
      (?P<minute>\d{2}) \D?
      (?P<second>\d{2})?
   )?

**All actions are logged**
  Log messages are saved to the system log (e.g. ``/var/log/syslog``) so you
  can retrace what happened when something seems to have gone wrong.

Installation
------------

The `rotate-backups-s3` package is available on PyPI_ which means installation
should be as simple as:

.. code-block:: sh

   $ pip install rotate-backups-s3


Usage
-----

There are two ways to use the `rotate-backups-s3` package: As the command line
program ``rotate-backups-s3`` and as a Python API
The command line interface is described below.

Command line
~~~~~~~~~~~~

.. A DRY solution to avoid duplication of the `rotate-backups-s3 --help' text:
..
.. [[[cog
.. from humanfriendly.usage import inject_usage
.. inject_usage('rotate_backups.cli')
.. ]]]

**Usage:** `rotate-backups [OPTIONS] DIRECTORY..`

Easy rotation of backups based on the Python package by the same name. To use this program you specify a rotation scheme via (a combination of) the ``--hourly``, ``--daily``, ``--weekly``, ``--monthly`` and/or ``--yearly`` options and specify the directory (or multiple directories) containing backups to rotate as one or more positional arguments.

Instead of specifying directories and a rotation scheme on the command line you can also add them to a configuration file.

Please use the ``--dry-run`` option to test the effect of the specified rotation scheme before letting this program loose on your precious backups! If you don't test the results using the dry run mode and this program eats more backups than intended you have no right to complain ;-).

**Supported options:**

.. csv-table::
   :header: Option, Description
   :widths: 30, 70


   "``-U``, ``--aws-access-key-id=xxxxxx``","Set the number of daily backups to preserve during rotation. Refer to the
   usage of the ``-H``, ``--hourly`` option for details."
   "``-P``, ``--aws-secret-access-key=xxxxxx``","AWS S3 secret key."
   "``-H``, ``--hourly=COUNT``","Set the number of hourly backups to preserve during rotation:
   
   - If ``COUNT`` is an integer it gives the number of hourly backups to preserve,
     starting from the most recent hourly backup and counting back in time.
   - You can also pass ""always"" for ``COUNT``, in this case all hourly backups are
     preserved.
   - By default no hourly backups are preserved."
   "``-d``, ``--daily=COUNT``","Set the number of daily backups to preserve during rotation. Refer to the
   usage of the ``-H``, ``--hourly`` option for details."
   "``-w``, ``--weekly=COUNT``","Set the number of weekly backups to preserve during rotation. Refer to the
   usage of the ``-H``, ``--hourly`` option for details."
   "``-m``, ``--monthly=COUNT``","Set the number of monthly backups to preserve during rotation. Refer to the
   usage of the ``-H``, ``--hourly`` option for details."
   "``-y``, ``--yearly=COUNT``","Set the number of yearly backups to preserve during rotation. Refer to the
   usage of the ``-H``, ``--hourly`` option for details."
   "``-I``, ``--include=PATTERN``","Only process backups that match the shell pattern given by ``PATTERN``. This
   argument can be repeated. Make sure to quote ``PATTERN`` so the shell doesn't
   expand the pattern before it's received by rotate-backups."
   "``-x``, ``--exclude=PATTERN``","Don't process backups that match the shell pattern given by ``PATTERN``. This
   argument can be repeated. Make sure to quote ``PATTERN`` so the shell doesn't
   expand the pattern before it's received by rotate-backups."
   "``-c``, ``--config=PATH``","Load configuration from the pathname given by ``PATH``. If this option isn't
   given two default locations are checked: ""~/.rotate-backups.ini"" and
   ""/etc/rotate-backups.ini"". The first of these two configuration files to
   exist is loaded. For more details refer to the online documentation."
   "``-n``, ``--dry-run``","Don't make any changes, just print what would be done. This makes it easy
   to evaluate the impact of a rotation scheme without losing any backups."
   "``-v``, ``--verbose``",Make more noise (increase logging verbosity).
   "``-h``, ``--help``","Show this message and exit.
   "

.. [[[end]]]

Configuration files
~~~~~~~~~~~~~~~~~~~

Instead of specifying directories and rotation schemes on the command line you
can also add them to a configuration file.

By default two locations are checked for a configuration file, these are
``~/.rotate-backups-s3.ini`` and ``/etc/rotate-backups-s3.ini``. The first of these
that exists is loaded. You can load a configuration file in a nonstandard
location using the command line option ``--config``.

Configuration files use the familiar INI syntax. Each section defines a
directory that contains backups to be rotated. The options in each section
define the rotation scheme and other options. Here's an example

.. code-block:: ini

   # /etc/rotate-backups-s3.ini:
   # Configuration file for the rotate-backups program that specifies
   # buckets containing backups to be rotated according to specific
   # rotation schemes.

   [laptop]
   hourly = 24
   daily = 7
   weekly = 4
   monthly = 12
   yearly = always

   [server]
   daily = 7
   weekly = 4
   monthly = 12
   yearly = always

   [mopidy]
   daily = 7
   weekly = 4
   monthly = 2

   [xbmc]
   daily = 7
   weekly = 4
   monthly = 2
