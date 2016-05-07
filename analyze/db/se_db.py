from models import *
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from analyze.log.log import LOG
import datetime

class SearchEngineDB(object):
    def __init__(self,conf):
        self.conf=conf

        self.engine=create_engine(self.conf.db_connection())
        self.session=sessionmaker(bind=self.engine)()

        Base.metadata.bind=self.engine
        Base.metadata.create_all()

    def add_result(self,user_name,url,source_url,keyword):
        user_id=self.session.query(User.id).filter_by(name=user_name).first()
        if not user_id:
            LOG.error("user_name: %s not found in db"%(user_name))
            return

        self.session.add(Result(user_id=user_id.id,url=url,
                            source_url=source_url,keyword=keyword,
                            datetime=datetime.datetime.now()))
        self.session.commit()

