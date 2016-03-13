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
        return self.session.query(User.id).all();

    def result_list(self,user_id):
        last_time=self.session.query(User.last_report_time).filter_by(id=user_id).first()
        if not last_time:
            last_time=datetime.datetime.now()
        else:
            last_time=last_time[0]
            if not last_time:
                last_time=datetime.datetime.now()

        results=self.session.query(Result.url,Result.source_url,Result.datetime,
                    Result.keyword).filter(Result.user_id==user_id).filter(Result.datetime>last_time).all()

        return results
