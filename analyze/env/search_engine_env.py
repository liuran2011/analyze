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

    def user_info_file(self):
        return SEARCH_ENGINE_USER_INFO

    def lib_dir(self):
        return SEARCH_ENGINE_LIB_DIR

    def uuid_file(self):
        return SEARCH_ENGINE_UUID_FILE

    @staticmethod
    def check():
        Env.check()

        if not os.path.exists(SEARCH_ENGINE_LOG_DIR):
            os.makedirs(SEARCH_ENGINE_LOG_DIR)

        if not os.path.exists(SEARCH_ENGINE_RUN_DIR):
            os.makedirs(SEARCH_ENGINE_RUN_DIR)

        if not os.path.exists(SEARCH_ENGINE_LOCK):
            os.mknod(SEARCH_ENGINE_LOCK)

        if not os.path.exists(SEARCH_ENGINE_USER_INFO):
            os.mknod(SEARCH_ENGINE_USER_INFO)

        if not os.path.exists(SEARCH_ENGINE_LIB_DIR):
            os.makedirs(SEARCH_ENGINE_LIB_DIR)
