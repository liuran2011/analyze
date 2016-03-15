import time

class BasicGenerator(object):
    def __init__(self,conf,env,db):
        self.conf=conf
        self.db=db
        self.env=env

    def _run_user(self,userid,username):
        result_list=self.db.result_list(userid)
        if not result_list or len(result_list)==0:
            return

        self.ready(username)
        for result in result_list:
            self.add(result)
        self.finish(username)
        self.db.reset_last_time(userid)

    def run(self):
        while True:
            for user in self.db.user_list():
                self._run_user(user[0],user[1])

            time.sleep(int(self.conf.interval()))
