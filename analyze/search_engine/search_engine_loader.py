#!/usr/bin/env python

import gevent
from conf.search_engine_conf import SearchEngineConf
import importlib

class SearchEngineLoader(object):
    def __init__(self,env,conf_file):
        self.env=env
        self.conf=SearchEngineConf('/'.join([self.env.conf_dir(),conf_file]))
        
        module_name="search_engine.%s"%(self.conf.engine_name())
        m=importlib.import_module(module_name)
        self.engine=m.SearchEngine(self.conf,self.env)

    def start(self):
        gevent.spawn(self.engine.start())
        gevent.wait()

