#! /usr/bin/env python

import os
import re
from env.env import Env
from conf.analyze_conf import AnalyzeConf

class AnalyzeDBSync(object):
    def __init__(self):
		self._env_init()
		self._conf_init()

    def _env_init(self):
        self.env=Env()

    def _conf_init(self):
        conf_file="/".join([self.env.basic_conf_dir(),self.env.basic_conf_file()])
        self.conf=AnalyzeConf(conf_file)

    def main(self):
        group=re.match("mysql://(.*):(.*)@.*/(.*)",
                    self.conf.db_connection())
        if len(group.groups())<3:
            print "invalid database connect:",self.conf.db_connection()
            return

        user=group.groups()[0]
        password=group.groups()[1]
        db=group.groups()[2]

        sql_cmd="create database %s;"%(db)
        sql_cmd+="grant all privileges on %s.* to '%s'@'localhost' identified by '%s';"%(db,user,password)
        sql_cmd+="grant all privileges on %s.* to '%s'@"%(db,user)
        sql_cmd+="'%' identified by "
        sql_cmd+="'%s';"%(password)
        
        os.system('mysql -u root -p -e "%s"'%(sql_cmd))

def main():
    AnalyzeDBSync().main()
    
if __name__=="__main__":
    main()
