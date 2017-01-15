from io import StringIO
from lxml import html
import requests
import re

from downloaders.torrent import Torrent
from utils.config import Config


class Lostfilm:
    __url = "http://lostfilm.tv/nrdr2.php?c={}&s={}&e={}"
    __login_url = "http://login1.bogi.ru/login.php?referer=https%3A%2F%2Fwww.lostfilm.tv%2F"
    __login_data = "login={}&password={}&module=1&target=http%3A%2F%2Flostfilm.tv%2F&repage=user&act=login".format(
        Config().lostfilm_login, Config().lostfilm_password)
    __user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    def list(self, show_id, season, episode):
        session = self.__login()
        response = session.get(self.__url.format(show_id, season, episode))
        url = re.search('href="(.+?)"', response.text).group(1)
        torrents_response = session.get(url)
        torrents_response.encoding = "cp1251"
        page = html.parse(StringIO(torrents_response.text))

        torrents = []
        for url_node in page.xpath("//table//tr//a"):
            if url_node.getnext() is None:
                continue
            torrent_url = url_node.attrib['href']
            quality_node = url_node.getnext().getnext()
            quality, size_string = re.search("Видео: (.+)\. Размер: (.+)+", quality_node.text).groups()

            torrent = Torrent(torrent_url, Lostfilm.__get_size(size_string), quality)
            torrents.append(torrent)

        return torrents

    def __login(self):
        session = requests.session()
        session.headers["User-Agent"] = self.__user_agent
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = session.post(self.__login_url, data=self.__login_data, headers=headers)
        action = re.search("action=\"(.+?)\"", response.text).group(1)
        matches = re.findall('<input.+?name="(.+?)".+?value="(.+)"', response.text)
        inputs = map(lambda m: "{}={}".format(m[0], m[1]), matches[1:])
        session.post(action, data="&".join(inputs), headers=headers)
        return session

    @staticmethod
    def __get_size(size_string):
        size = float(size_string.split(" ")[0])
        if "ГБ" in size_string:
            size *= 1024
        return size
