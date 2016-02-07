import pickle
from utils import FileLock

class UserInfoExport(object):
    def __init__(self,env):
        self.env=env
        self.lock=FileLock(self.env.lock_file())

    def export(self,user_info):
        self.lock.lock()
        f=open(self.env.user_info_file(),"w")
        pickle.dump(user_info,f)
        f.close()
        self.lock.unlock()
