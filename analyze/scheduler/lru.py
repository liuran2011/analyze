from basic_filter import BasicFilter
from analyze.search_engine_mgr import SearchEngineMgr as sem

class Filter(BasicFilter):
    def __init__(self):
        super(Filter,self).__init__()

    def select(self,search_engine_stats):
        user_num=0
        target_key=None
        for key,value in search_engine_stats.iteritems():
            if not value.get(sem.SE_USER_LIST,None):
                target_key=key
                break
            
            if len(value[sem.SE_USER_LIST])<=user_num:
                user_num=len(value[sem.SE_USER_LIST])
                target_key=key

        return target_key
