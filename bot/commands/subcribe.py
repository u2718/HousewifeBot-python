from telegram.ext import ConversationHandler
from bot.commands.abstract_command import AbstractCommand
from data.database import Subscription, database


class SubscribeCommand(AbstractCommand):
    GET_TITLE = 1

    def _execute(self, db, user, bot, update, args):
        self.db = db
        self.user = user
        if not args:
            bot.send_message(chat_id=update.message.chat_id, text='Введите название сериала')
            return SubscribeCommand.GET_TITLE
        show_title = ' '.join(args)
        self._subscribe(bot, update, show_title)
        return self.__handled()

    def get_title(self, bot, update):
        self._subscribe(bot, update, update.message.text)
        return self.__handled()

    def __handled(self):
        database.close(self.db)
        return ConversationHandler.END

    def _handled(self, db):
        pass

    def _subscribe(self, bot, update, title):
        show = database.get_show(self.db, title)
        if not show:
            bot.send_message(chat_id=update.message.chat_id, text='Сериал не найден')
            return

        if show.id in [show.show_id for show in self.user.subscriptions]:
            bot.send_message(chat_id=update.message.chat_id, text='Вы уже подписаны на сериал "%s"' % show.title)
            return

        subscription = Subscription(user=self.user, show=show)
        self.db.add(subscription)
        bot.send_message(chat_id=update.message.chat_id, text='Вы подписались на сериал "%s"' % show.title)
