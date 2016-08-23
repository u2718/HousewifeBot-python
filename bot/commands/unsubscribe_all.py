from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.commands.abstract_command import AbstractCommand
from data import database
from data.database import Subscription


class UnsubscribeAllCommand(AbstractCommand):
    def _execute(self, db, user, bot, update, args):
        self.db = db
        self.user = user
        if not user.subscriptions:
            bot.send_message(chat_id=update.message.chat_id, text='Вы не подписаны ни на один сериал')
            return

        keyboard = [[InlineKeyboardButton("Да", callback_data='yes'), InlineKeyboardButton("Нет", callback_data='no')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(update.message.chat_id, text="Вы действительно хотите отписаться от всех сериалов?",
                        reply_markup=reply_markup)

    def __handled(self):
        database.close(self.db)

    def _handled(self, db):
        pass

    def unsubscribe_all(self, bot, update):
        if update.callback_query.data == 'yes':
            for s in self.user.subscriptions:
                self.db.query(Subscription).filter(Subscription.id == s.id).delete()
            bot.send_message(chat_id=update.callback_query.message.chat.id, text='Вы отписались от всех сериалов')
        self.__handled()
