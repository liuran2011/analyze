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
        last_time=self.session.query(User.last_report_time).filter_by(id=user_id).first()
        if last_time:
            last_time=last_time[0]

        now_time=datetime.datetime.now()
        if not last_time:
            results=self.session.query(Result.url,Result.source_url,Result.datetime,
                        Result.keyword).filter(Result.user_id==user_id).filter(Result.datetime<=now_time).all()
        else:
            results=self.session.query(Result.url,Result.source_url,Result.datetime,
                        Result.keyword).filter(Result.user_id==user_id).filter(
                        Result.datetime<=now_time).filter(Result.datetime>last_time).all()

        return results

    def reset_last_time(self,userid):
        pass
