from notify.basic import BasicNotify
from log.log import LOG
import smtplib

class Notify(BasicNotify):
    def __init__(self,db):
        super(Notify,this).__init__(db)

    def send(self,report):
        setting=self.db.global_setting()
        if not setting:
            LOG.error('email not set')
            return

        smtp=smtplib.SMTP()    
        smtp
