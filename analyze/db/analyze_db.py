from models import *
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker
from log.log import LOG

class AnalyzeDB(object):
    def __init__(self,conf):
        self.conf=conf

        self.engine=create_engine(self.conf.db_connection())
        Session=sessionmaker(bind=self.engine)
        self.session=Session()

        Base.metadata.bind=self.engine
        Base.metadata.create_all()

    def global_setting_update(self,email,smtp_server,smtp_port,smtp_username,
                        smtp_password):
        glb=self.session.query(GlobalSetting).first()
        if glb:
            glb.email=email
            glb.smtp_server=smtp_server
            glb.smtp_port=smtp_port
            glb.smtp_username=smtp_username
            glb.smtp_password=smtp_password
        else:
            glb=GlobalSetting(email=email,smtp_server=smtp_server,smtp_port=smtp_port,
                                smtp_username=smtp_username,smtp_password=smtp_password)
            self.session.add(glb)

        self.session.commit()

    def global_setting(self):
        return self.session.query(GlobalSetting.email,
                                GlobalSetting.smtp_server,
                                GlobalSetting.smtp_port,
                                GlobalSetting.smtp_username,
                                GlobalSetting.smtp_password).first()

    def user_list(self):
        return self.session.query(User.name,User.email,User.mobile_phone,
                            User.permission,User.company,User.monitor_keyword,
                            User.last_report_time).all()

    def user_update(self,username,password,email,mobile_phone,permission,company,monitor_keyword):
        user=self.session.query(User).filter_by(name=username).first()
        if not user:
            LOG.error("user %s not exist"%(username))
            return False

        user.password=password
        user.email=email
        user.mobile_phone=mobile_phone
        user.permission=permission
        user.company=company
        user.monitor_keyword=monitor_keyword
        self.session.commit()
        
        return True

    def user_add(self,username,password,email,
                mobile_phone,permission,company,monitor_keyword):
        user_id=self.session.query(User.id).filter_by(name=username).first()
        if user_id:
            LOG.error("user %s already exist."%(username))
            return False

        self.session.add(User(name=username,password=password,email=email,mobile_phone=mobile_phone,
                            permission=permission,company=company,
                            monitor_keyword=monitor_keyword))
        self.session.commit()

        return True

    def user_del(self,username):
        self.session.query(User).filter(User.name==username).delete()
        self.session.commit()

