from models import *
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from analyze.log.log import LOG
import datetime

class ReportDB(object):
    def __init__(self,conf):
        self.conf=conf

        self.engine=create_engine(self.conf.db_connection())
        self.session=sessionmaker(bind=self.engine)()

        Base.metadata.bind=self.engine
        Base.metadata.create_all()

    def user_list(self):
        return self.session.query(User.id,User.name).all();

    def user_email(self,username):
        result=self.session.query(User.email).filter_by(name=username).first()
        if not result:
            LOG.error("user %s do not setting email"%(username))
            return None
        
        return result.email

    def global_setting(self):
        setting=self.session.query(GlobalSetting.email,GlobalSetting.smtp_server,
                            GlobalSetting.smtp_port,GlobalSetting.smtp_username,
                            GlobalSetting.smtp_password).first()
        if not setting:
            return None

        return setting
    
    def result_list_direct(self,username,start_time,end_time):
        user=self.session.query(User.id).filter_by(name=username).first()
        if not user:
            LOG.info('user %s not find'%(username))
            return []
        
        if not end_time:
            end_time=datetime.datetime.now()

        results=self.session.query(Result.url,Result.source_url,Result.datetime,
                            Result.keyword).filter(Result.user_id==user.id).filter(
                            Result.datetime>=start_time).filter(Result.datetime<end_time).all()
        
        return results

    def result_list(self,user_id):
        user=self.session.query(User).filter_by(id=user_id).first()
        if not user:
            return []

        last_time=None
        if user.last_report_time:
            last_time=user.last_report_time

        now_time=datetime.datetime.now()
        if not last_time:
            results=self.session.query(Result.url,Result.source_url,Result.datetime,
                        Result.keyword).filter(Result.user_id==user_id).filter(Result.datetime<=now_time).all()
        else:
            results=self.session.query(Result.url,Result.source_url,Result.datetime,
                        Result.keyword).filter(Result.user_id==user_id).filter(
                        Result.datetime<=now_time).filter(Result.datetime>last_time).all()

        user.last_report_time=now_time
        self.session.commit()

        return results
