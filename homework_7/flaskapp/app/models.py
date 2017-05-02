from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

db = SQLAlchemy()


def lower(field):
    return func.lower(field)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.Text)
    pw_hash = db.Column(db.Text)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __str__(self):
        return '<User %s>' % self.username


class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40), unique=True)

    def __init__(self, author):
        self.author = author

    def __str__(self):
        return '<Author %s>' % self.author


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    url = db.Column(db.String(100), unique=True)
    topic = db.Column(db.String)
    article_text = db.Column(db.String)
    price = db.Column(db.String, nullable=True)
    currency = db.Column(db.String(10))

    author = db.relationship("Authors", backref="posts")

    def __str__(self):
        return '<%s by %s>' % (self.topic, self.author)


if __name__ == '__main__':
    engine = db.create_engine('postgresql://postgres:2367@localhost:5432/postgres')
    db.Model.metadata.create_all(engine)
