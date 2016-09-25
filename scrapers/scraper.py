import threading
from data import database
from data.database import Show, Episode
from scrapers.lostfilm import Lostfilm
from utils.config import Config
from sqlalchemy import exists
from sqlalchemy.sql import func
import logging

logger = logging.getLogger('logger')


class Scraper:
    def __init__(self, shows_updated_callback=None, episodes_updated_callback=None):
        self._scraper = Lostfilm()
        self._shows_updated_callback = shows_updated_callback
        self._episodes_updated_callback = episodes_updated_callback

    def start(self):
        def update(func, interval):
            try:
                func(self._scraper)
            except Exception as e:
                logger.error('An unhandled error occurred: ' + str(e))
            threading.Timer(interval, update, kwargs={'func': func, 'interval': interval}).start()

        update(self._update_shows, Config().shows_update_interval)
        update(self._update_episodes, Config().episodes_update_interval)

    def _update_shows(self, scraper):
        try:
            shows = scraper.load_shows()
        except Exception as e:
            logger.error('An error has occurred while updating shows: ' + str(e))
            return
        updated = False
        with database() as db:
            for show in shows:
                if not db.query(exists().where(Show.site_id == show.site_id)).scalar():
                    updated = True
                    db.add(show)
        if updated and self._shows_updated_callback:
            self._shows_updated_callback()

    def _update_episodes(self, scraper):
        updated = False
        with database() as db:
            last_loaded_site_id = db.query(func.max(Episode.site_id)).one()[0]
            try:
                episodes = scraper.load_episodes(last_loaded_site_id)
            except Exception as e:
                logger.error('An error has occurred while updating episodes: ' + str(e))
                return
            for show_site_id in episodes:
                show = db.query(Show).filter(Show.site_id == show_site_id).first()
                if not show:
                    self._update_shows(scraper)
                    show = db.query(Show).filter(Show.site_id == show_site_id).first()
                if not show:
                    raise Exception('show (site_id=%s) not found' % show_site_id)
                for episode in episodes[show_site_id]:
                    if not db.query(exists().where(Episode.site_id == episode.site_id)).scalar():
                        episode.show_id = show.id
                        db.add(episode)
                        updated = True
        if updated and self._episodes_updated_callback:
            self._episodes_updated_callback()
