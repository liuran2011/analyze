#coding=utf-8

from analyze.notify.basic import BasicNotify
from analyze.log.log import LOG
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Notify(BasicNotify):
    def __init__(self,db):
        super(Notify,self).__init__(db)

    def _build_msg(self,report,sendto,sendfrom,report_format):
        try:
            f=open(report,'rb')
        except IOError as e:
            LOG.error("open report %s failed. except:%s"%(report,e))
            return None

        msg=MIMEMultipart()
        attach=MIMEText(f.read(),'base64','utf-8')
        attach['Content-Type']='application/octet-stream'
        attach['Content-Disposition']='attachment; filename="报告.%s"'%(report_format)
        msg.attach(attach)
        
        msg['to']=sendto
        msg['from']=sendfrom
        msg['subject']='报告'

        return msg

    def send(self,report,report_format,sendto):
        setting=self.db.global_setting()
        if not setting:
            LOG.error('email not set')
            return False
       
        msg=self._build_msg(report,sendto,setting.email,report_format)
        if not msg:
            return False

        try:
            smtp=smtplib.SMTP()    
            smtp.connect(setting.smtp_server,setting.smtp_port)
            smtp.login(setting.smtp_username,setting.smtp_password)
            smtp.sendmail(setting.email,sendto,msg.as_string())
            smtp.close()

            return True

        except Exception as e:
            LOG.error("send mail to %s failed. exception: %s"%(sendto,e))
            return False
