#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

from logging import getLogger
from logging.config import fileConfig
from os.path import dirname


def init():
    """
    Initializes the logging system with the logging.conf configuration file
    """

    # load the configuration relative to logutil.py

    mydir = dirname(__file__)
    if mydir == '':
        mydir = '.'

    config_file = '%s/logging.conf' % mydir

    fileConfig(config_file)


if __name__ == '__main__':
    init()
    getLogger('mylogclass').debug('this is debug from mylogclass')
    getLogger('boto').debug('this is debug from boto')