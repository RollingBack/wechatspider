# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Date, Text

Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root:@127.0.0.1:3306/spider')

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True)
    signature = Column(String(100))
    date = Column(Date())
    author = Column(String(60))
    title = Column(String(300))
    content = Column(Text())
    readnum = Column(Integer())
    likenum = Column(Integer())
    keyword = Column(String(50))
    
    def __init__(self, signature, date, author, title, content, readnum, likenum, keyword):
        self.signature = signature
        self.date = date
        self.author = author
        self.title = title
        self.content = content
        self.keyword = keyword
    
    def __repr__(self):
        return "<Article(signature='%s', date='%s', author='%s', title='%s', content='%s', keyword='%s')>" % (self.signature, self.date, self.author, self.title, self.content, self.keyword)
    
    
if __name__ == "__main__":  
    Base.metadata.create_all(engine)    
