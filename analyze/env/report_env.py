from constants import *
from env import Env
import os

class ReportEnv(Env):
    def log_dir(self):
        return LOG_DIR;
    
    def conf_dir(self):
        return self.basic_conf_dir()

    def conf_file(self):
        return REPORT_CONF_FILE

    def run_dir(self):
        return REPORT_RUN_DIR

    def share_dir(self):
        return SHARE_DIR

    @staticmethod
    def check():
        Env.check()
        
        if not os.path.exists(REPORT_RUN_DIR):
            os.makedirs(REPORT_RUN_DIR)
