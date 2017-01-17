import logging
from operator import attrgetter
from telegram.chataction import ChatAction
from sqlalchemy.sql.elements import and_
from sqlalchemy import exists
from data import database
from data.database import User, Show, ShowNotification, Notification, Subscription, Episode
from downloaders.lostfilm import Lostfilm

logger = logging.getLogger('logger')


class Notifier:
    def __init__(self, bot):
        self.bot = bot
        self.torrent_downloader = Lostfilm()

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
                chat_id = notification.User.telegram_user_id
                try:
                    self.bot.send_message(
                        chat_id=chat_id,
                        text='Новый сериал: %s (%s)' % (notification.Show.title, notification.Show.original_title))
                    notification.ShowNotification.notified = True
                except Exception as e:
                    logger.error('An error has occurred while sending notification to %s: %s' % (chat_id, str(e)))

    def _send_episodes_notifications(self):
        with database() as db:
            query = db.query(Notification, User, Episode, Show)\
                .join(User, User.id == Notification.user_id) \
                .join(Episode, Episode.id == Notification.episode_id)\
                .join(Show, Show.id == Episode.show_id) \
                .filter(~Notification.notified)
            for notification in query:
                chat_id = notification.User.telegram_user_id
                try:
                    self.bot.send_message(
                        chat_id=chat_id,
                        text='%s: %s' % (notification.Show.title, notification.Episode.title)
                    )
                    notification.Notification.notified = True
                    if notification.User.download_torrents:
                        self.__send_torrent(chat_id, notification)
                except Exception as e:
                    logger.error('An error has occurred while sending notification to %s: %s' % (chat_id, str(e)))

    def __send_torrent(self, chat_id, notification):
        if notification.Episode.file_id is None:
            torrents = self.torrent_downloader.list(notification.Show.site_id, notification.Episode.season_number,
                                                    notification.Episode.episode_number)
            torrent = max(torrents, key=attrgetter('size'))
            path = torrent.download()
            document = open(path, 'rb')
            file_id = self.__send_document(chat_id, document)
            notification.Episode.file_id = file_id
        else:
            self.__send_document(chat_id, notification.Episode.file_id)

    def __send_document(self, chat_id, document):
        self.bot.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
        msg = self.bot.send_document(chat_id, document)
        return msg.document.file_id
