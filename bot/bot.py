import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler
from bot.commands.help import HelpCommand
from bot.commands.my_subscriptions import MySubscriptionsCommand
from bot.commands.shows import ShowsCommand
from bot.commands.start import StartCommand
from bot.commands.subcribe import SubscribeCommand
from bot.commands.unknown import UnknownCommand
from bot.commands.unsubscribe import UnsubscribeCommand
from bot.commands.unsubscribe_all import UnsubscribeAllCommand
from utils.config import Config


class Bot:
    def __init__(self):
        self.bot = telegram.Bot(token=Config().token)
        self.updater = Updater(token=Config().token)
        self.dispatcher = self.updater.dispatcher

        shows_handler = CommandHandler('shows', ShowsCommand().execute)
        self.dispatcher.add_handler(shows_handler)

        start_handler = CommandHandler('start', StartCommand().execute)
        self.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', HelpCommand().execute)
        self.dispatcher.add_handler(help_handler)

        subscribe_command = SubscribeCommand()
        subscribe_handler = ConversationHandler(
            entry_points=[CommandHandler('subscribe', subscribe_command.execute, pass_args=True)],
            states={
                SubscribeCommand.GET_TITLE: [MessageHandler([], subscribe_command.get_title)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(subscribe_handler)

        unsubscribe_command = UnsubscribeCommand()
        unsubscribe_handler = ConversationHandler(
            entry_points=[CommandHandler('unsubscribe', unsubscribe_command.execute, pass_args=True)],
            states={
                UnsubscribeCommand.GET_TITLE: [MessageHandler([], unsubscribe_command.get_title)]
            },
            fallbacks=[]
        )
        self.dispatcher.add_handler(unsubscribe_handler)

        unsubscribe_all_command = UnsubscribeAllCommand()
        unsubscribe_all_handler = CommandHandler('unsubscribe_all', unsubscribe_all_command.execute)
        self.dispatcher.add_handler(CallbackQueryHandler(unsubscribe_all_command.unsubscribe_all))
        self.dispatcher.add_handler(unsubscribe_all_handler)

        my_subscriptions_handler = CommandHandler('my_subscriptions', MySubscriptionsCommand().execute)
        self.dispatcher.add_handler(my_subscriptions_handler)

        unknown_handler = MessageHandler([], UnknownCommand().execute)
        self.dispatcher.add_handler(unknown_handler)

    def start_polling(self):
        self.updater.start_polling()
