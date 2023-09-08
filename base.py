#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

import os
from logging import getLogger

class Base:

    def __init__(self, filenames=[]):
        self.log = getLogger(self.__class__.__name__)

    def time_stamp(self):
        '''
        returns a utc timestamp in the format %Y%m%d_%H%M%S_UTC
        suitable for naming amis, keys, etc
        '''

        from time import strftime, gmtime
        return strftime('%Y%m%d_%H%M%S_UTC', gmtime())