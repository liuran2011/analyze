#!/usr/bin/env python

import gevent.monkey
gevent.monkey.patch_all()

from log.log import LOG
from conf.report_conf import ReportConf
from conf.analyze_conf import AnalyzeConf
from env.report_env import ReportEnv
from db.report_db import ReportDB
import importlib

class ReportGenerator(object):
    def __init__(self):
        self._env_init()
        self._conf_init()
        self._log_init()
        self._db_init()

    def _db_init(self):
        self.db=ReportDB(self.basic_conf)

    def _log_init(self):
        id='report'
        LOG.set_log_id(id)
        LOG.set_log_level(self.conf.log_level())
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def _conf_init(self):
        conf_file="/".join([self.env.conf_dir(),self.env.conf_file()])
        self.conf=ReportConf(conf_file)
        
        conf_file="/".join([self.env.conf_dir(),self.env.basic_conf_file()])
        self.basic_conf=AnalyzeConf(conf_file)

    def _env_init(self):
        self.env=ReportEnv()
        self.env.check()

    def main(self):
        module=importlib.import_module("report.%s"%(self.conf.format()))
        self.engine=module.Generator(self.conf,self.env,self.db)
        self.engine.run()

if __name__=="__main__":
    ReportGenerator().main()
