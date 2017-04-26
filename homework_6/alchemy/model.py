from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author = Column(String(40), unique=True)


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    url = Column(String(100), unique=True)
    topic = Column(String)
    article_text = Column(Text)
    price = Column(String, nullable=True)
    currency = Column(String(10))

    author = relationship("Authors", backref="posts")


if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:2367@localhost:5432/postgres')
    Base.metadata.create_all(engine)
