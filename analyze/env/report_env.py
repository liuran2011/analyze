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

    @staticmethod
    def check():
        Env.check()

