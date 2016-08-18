import re
from lxml import html
from data.database import Show, Episode


class Lostfilm:
    episodes_url = 'http://www.lostfilm.tv/browse.php?o={}'
    shows_url = 'http://www.lostfilm.tv/serials.php'
    page_size = 15

    def load_shows(self):
        page = html.parse(self.shows_url)
        shows = []
        for node in page.xpath('//div[@class="mid"]//a[@class="bb_a"]'):
            site_id = int(re.search('cat=(.+)', node.attrib['href']).group(1))
            title = node.text
            original_title = re.search('\((.+)\)', node.getchildren()[1].text).group(1)
            s = Show(site_id=site_id, title=title, original_title=original_title)
            shows.append(s)
        return shows

    def load_episodes(self, last_loaded_site_id=19081):
        """:returns: {show_id: [episodes]}"""
        if not last_loaded_site_id:
            last_loaded_site_id = 19081
        page_number = 0
        shows = {}
        while True:
            page = html.parse(self.episodes_url.format(page_number * self.page_size))
            episodes_details = page.xpath('//div[@class="content_body"]/a[@class="a_discuss"]')
            episodes_ids = page.xpath('//div[@class="content_body"]/a[@class="a_details"]')
            episodes_titles = page.xpath('//div[@class="content_body"]/span[@class="torrent_title"]/b')
            stop = False
            for i in range(len(episodes_details)):
                site_id = int(re.search('id=(.+)', episodes_ids[i].attrib['href']).group(1))
                if site_id <= last_loaded_site_id:
                    stop = True
                    break
                details = re.search('cat=(\d+).+s=(\d+)\..+e=(\d+)', episodes_details[i].attrib['href']).groups()
                show_site_id, season_number, episode_number = int(details[0]), int(details[1]), int(details[2])
                e = Episode(site_id=site_id,
                            title=episodes_titles[i].text,
                            season_number=season_number,
                            episode_number=episode_number)
                if show_site_id not in shows:
                    shows[show_site_id] = []
                shows[show_site_id].append(e)
            if stop:
                break
            page_number += 1
        return shows
