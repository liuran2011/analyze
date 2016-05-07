#coding=utf-8

import os
import time
from analyze.log.log import LOG

class BasicGenerator(object):
    def __init__(self,conf,env,db,notify):
        self.conf=conf
        self.db=db
        self.env=env
        self.notify=notify

    def _gen_result(self,username,result_list):
        self.ready(username)
        for result in result_list:
            self.add(result)
        file_name=self.finish(username)
        
        user_email=self.db.user_email(username)
        if not user_email:
            LOG.error("username %s get email failed."%(username))
            os.unlink(file_name)
            return False

        if not self.notify.send(file_name,self.format(),user_email):
            LOG.error("username %s send email failed."%(username))
            os.unlink(file_name)
            return False 
       
        os.unlink(file_name)
        
        return True

    def _run_user(self,userid,username):
        result_list=self.db.result_list(userid)
        if not result_list or len(result_list)==0:
            return False

        return self._gen_result(username,result_list)

    def run_user(self,username,start_time,end_time):
        result_list=self.db.result_list_direct(username,start_time,end_time)
        if not result_list or len(result_list)==0:
            return False
        
        return self._gen_result(username,result_list)
       
    def run(self):
        while True:
            for user in self.db.user_list():
                self._run_user(user[0],user[1])

            time.sleep(int(self.conf.interval()))
