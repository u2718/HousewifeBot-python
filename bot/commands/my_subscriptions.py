from bot.commands.abstract_command import AbstractCommand


class MySubscriptionsCommand(AbstractCommand):
    __MAX_ROWS__ = 100

    def _execute(self, db, user, bot, update, args):
        if not user.subscriptions:
            bot.send_message(chat_id=update.message.chat_id, text='Вы не подписаны ни на один сериал')
            return

        subscriptions = ['%s (%s)' % (s.show.title, s.show.original_title) for s in user.subscriptions]
        if len(subscriptions) > MySubscriptionsCommand.__MAX_ROWS__:
            messages = (subscriptions[:len(subscriptions) // 2], subscriptions[len(subscriptions) // 2:])
        else:
            messages = (subscriptions,)
        for row in messages:
            result = '\n'.join(row)
            bot.send_message(chat_id=update.message.chat_id, text=result)
