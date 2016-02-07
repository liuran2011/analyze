#! /usr/bin/env python
#coding=utf-8

import gevent.monkey
gevent.monkey.patch_all()

import os
import multiprocessing
from env.search_engine_env import SearchEngineEnv
from search_engine.search_engine_loader import SearchEngineLoader
from search_engine.user_info_export import UserInfoExport
from log.log import LOG

class SearchEngineMonitor(object):
    def __init__(self):
        self.env=SearchEngineEnv()
        self.env.check()

        self.engine_process=[]

        self.user_info=[]
        self.user_info_export=UserInfoExport(self.env)
       
        self.user_info_export.export(self.user_info)

    def _load_engine(self,conf_file):
        print "loading search engine %s..."%(conf_file)

        loader=SearchEngineLoader(self.env,conf_file)
        loader.start()

    def main(self):
        for f in os.listdir(self.env.conf_dir()):
            p=multiprocessing.Process(target=self._load_engine,args=(f,))
            p.start()
            self.engine_process.append(p)
        
        for p in self.engine_process:
            p.join()

if __name__=="__main__":
    SearchEngineMonitor().main()
