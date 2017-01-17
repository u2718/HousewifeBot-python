from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.sql.elements import or_

from utils.config import Config

Base = declarative_base()


class Show(Base):
    __tablename__ = 'show'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    original_title = Column(String)
    created_date = Column(DateTime, nullable=False, default=func.now())
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
    created_date = Column(DateTime, nullable=False, default=func.now())
    notifications = relationship('Notification', backref=backref('episode'))
    file_id = Column(String)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    created_date = Column(DateTime, nullable=False, default=func.now())
    subscriptions = relationship('Subscription', backref=backref('user'))
    show_notifications = relationship('ShowNotification', backref=backref('user'))
    notifications = relationship('Notification', backref=backref('user'))
    download_torrents = Column(Boolean)


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    created_date = Column(DateTime, nullable=False, default=func.now())


class ShowNotification(Base):
    __tablename__ = 'show_notification'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    show_id = Column(Integer, ForeignKey('show.id'), nullable=False)
    notified = Column(Boolean, nullable=False, default=False)


class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    episode_id = Column(Integer, ForeignKey('episode.id'), nullable=False)
    notified = Column(Boolean, nullable=False, default=False)


class database:
    def __init__(self):
        self._session, _ = self._create_session()

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        database.close(self._session)

    def get(self):
        return self._session

    def close(self):
        database.close(self._session)

    @staticmethod
    def close(session):
        session.commit()
        session.expire_all()

    @classmethod
    def get_show(cls, db, title):
        return db.query(Show).filter(
            or_(func.lower(Show.title) == func.lower(title), func.lower(Show.original_title) == func.lower(title))
        ).first()

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
