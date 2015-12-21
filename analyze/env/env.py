import os
from constants import *

class Env(object):
    @staticmethod
    def check():
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        if not os.path.exists(RUN_DIR):
            os.makedirs(RUN_DIR)

        if not os.path.exists(CONF_DIR):
            os.makedirs(CONF_DIR)


