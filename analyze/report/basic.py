#coding=utf-8

import time

class BasicGenerator(object):
    def __init__(self,conf,env,db,notify):
        self.conf=conf
        self.db=db
        self.env=env
        self.notify=notify

    def _run_user(self,userid,username):
        result_list=self.db.result_list(userid)
        if not result_list or len(result_list)==0:
            return

        self.ready(username)
        for result in result_list:
            self.add(result)
        self.finish(username)

    def run_user(self,username,start_time,end_time):
        result_list=self.db.result_list_direct(username,start_time,end_time)
        if not result_list or len(result_list)==0:
            return

        self.ready(username)
        for result in result_list:
            self.add(result)
        self.finish(username)

    def run(self):
        while True:
            for user in self.db.user_list():
                self._run_user(user[0],user[1])

            time.sleep(int(self.conf.interval()))
