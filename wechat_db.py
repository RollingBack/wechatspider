# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Date, Text, BLOB
from time import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:@127.0.0.1:3306/spider')

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    signature = Column(String(180), unique=True, nullable=False)
    timestamp = Column(Integer, nullable=False)
    src = Column(SmallInteger, nullable=False)
    ver = Column(SmallInteger, nullable=False)
    date = Column(Date, nullable=False)
    author = Column(BLOB(60), nullable=False)
    title = Column(BLOB(300), nullable=False)
    content = Column(BLOB(), nullable=False)
    readnum = Column(Integer, nullable=False, server_default='0')
    likenum = Column(Integer, nullable=False, server_default='0')
    keyword = Column(String(50), nullable=False)
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer, nullable=False)
    
    def __init__(self, signature, timestamp, src, ver, date, author, title, content, keyword):
        self.signature = signature
        self.timestamp = timestamp
        self.src = src
        self.ver = ver
        self.date = date
        self.author = author
        self.title = title
        self.content = content
        self.keyword = keyword
        self.readnum = 0
        self.likenum = 0
        self.created_at = int(time())
        self.updated_at = self.created_at
    
    def __repr__(self):
        return "<Article(signature='%s', date='%s', author='%s', title='%s', content='%s', keyword='%s')>" % (self.signature, self.date, self.author, self.title, self.content, self.keyword)
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }    
    
if __name__ == "__main__":  
    Base.metadata.create_all(engine)    
