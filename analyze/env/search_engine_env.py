from env import Env
from constants import *
import os

class SearchEngineEnv(Env):
    def log_dir(self):
        return SEARCH_ENGINE_LOG_DIR

    def run_dir(self):
        return SEARCH_ENGINE_RUN_DIR

    def conf_dir(self):
        return SEARCH_ENGINE_CONF_DIR

    def lock_file(self):
        return SEARCH_ENGINE_LOCK

    @staticmethod
    def check():
        Env.check()

        if not os.path.exists(SEARCH_ENGINE_LOG_DIR):
            os.makedirs(SEARCH_ENGINE_LOG_DIR)

        if not os.path.exists(SEARCH_ENGINE_RUN_DIR):
            os.makedirs(SEARCH_ENGINE_RUN_DIR)

        if not os.path.exists(SEARCH_ENGINE_LOCK):
            os.mknod(SEARCH_ENGINE_LOCK)
