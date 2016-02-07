import fcntl

class FileLock(object):
    def __init__(self,lock_file):
        self.lock_file=lock_file
        self.file=open(self.lock_file)
        
    def lock(self):
        fcntl.flock(self.file.fileno(),fcntl.LOCK_EX)

    def unlock(self): 
        fcntl.flock(self.file.fileno(),fcntl.LOCK_UN)

