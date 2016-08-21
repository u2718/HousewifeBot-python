from bot.commands.abstract_command import AbstractCommand


class UnknownCommand(AbstractCommand):
    def _execute(self, db, user, bot, update, args):
        bot.send_message(chat_id=update.message.chat_id, text='Пощади, братишка')
