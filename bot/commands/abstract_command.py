from abc import abstractmethod
from data import database
from data.database import User


class AbstractCommand:
    def execute(self, bot, update):
        with database() as db:
            user = db.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
            if not user:
                user = User(telegram_user_id=update.message.from_user.id,
                            first_name=update.message.from_user.first_name,
                            last_name=update.message.from_user.last_name,
                            user_name=update.message.from_user.username)
                db.add(user)
            self._execute(db, user, bot, update)

    @abstractmethod
    def _execute(self, db, user, bot, update):
        pass
