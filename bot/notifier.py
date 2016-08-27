import logging

from sqlalchemy.sql.elements import and_
from sqlalchemy import exists
from data import database
from data.database import User, Show, ShowNotification, Notification, Subscription, Episode

logger = logging.getLogger('logger')


class Notifier:
    def __init__(self, bot):
        self.bot = bot

    def create_shows_notifications(self):
        with database() as db:
            query = db.query(Show, User).filter(
                and_(
                    Show.created_date >= User.created_date,
                    ~exists().where(and_(ShowNotification.user_id == User.id, ShowNotification.show_id == Show.id))
                )
            )
            for row in query:
                notification = ShowNotification(user=row.User, show=row.Show, notified=False)
                db.add(notification)
                logger.info('Notification created (user: %s, show: %s )' % (row.User.telegram_user_id, row.Show.title))
        self._send_shows_notifications()

    def create_episodes_notifications(self):
        with database() as db:
            query = db.query(Subscription, User, Episode) \
                .join(Episode, Episode.show_id == Subscription.show_id) \
                .join(User, User.id == Subscription.user_id) \
                .filter(
                and_(
                    Episode.created_date >= Subscription.created_date,
                    ~exists().where(
                        and_(Notification.episode_id == Episode.id, Notification.user_id == Subscription.user_id))
                )
            )
            for row in query:
                notification = Notification(user=row.User, episode=row.Episode, notified=False)
                db.add(notification)
                logger.info(
                    'Notification created (user: %s, episode: %s )' % (row.User.telegram_user_id, row.Episode.title))
        self._send_episodes_notifications()

    def _send_shows_notifications(self):
        with database() as db:
            query = db.query(ShowNotification, User, Show) \
                .join(User, User.id == ShowNotification.user_id) \
                .join(Show, Show.id == ShowNotification.show_id) \
                .filter(~ShowNotification.notified)
            for notification in query:
                self.bot.send_message(
                    chat_id=notification.User.telegram_user_id,
                    text='Новый сериал: %s (%s)' % (notification.Show.title, notification.Show.original_title))
                notification.ShowNotification.notified = True

    def _send_episodes_notifications(self):
        with database() as db:
            query = db.query(Notification, User, Episode, Show)\
                .join(User, User.id == Notification.user_id) \
                .join(Episode, Episode.id == Notification.episode_id)\
                .join(Show, Show.id == Episode.show_id) \
                .filter(~Notification.notified)
            for notification in query:
                self.bot.send_message(
                    chat_id=notification.User.telegram_user_id,
                    text='%s: %s' % (notification.Show.title, notification.Episode.title)
                )
                notification.Notification.notified = True
