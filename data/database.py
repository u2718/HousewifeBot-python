import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.config import Config

Base = declarative_base()


class Show(Base):
    __tablename__ = 'show'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    original_title = Column(String)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    episodes = relationship('Episode', backref=backref('show'))
    subscriptions = relationship('Subscription', backref=backref('show'))
    show_notifications = relationship('ShowNotification', backref=backref('show'))


class Episode(Base):
    __tablename__ = 'episode'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    season_number = Column(Integer)
    episode_number = Column(Integer)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    subscriptions = relationship('Subscription', backref=backref('user'))
    show_notifications = relationship('ShowNotification', backref=backref('user'))


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())


class ShowNotification(Base):
    __tablename__ = 'show_notification'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    notified = Column(Boolean, nullable=False, default=False)


class database:
    def __init__(self):
        self._session, _ = self._create_session()

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.commit()

    @classmethod
    def _create_session(cls):
        engine = create_engine(Config().connection_string)
        session = sessionmaker()
        session.configure(bind=engine)
        return session(), engine

    @classmethod
    def init_db(cls):
        _, engine = cls._create_session()
        Base.metadata.create_all(engine)
