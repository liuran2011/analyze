#! /usr/bin/env python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gevent.monkey
gevent.monkey.patch_all()

import os
import multiprocessing
from env.search_engine_env import SearchEngineEnv
from search_engine.search_engine_loader import SearchEngineLoader
from search_engine.user_info_export import UserInfoExport
from log.log import LOG
from conf.analyze_conf import AnalyzeConf
from mq.mq_se import SearchEngineMQ
from search_engine.stats import Stats
import time

class SearchEngineMonitor(object):
    def __init__(self):
        self._env_init()
        self._log_init()
        self._conf_init()
        self._engine_fork()
        self._user_info_init()
        self._rabbitmq_init()
        self._stats_init()

    def _stats_update(self):
        while True:
            self.rabbitmq.publish_stats(self.stats.get())
            time.sleep(Stats.STATS_UPDATE_INTERVAL)

    def _stats_init(self):
        self.stats=Stats()
        
        for f in os.listdir(self.env.conf_dir()):
            self.stats.add_engine(f.strip(".conf"))

        self.stats_task=gevent.spawn(self._stats_update)

    def _rabbitmq_init(self):
        self.rabbitmq=SearchEngineMQ(self.analyze_conf,
                                    self.env,
                                    self.user_info_export)

    def _conf_init(self):
        conf_file="/".join([self.env.basic_conf_dir(),self.env.basic_conf_file()])
        self.analyze_conf=AnalyzeConf(conf_file)

    def _env_init(self):
        self.env=SearchEngineEnv()
        self.env.check()

    def _user_info_init(self):
        self.user_info_export=UserInfoExport(self.env)
        self.user_info_export.export([])

    def _log_init(self):
        id='search_engine_monitor'
        LOG.set_log_id(id)
        LOG.set_log_level('info')
        
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def _load_engine(self,conf_file):
        LOG.info("loading search engine %s..."%(conf_file))

        loader=SearchEngineLoader(self.env,conf_file)
        loader.start()

    def _engine_fork(self):
        self.engine_process=[]
        for f in os.listdir(self.env.conf_dir()):
            p=multiprocessing.Process(target=self._load_engine,args=(f,))
            p.start()
            self.engine_process.append(p)

    def main(self):
        self.rabbitmq.run()

        for p in self.engine_process:
            p.join()

def main():
    SearchEngineMonitor().main()
    
if __name__=="__main__":
    main()
