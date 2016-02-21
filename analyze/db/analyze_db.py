from models import *
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker

class AnalyzeDB(object):
    def __init__(self,conf):
        self.conf=conf

        self.engine=create_engine(self.conf.db_connection())
        Session=sessionmaker(bind=self.engine)
        self.session=Session()

        Base.metadata.bind=self.engine
        Base.metadata.create_all()


