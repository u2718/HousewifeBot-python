import logging
from bot.bot import Bot
from bot.notifier import Notifier
from scrapers.scraper import Scraper

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(open('.log', 'a'))
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(levelname)s| %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('Start')

bot = Bot()
bot.start_polling()

notifier = Notifier(bot.bot)
notifier.create_shows_notifications()
notifier.create_episodes_notifications()

scraper = Scraper(shows_updated_callback=notifier.create_shows_notifications,
                  episodes_updated_callback=notifier.create_episodes_notifications)
scraper.start()
