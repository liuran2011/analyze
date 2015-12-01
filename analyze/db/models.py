from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,ForeignKey,String
from sqlalchemy.orm import relationship

from constants import *

Base=declarative_base()

class User(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True)
    name=Column(String(USER_NAME_LEN),nullable=False)
    email=Column(String(EMAIL_LEN))
    mobile_phone=Column(String(MOBILE_PHONE_LEN))
    permission=Column(String(PERMISSION_LEN))
    password=Column(String(PASSWORD_LEN),nullable=False)
    company=Column(String(COMPANY_LEN))
    monitor_keyword=Column(String(MONITOR_KEYWORD_LEN))

class Result(Base):
    __tablename__="result"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('user.id'))
    url=Column(String(URL_LEN),nullable=False)
    source_url=Column(String(URL_LEN))

    user=relationship(User)

class NegativeWord(Base):
    __tablename__="negative_word"

    word=Column(String(NEGATIVE_WORD_LEN),nullable=False)

