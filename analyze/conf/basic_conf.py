import ConfigParser

from constants import *
from log.log import LOG

class BasicConf(object):
    def __init__(self,conf_file):
        self.conf_file=conf_file
        self.parser=ConfigParser.ConfigParser()
        try:
            self.parser.read(conf_file)
        except Exception as e:
            LOG.warn("parse config file %s failed."%(conf_file))
            raise

    def log_level(self):
        return self.parser.get(DEFAULT,LOG_LEVEL)

    
