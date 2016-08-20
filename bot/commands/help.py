from bot.commands.abstract_command import AbstractCommand


class HelpCommand(AbstractCommand):
    def _execute(self, db, user, bot, update):
        help_template = 'Список команд: \n' \
                        '/shows - вывести список всех сериалов \n' \
                        '/subscribe - подписаться на сериал \n' \
                        '/unsubscribe - отписаться от сериала \n' \
                        '/unsubscribe_all - отписаться от всех сериалов \n' \
                        '/help - справка'
        bot.send_message(chat_id=update.message.chat_id, text=help_template)
