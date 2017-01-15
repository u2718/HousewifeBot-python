from configparser import ConfigParser


class Config:
    class __Config:
        def __init__(self):
            config = ConfigParser()
            config.read('.config')
            self.connection_string = config['Database']['connection_string']
            self.shows_update_interval = config.getfloat('Scraper', 'shows_update_interval')
            self.episodes_update_interval = config.getfloat('Scraper', 'episodes_update_interval')
            self.token = config['Telegram']['token']
            self.lostfilm_login = config['Lostfilm']['login']
            self.lostfilm_password = config['Lostfilm']['password']

    _instance = None

    def __init__(self):
        if not Config._instance:
            Config._instance = Config.__Config()

    def __getattr__(self, name):
        return getattr(self._instance, name)
