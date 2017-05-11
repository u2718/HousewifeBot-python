import re
from lxml import html
from data.database import Show, Episode
import requests
import json


class Lostfilm:
    __episodes_url = 'http://www.lostfilm.tv/new/page_{}'
    __shows_url = 'http://www.lostfilm.tv/ajaxik.php'
    __page_size = 10
    __user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    __search_data = "act=serial&type=search&o={}&s=3&t=0"
    __DEFAULT_LAST_LOADED_EPISODE = (247, 17, 2)

    def load_shows(self):
        session = requests.session()
        session.headers["User-Agent"] = self.__user_agent
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        count = 0
        shows = []
        while True:
            response = session.post(self.__shows_url, data=self.__search_data.format(count), headers=headers)
            data = json.loads(response.text)['data']
            if len(data) == 0:
                break
            for show in data:
                s = Show(site_id=int(show['id']), title=show['title'], original_title=show['title_orig'])
                shows.append(s)
            count += len(data)
        return shows

    def load_episodes(self, last_loaded_site_id=__DEFAULT_LAST_LOADED_EPISODE):
        """:returns: {show_id: [episodes]}"""
        if not last_loaded_site_id:
            last_loaded_site_id = self.__DEFAULT_LAST_LOADED_EPISODE
        page_number = 1
        shows = {}
        while True:
            page = html.parse(self.__episodes_url.format(page_number))
            episodes_details = page.xpath('//div[@class="haveseen-btn"]')
            episodes_titles = page.xpath('//div[@class="details-pane"]/div[@class="alpha"][1]')
            stop = False
            for i in range(len(episodes_details)):
                details = re.search('(\d+)-(\d+)-(\d+)', episodes_details[i].attrib['data-code']).groups()
                show_site_id, season_number, episode_number = int(details[0]), int(details[1]), int(details[2])
                if (show_site_id, season_number, episode_number) == last_loaded_site_id:
                    stop = True
                    break

                e = Episode(site_id=None,
                            show_id=show_site_id,
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
