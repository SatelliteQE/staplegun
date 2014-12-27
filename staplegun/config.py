"""Reads configuration file for StapleGun."""

from ConfigParser import SafeConfigParser

import logging
import os


class Configs(object):
    """Read configuration file."""
    def __init__(self):
        """Read Robottelo's config file and initialize the logger."""
        # Set instance vars.
        self.properties = {}
        self.logger = logging.getLogger('staplegun')

        # Read the config file, if available.
        conf_parser = SafeConfigParser()
        if conf_parser.read(_config_file()):
            for section in conf_parser.sections():
                for option in conf_parser.options(section):
                    self.properties[
                        "{0}".format(option)
                    ] = conf_parser.get(section, option)
        else:
            self.logger.error(
                'No config file found at "{0}".'.format(_config_file())
            )


def get_app_root():
    """Return the path to the application root directory.

    :return: A directory path.
    :rtype: str

    """
    return os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))


def _config_file():
    """Return the path to the application-wide config file.

    :return: A file path.
    :rtype: str

    """
    return os.path.join(get_app_root(), 'settings.ini')


conf = Configs()
