from io import StringIO
from lxml import html
import requests
import re

from downloaders.torrent import Torrent
from utils.config import Config


class Lostfilm:
    __url = "http://lostfilm.tv/v_search.php?c={}&s={}&e={}"
    __login_url = "http://lostfilm.tv/ajaxik.php"
    __login_data = "act=users&type=login&mail={}&pass={}&rem=1".format(
        Config().lostfilm_login, Config().lostfilm_password)
    __user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    def list(self, show_id, season, episode):
        session = self.__login()
        response = session.get(self.__url.format(show_id, season, episode))
        url = re.search('href="(.+?)"', response.text).group(1)
        torrents_response = session.get(url)
        torrents_response.encoding = "utf-8"
        page = html.parse(StringIO(torrents_response.text))

        torrents = []
        for node in page.xpath('//div[@class="inner-box--list"]/div[@class="inner-box--item"]'):
            torrent_url = node.xpath('./div[@class="inner-box--link main"]/a')[0].attrib['href']
            description_node = node.xpath('./div[@class="inner-box--desc"]')[0]
            quality, size_string = re.search("Видео: (.+)\. Размер: (.+)+", description_node.text).groups()
            torrent = Torrent(torrent_url, Lostfilm.__get_size(size_string), quality)
            torrents.append(torrent)

        return torrents

    def __login(self):
        session = requests.session()
        session.headers["User-Agent"] = self.__user_agent
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        session.post(self.__login_url, data=self.__login_data, headers=headers)
        return session

    @staticmethod
    def __get_size(size_string):
        size = float(size_string.split(" ")[0])
        if "ГБ" in size_string:
            size *= 1024
        return size
