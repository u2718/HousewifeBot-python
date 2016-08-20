from bot.commands.abstract_command import AbstractCommand


class HelpCommand(AbstractCommand):
    def _execute(self, db, user, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='HelpCommand')
