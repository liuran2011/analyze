#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gevent
from conf.search_engine_conf import SearchEngineConf
from conf.analyze_conf import AnalyzeConf
import importlib
from log.log import LOG
from db.se_db import SearchEngineDB
from env import constants as env_cons

class SearchEngineLoader(object):
    def __init__(self,env,conf_file):
        self.env=env

        self._log_init(conf_file.split('.')[0])

        self.conf=SearchEngineConf('/'.join([self.env.conf_dir(),conf_file]))

        LOG.set_log_level(self.conf.log_level())

        self.analyze_conf=AnalyzeConf('/'.join([self.env.basic_conf_dir(),env_cons.ANALYZE_CONF_FILE]))
        self.db=SearchEngineDB(self.analyze_conf)

        module_name="search_engine.%s"%(self.conf.engine_name())
        m=importlib.import_module(module_name)
        self.engine=m.SearchEngine(self.conf,self.env,self.db)

    def _log_init(self,id):
        LOG.set_log_id(id)
        LOG.set_log_level('info')
        
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def start(self):
        gevent.spawn(self.engine.start())
        gevent.wait()

