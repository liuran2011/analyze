#!/usr/bin/env python

import gevent.monkey
gevent.monkey.patch_all()

from log.log import LOG
from conf.report_conf import ReportConf
from env.report_env import ReportEnv

class ReportGenerator(object):
    def __init__(self):
        self._env_init()
        self._conf_init()
        self._log_init()

    def _log_init(self):
        id='report'
        LOG.set_log_id(id)
        LOG.set_log_level(self.conf.log_level())
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def _conf_init(self):
        conf_file="/".join([self.env.conf_dir(),self.env.conf_file()])
        self.conf=ReportConf(conf_file)
        
    def _env_init(self):
        self.env=ReportEnv()
        self.env.check()

    def main(self):
        LOG.debug("report gen running....")

if __name__=="__main__":
    ReportGenerator().main()
