from abc import abstractmethod
from data import database
from data.database import User


class AbstractCommand:
    def execute(self, bot, update, args=None):
        db = database()
        try:
            user = db.get().query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
            if not user:
                user = User(telegram_user_id=update.message.from_user.id,
                            first_name=update.message.from_user.first_name,
                            last_name=update.message.from_user.last_name,
                            user_name=update.message.from_user.username)
                db.get().add(user)
            return self._execute(db.get(), user, bot, update, args)
        finally:
            self._handled(db)

    @abstractmethod
    def _execute(self, db, user, bot, update, args):
        pass

    def _handled(self, db):
        db.close()
