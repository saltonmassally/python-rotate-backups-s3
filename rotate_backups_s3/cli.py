# rotate-backups: Simple command line interface for backup rotation.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: March 20, 2016
# URL: https://github.com/xolox/python-rotate-backups

"""
Usage: rotate-backups-s3 [OPTIONS] DIRECTORY..

Easy rotation of backups in an AWS S3 bucket based. To use
this program you specify a rotation scheme via (a combination of) the --hourly,
--daily, --weekly, --monthly and/or --yearly options and specify the bucket
(or multiple buckets) containing backups to rotate as one or more
positional arguments.

Instead of specifying directories and a rotation scheme on the command line you
can also add them to a configuration file. For more details refer to the online
documentation (see also the --config option).

Please use the --dry-run option to test the effect of the specified rotation
scheme before letting this program loose on your precious backups! If you don't
test the results using the dry run mode and this program eats more backups than
intended you have no right to complain ;-).

Supported options:

  -U, --aws-access-key-id
    
    AWS S3 access ID; ensure that it has enough rights to list and delete from
    a bucket

  -P, --aws-secret-access-key
    
    AWS S3 secret key

  -H, --hourly=COUNT

    Set the number of hourly backups to preserve during rotation:

    - If COUNT is an integer it gives the number of hourly backups to preserve,
      starting from the most recent hourly backup and counting back in time.
    - You can also pass `always' for COUNT, in this case all hourly backups are
      preserved.
    - By default no hourly backups are preserved.

  -d, --daily=COUNT

    Set the number of daily backups to preserve during rotation. Refer to the
    usage of the -H, --hourly option for details.

  -w, --weekly=COUNT

    Set the number of weekly backups to preserve during rotation. Refer to the
    usage of the -H, --hourly option for details.

  -m, --monthly=COUNT

    Set the number of monthly backups to preserve during rotation. Refer to the
    usage of the -H, --hourly option for details.

  -y, --yearly=COUNT

    Set the number of yearly backups to preserve during rotation. Refer to the
    usage of the -H, --hourly option for details.

  -I, --include=PATTERN

    Only process backups that match the shell pattern given by PATTERN. This
    argument can be repeated. Make sure to quote PATTERN so the shell doesn't
    expand the pattern before it's received by rotate-backups.

  -x, --exclude=PATTERN

    Don't process backups that match the shell pattern given by PATTERN. This
    argument can be repeated. Make sure to quote PATTERN so the shell doesn't
    expand the pattern before it's received by rotate-backups.

  -c, --config=PATH

    Load configuration from the pathname given by PATH. If this option isn't
    given two default locations are checked: `~/.rotate-backups-s3.ini' and
    `/etc/rotate-backups-s3.ini'. The first of these two configuration files to
    exist is loaded. For more details refer to the online documentation.

  -n, --dry-run

    Don't make any changes, just print what would be done. This makes it easy
    to evaluate the impact of a rotation scheme without losing any backups.

  -v, --verbose

    Make more noise (increase logging verbosity).

  -h, --help

    Show this message and exit.
"""

# Standard library modules.
import getopt
import logging
import sys

# External dependencies.
import coloredlogs
from humanfriendly import parse_path
from humanfriendly.terminal import usage

# Modules included in our package.
from rotate_backups import coerce_retention_period, load_config_file
from rotate_backups_s3 import S3RotateBackups

# Initialize a logger.
logger = logging.getLogger(__name__)


def main():
    """Command line interface for the ``rotate-backups-s3`` program."""
    coloredlogs.install(syslog=True)
    # Command line option defaults.
    aws_access_key_id = None
    aws_secret_access_key = None
    config_file = None
    dry_run = False
    exclude_list = []
    include_list = []
    rotation_scheme = {}
    # Parse the command line arguments.
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'U:P:H:d:w:m:y:I:x:c:nvh', [
            'aws_access_key_id=', 'aws_secret_access_key=', 'hourly=', 'daily=',
            'weekly=', 'monthly=', 'yearly=', 'include=',
            'exclude=', 'config=', 'dry-run', 'verbose', 'help',
        ])
        for option, value in options:
            if option in ('-H', '--hourly'):
                rotation_scheme['hourly'] = coerce_retention_period(value)
            elif option in ('-d', '--daily'):
                rotation_scheme['daily'] = coerce_retention_period(value)
            elif option in ('-w', '--weekly'):
                rotation_scheme['weekly'] = coerce_retention_period(value)
            elif option in ('-m', '--monthly'):
                rotation_scheme['monthly'] = coerce_retention_period(value)
            elif option in ('-y', '--yearly'):
                rotation_scheme['yearly'] = coerce_retention_period(value)
            elif option in ('-I', '--include'):
                include_list.append(value)
            elif option in ('-x', '--exclude'):
                exclude_list.append(value)
            elif option in ('-c', '--config'):
                config_file = parse_path(value)
            elif option in ('-U', '--aws-access-key-id'):
                aws_access_key_id = value
            elif option in ('-P', '--aws-secret-access-key'):
                aws_secret_access_key = value
            elif option in ('-n', '--dry-run'):
                logger.info("Performing a dry run (because of %s option) ..", option)
                dry_run = True
            elif option in ('-v', '--verbose'):
                coloredlogs.increase_verbosity()
            elif option in ('-h', '--help'):
                usage(__doc__)
                return
            else:
                assert False, "Unhandled option! (programming error)"
        if rotation_scheme:
            logger.debug("Parsed rotation scheme: %s", rotation_scheme)

        # If no arguments are given but the system has a configuration file
        # then the backups in the configured directories are rotated.
        if not arguments:
            arguments.extend(bucket for bucket, _, _ in load_config_file(config_file))
        # Show the usage message when no directories are given nor configured.
        if not arguments:
            usage(__doc__)
            return
    except Exception as e:
        logger.error("%s", e)
        sys.exit(1)
    # Rotate the backups in the given or configured directories.
    for bucket in arguments:
        S3RotateBackups(
            rotation_scheme=rotation_scheme,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            include_list=include_list,
            exclude_list=exclude_list,
            dry_run=dry_run,
        ).rotate_backups(bucket)

if __name__ == "__main__":
    main()