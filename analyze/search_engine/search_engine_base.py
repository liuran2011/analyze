import urllib
from user_info_mgr import UserInfoMgr
import copy
import time
from log.log import LOG
import importlib

class NotImplementException(Exception):
    """Function method not implement exception."""

class SearchEngineBase(object):
    USER_LIST_EMPTY_RESCHED_INTERVAL=5

    def __init__(self,conf,env,db):
        self.conf=conf
        self.max_page=100
        self.env=env
        self.db=db
        self.user_info_mgr=UserInfoMgr(env)
        self.user_list=[]
        self._algorithm_init()

    def _algorithm_init(self):
        module_name="algorithm.%s"%(self.conf.algorithm())
        self.algorithm=importlib.import_module(module_name)

    def user_list_reload(self):
        self.user_list=copy.deepcopy(self.user_info_mgr.user_info())

    def fetch_page(self,url):
        page=None
        try:
            fd=urllib.urlopen(url)
            page=fd.read()
            fd.close()
            return page
        except IOError as e:
            LOG.warn("open url:%s failed."%(url))
            return page

    def search_user(self,user):
        raise NotImplementException("search_user not implement")

    def start(self):
        LOG.info("search engine running...")

        while True:
            self.user_list_reload()

            if len(self.user_list)==0:
                time.sleep(SearchEngineBase.USER_LIST_EMPTY_RESCHED_INTERVAL)
                continue

            for user in self.user_list:
                self.search_user(user)

                time.sleep(self.conf.search_interval())

            time.sleep(self.conf.search_interval())
