from abc import abstractmethod
from data import database
from data.database import User


class AbstractCommand:
    def execute(self, bot, update, args=None):
        with database() as db:
            user = db.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
            if not user:
                user = User(telegram_user_id=update.message.from_user.id,
                            first_name=update.message.from_user.first_name,
                            last_name=update.message.from_user.last_name,
                            user_name=update.message.from_user.username)
                db.add(user)
            return self._execute(db, user, bot, update, args)

    @abstractmethod
    def _execute(self, db, user, bot, update, args):
        pass
