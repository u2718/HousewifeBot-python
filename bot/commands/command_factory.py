from bot.commands.help import HelpCommand
from bot.commands.my_subscriptions import MySubscriptionsCommand
from bot.commands.shows import ShowsCommand
from bot.commands.start import StartCommand
from bot.commands.subcribe import SubscribeCommand
from bot.commands.unknown import UnknownCommand
from bot.commands.unsubscribe import UnsubscribeCommand
from bot.commands.unsubscribe_all import UnsubscribeAllCommand


class CommandFactory:
    @staticmethod
    def create(command):
        cmd = command.lower()
        if cmd == '/help':
            return HelpCommand()
        if cmd == '/my_subscriptions':
            return MySubscriptionsCommand()
        if cmd == '/shows':
            return ShowsCommand()
        if cmd == '/start':
            return StartCommand()
        if cmd == '/subscribe':
            return SubscribeCommand()
        if cmd == '/unsubscribe':
            return UnsubscribeCommand()
        if cmd == '/unsubscribe_all':
            return UnsubscribeAllCommand()

        return UnknownCommand()
