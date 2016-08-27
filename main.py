from bot.bot import Bot
from bot.notifier import Notifier
from scrapers.scraper import Scraper

bot = Bot()
bot.start_polling()

notifier = Notifier(bot.bot)
notifier.create_shows_notifications()
notifier.create_episodes_notifications()

scraper = Scraper(shows_updated_callback=notifier.create_shows_notifications,
                  episodes_updated_callback=notifier.create_episodes_notifications)
scraper.start()
