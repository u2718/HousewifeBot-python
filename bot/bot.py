import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler
from bot.commands.help import HelpCommand
from bot.commands.shows import ShowsCommand
from bot.commands.start import StartCommand
from bot.commands.subcribe import SubscribeCommand
from bot.commands.unknown import UnknownCommand
from utils.config import Config


class Bot:
    def __init__(self):
        self.bot = telegram.Bot(token=Config().token)
        self.updater = Updater(token=Config().token)
        self.dispatcher = self.updater.dispatcher
        shows_handler = CommandHandler('shows', ShowsCommand().execute)
        start_handler = CommandHandler('start', StartCommand().execute)
        help_handler = CommandHandler('help', HelpCommand().execute)
        unknown_handler = MessageHandler([], UnknownCommand().execute)
        subscribe_command = SubscribeCommand()
        subscribe_handler = ConversationHandler(
            entry_points=[CommandHandler('subscribe', subscribe_command.execute, pass_args=True)],
            states={
                SubscribeCommand.GET_TITLE: [MessageHandler([], subscribe_command.get_title)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(shows_handler)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(subscribe_handler)
        self.dispatcher.add_handler(unknown_handler)

    def start_polling(self):
        self.updater.start_polling()
