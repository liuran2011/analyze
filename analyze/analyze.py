#! /usr/bin/env python

import gevent.monkey
gevent.monkey.patch_all()

from env.env import Env
from conf.analyze_conf import AnalyzeConf
from log.log import LOG
from mq.mq_analyze import AnalyzeMQ
from analyze.search_engine_mgr import SearchEngineMgr

class Analyze(object):
    def __init__(self):
        self._env_init()
        self._log_init()
        self._conf_init()
        self.se_mgr=SearchEngineMgr(self.conf)
        self._rabbitmq_init()

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
        self.analyze_mq.run()

if __name__=="__main__":
    Analyze().main()
