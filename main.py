from bot.bot import Bot
from scrapers.scraper import Scraper

scraper = Scraper()
scraper.start()

bot = Bot()
bot.start_polling()
