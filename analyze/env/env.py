import os
from constants import *

class Env(object):
    def basic_conf_dir(self):
        return CONF_DIR
    
    def basic_conf_file(self):
        return ANALYZE_CONF_FILE

    def log_dir(self):
        return LOG_DIR

    @staticmethod
    def check():
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        if not os.path.exists(RUN_DIR):
            os.makedirs(RUN_DIR)

        if not os.path.exists(CONF_DIR):
            os.makedirs(CONF_DIR)


