from bot.commands.abstract_command import AbstractCommand


class UnsubscribeAllCommand(AbstractCommand):
    def _execute(self, db, user, bot, update, args):
        bot.send_message(chat_id=update.message.chat_id, text='UnsubscribeAllCommand')
