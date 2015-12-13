#!/usr/bin/env python

from env import Env
from search_engine.search_engine_mgr import SearchEngineManager

class SearchEngine(object):
    def __init__(self):
        Env.check()
        self.engine_mgr=SearchEngineManager()

    def main(self):
        self.engine_mgr.run()

if __name__=="__main__":
    SearchEngine().main()

