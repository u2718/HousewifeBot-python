class Torrent:
    url = ''
    size = 0
    quality = ''

    def __init__(self, url, size, quality):
        self.url = url
        self.size = size
        self.quality = quality
