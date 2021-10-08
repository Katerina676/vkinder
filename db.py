import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
engine = sq.create_engine('postgresql://postgres:postgres@localhost:5432/user_test1')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user_id'
    id = sq.Column(sq.Integer, primary_key=True)
    url_id = sq.Column(sq.String)


class Photos(Base):
    __tablename__ = 'photos_id'
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user_id.id'))
    photos_url = sq.Column(sq.String(1000))
    user = relationship(User)


def create_tables():
    Base.metadata.create_all(engine)
