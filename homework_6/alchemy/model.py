from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author = Column(String(40))
    url = Column(String(100), unique=True)
    topic = Column(String, unique=True)
    article_text = Column(Text)
    price = Column(String, nullable=True)
    currency = Column(String(10))


if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:2367@localhost:5432/postgres')
    Base.metadata.create_all(engine)
