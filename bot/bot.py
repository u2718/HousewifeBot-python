import telegram
from telegram.ext import Updater, MessageHandler, Filters
from bot.commands.command_factory import CommandFactory
from utils.config import Config


class Bot:
    def __init__(self):
        self.bot = telegram.Bot(token=Config().token)
        self.updater = Updater(token=Config().token)
        self.dispatcher = self.updater.dispatcher
        unknown_handler = MessageHandler([Filters.command, Filters.text], self._commands_handler)
        self.dispatcher.add_handler(unknown_handler)

    def start_polling(self):
        self.updater.start_polling()

    @staticmethod
    def _commands_handler(bot, update):
        command = CommandFactory.create(update.message.text)
        command.execute(bot, update)
