from models import *
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from log.log import LOG
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
