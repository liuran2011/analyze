#!/usr/bin/env python

import gevent
from conf.search_engine_conf import SearchEngineConf
import importlib
from log.log import LOG

class SearchEngineLoader(object):
    def __init__(self,env,conf_file):
        self.env=env

        self._log_init(conf_file.split('.')[0])

        self.conf=SearchEngineConf('/'.join([self.env.conf_dir(),conf_file]))

        LOG.set_log_level(self.conf.log_level())

        module_name="search_engine.%s"%(self.conf.engine_name())
        m=importlib.import_module(module_name)
        self.engine=m.SearchEngine(self.conf,self.env)

    def _log_init(self,id):
        LOG.set_log_id(id)
        LOG.set_log_level('info')
        
        log_file=self.env.log_dir()+"/"+id+".log"
        LOG.set_log_file(log_file)

    def start(self):
        gevent.spawn(self.engine.start())
        gevent.wait()

