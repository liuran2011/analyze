import gevent
import pickle
import os
import time
from utils import FileLock

class UserInfoMgr(object):
    USER_INFO_UPDATE_INTERVAL=5

    def __init__(self,env):
        self.env=env
        self._user_info=[]
        self._update_task=gevent.spawn(self._update)
        self.file_lock=FileLock(self.env.lock_file())

    def user_info(self):
        return self._user_info

    def _update(self):
        while True:
            try:
                self.file_lock.lock()
                f=open(self.env.user_info_file())
                s=f.read()
                if len(s)!=0:
                    self._user_info=pickle.loads(s)
                f.close()
                self.file_lock.unlock()
            except IOError:
                os.mknod(self.env.lock_file())

            time.sleep(UserInfoMgr.USER_INFO_UPDATE_INTERVAL)
