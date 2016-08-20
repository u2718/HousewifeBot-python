from bot.commands.abstract_command import AbstractCommand
from data.database import Show


class ShowsCommand(AbstractCommand):
    def _execute(self, db, user, bot, update):
        shows = ['%s (%s)' % (show.title, show.original_title) for show in db.query(Show)]
        for shows_part in (shows[:len(shows)//2], shows[len(shows)//2:]):
            result = '\n'.join(shows_part)
            bot.send_message(chat_id=update.message.chat_id, text=result)
