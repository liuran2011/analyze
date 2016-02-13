#! /usr/bin/env python

from env.env import Env
from conf.analyze_conf import AnalyzeConf
from log.log import LOG

class Analyze(object):
    def __init__(self):
        self._env_init()
        self._log_init()
        self._conf_init()
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
        pass

    def main(self):
        pass

if __name__=="__main__":
    Analyze().main()
