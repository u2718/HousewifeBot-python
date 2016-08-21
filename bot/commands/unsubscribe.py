from telegram.ext import ConversationHandler
from bot.commands.abstract_command import AbstractCommand
from data.database import Subscription, database


class UnsubscribeCommand(AbstractCommand):
    GET_TITLE = 1

    def _execute(self, db, user, bot, update, args):
        self.db = db
        self.user = user
        if not user.subscriptions:
            bot.send_message(chat_id=update.message.chat_id, text='Вы не подписаны ни на один сериал')
            return ConversationHandler.END

        if not args:
            bot.send_message(chat_id=update.message.chat_id, text='Введите название сериала')
            return UnsubscribeCommand.GET_TITLE
        show_title = ' '.join(args)
        self._unsubscribe(bot, update, show_title)
        return self.__handled()

    def get_title(self, bot, update):
        self._unsubscribe(bot, update, update.message.text)
        return self.__handled()

    def __handled(self):
        database.close(self.db)
        return ConversationHandler.END

    def _handled(self, db):
        pass

    def _unsubscribe(self, bot, update, title):
        show = database.get_show(self.db, title)
        if not show:
            bot.send_message(chat_id=update.message.chat_id, text='Сериал не найден')
            return

        subscription = [s.id for s in self.user.subscriptions if s.show_id == show.id]
        if not subscription:
            bot.send_message(chat_id=update.message.chat_id, text='Вы не подписаны на сериал "%s"' % show.title)
            return

        self.db.query(Subscription).filter(Subscription.id == subscription[0]).delete()
        bot.send_message(chat_id=update.message.chat_id, text='Вы отписались от сериала "%s"' % show.title)
