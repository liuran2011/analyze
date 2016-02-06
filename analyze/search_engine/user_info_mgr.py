import gevent
import fcntl
import pickle
import os
import time
import threading

class UserInfoMgr(object):
    USER_INFO_UPDATE_INTERVAL=5

    def __init__(self,env):
        self.env=env
        self._user_info=[]
        self._update_task=gevent.spawn(self._update)
        self._lock=threading.Lock()

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def user_info(self):
        return self._user_info

    def _update(self):
        while True:
            try:
                f=open(self.env.lock_file())
                fcntl.flock(f.fileno(),fcntl.LOCK_EX)
                s=f.read()
                if len(s)!=0:
                    self.lock()
                    self._user_info=pickle.loads(s)
                    self.unlock()
                fcntl.flock(f.fileno(),fcntl.LOCK_UN)
                f.close()
            except IOError:
                os.mknod(self.env.lock_file())

            time.sleep(UserInfoMgr.USER_INFO_UPDATE_INTERVAL)
