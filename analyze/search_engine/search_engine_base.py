import urllib
from user_info_mgr import UserInfoMgr
import copy

class SearchEngineBase(object):
    def __init__(self,conf,env):
        self.conf=conf
        self.max_page=100
        self.env=env
        self.user_info_mgr=UserInfoMgr(env)
        self.user_list=[]

    def user_list_reload(self):
        self.user_info_mgr.lock()
        self.user_list=copy.deepcopy(self.user_info_mgr.user_info())
        self.user_info_mgr.unlock()

    def fetch_page(self,url):
        page=None
        try:
            fd=urllib.urlopen(url)
            page=fd.read()
            fd.close()
            return page
        except IOError as e:
            print "open url:%s failed."%(url)
            return page

