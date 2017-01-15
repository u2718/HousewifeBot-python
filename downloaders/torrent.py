from urllib import request
import re
import shutil

from utils.config import Config


class Torrent:
    url = ''
    size = 0
    quality = ''

    def __init__(self, url, size, quality):
        self.url = url
        self.size = size
        self.quality = quality

    def download(self):
        path, headers = request.urlretrieve(self.url)
        filename = re.search('filename="(.+?)"', headers["Content-Disposition"]).group(1)
        dst_path = Config().torrents_path.format(filename)
        shutil.move(path, dst_path)
        return dst_path
