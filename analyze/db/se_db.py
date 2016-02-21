from modules import *
from sqlalchemy.engine import Connection
from sqlalchemy.orm import sessionmaker

class SearchEngineDB(object):
    def __init__(self,conf):
        self.conf=conf

        self.engine=create_engine(self.conf.db_connection())
        self.session=sessionmaker(bind=self.engine)()

        Base.metadata.bind=self.engine
        Base.metadata.create_all()

