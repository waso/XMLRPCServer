from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import SocketServer
import string
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): pass

Base = declarative_base()
engine = create_engine('mysql+mysqldb://root:@localhost:5000/spike', echo=True)
Session = scoped_session(sessionmaker(bind=engine))

server = AsyncXMLRPCServer(('', 8000), SimpleXMLRPCRequestHandler)

class xmlrpc_registers:
    def __init__(self):
        self.python_string = string
    
    def echo (self,text):
        return text + " !!!"
    
    def total_news(self):
        session = Session()
        cnt = session.query(News.id).count()
        session.commit()
        session.close()
        return 'Total number of news: ' + str(cnt)
    
    def total_news_by_text(self, text_to_find):
        session = Session()
        count = 0
        count = session.query(News).join(Author, Author.id==News.author_id).filter(News.text.like('%' + text_to_find + '%')).count()
        session.commit()
        session.close()
        return count
    
    def print_news_by_text(self, text_to_find):
        session = Session()
        count = 0
        res = ''
        for n, a in session.query(News, Author).filter(News.author_id == Author.id).filter(News.text.like('%' + text_to_find + '%')).all():
            count = count + 1
            res = res + str(n.id) + ', title: ' + n.title + ' author: ' + a.name + ' ' + a.email + '\n'
        session.commit()
        session.close()
        return res
    
    def add_news(self, title, author_id, text):
        session = Session()
        newNews = News(title, author_id, text)
        session.add(newNews)
        session.commit()
        newid = newNews.id
        session.close()
        return newid
    
    def add_author(self, name, email):
        session = Session()
        newAuthor = Author(name, email)
        session.add(newAuthor)
        session.commit()
        newid = newAuthor.id
        session.close()
        return newid

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author_id = Column(Integer)
    text = Column(String(65535))
    def __init__(self, title, author_id, text):
        self.title = title
        self.author_id = author_id
        self.text = text
    def __repr__(self):
        return "<News('%s','%s', '%s')>" % (self.title, self.author_id, self.text)
    
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def __repr__(self):
        return "<Author('%s', '%s')>" % (self.name, self.email)
    
server.register_instance(xmlrpc_registers())
server.serve_forever()