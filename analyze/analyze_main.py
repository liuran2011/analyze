#! /usr/bin/env python

#coding=utf-8

import gevent.monkey
gevent.monkey.patch_all()
import gevent

from env.env import Env
from conf.analyze_conf import AnalyzeConf
from log.log import LOG
from mq.mq_analyze import AnalyzeMQ
from analyze.search_engine_mgr import SearchEngineMgr
from db.analyze_db import AnalyzeDB
from analyze.rest_server import RestServer
from scheduler.scheduler import Scheduler

class Analyze(object):
    def __init__(self):
        self._env_init()
        self._log_init()
        self._conf_init()
        self._db_init()
        self.se_mgr=SearchEngineMgr(self.conf,self.db)
        self._rabbitmq_init()
        self.scheduler=Scheduler(self.conf,self.se_mgr,self.db)
        self.se_mgr.set_scheduler(self.scheduler)
        self.se_mgr.set_mq(self.analyze_mq)
        self.rest_server=RestServer(self.conf,self.db,self.analyze_mq,self.se_mgr,self.scheduler)
        self.analyze_mq.set_rest_server(self.rest_server)

    def _db_init(self):
        self.db=AnalyzeDB(self.conf)

    def _log_init(self):
        id="analyze"
        LOG.set_log_id(id)
        LOG.set_log_level('info')
       
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def _env_init(self):
        self.env=Env()
        self.env.check() 

    def _conf_init(self):
        conf_file="/".join([self.env.basic_conf_dir(),self.env.basic_conf_file()])
        self.conf=AnalyzeConf(conf_file)

        LOG.set_log_level(self.conf.log_level())

    def _rabbitmq_init(self):
        self.analyze_mq=AnalyzeMQ(self.conf,self.se_mgr)
        self.se_mgr.register_notifier(self.analyze_mq.del_queue)

    def main(self):
        mq_task=gevent.spawn(self.analyze_mq.run)
        rest_task=gevent.spawn(self.rest_server.run)

        gevent.wait([mq_task,rest_task])

def analyze_main():
    Analyze().main()
    
if __name__=="__main__":
    analyze_main()
