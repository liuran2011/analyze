import time

class BasicGenerator(object):
    def __init__(self,conf,db):
        self.conf=conf
        self.db=db

    def _run_user(self,userid):
        result_list=self.db.result_list(userid)
        if not result_list or len(result_list)==0:
            return

        self.ready("xxx")
        for result in result_list:
            self.add(result)
        self.finish("xxx")

    def run(self):
        while True:
            for user in self.db.user_list():
                self._run_user(user[0])

            time.sleep(int(self.conf.interval()))
