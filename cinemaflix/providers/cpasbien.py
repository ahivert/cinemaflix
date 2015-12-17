import requests
import re

from urlparse import urljoin
from models import Torrent
from provider import BaseProvider


class Cpasbien(BaseProvider):
    url_cat = "view_cat.php?categorie="
    url_search = "recherche"
    url_download = "telechargement"
    seeders_desc = "trie-seeds-d"

    def __init__(self, base_url):
        super(Cpasbien, self).__init__(base_url)

    def search(self, query, cat='films', page=0, limit=None):
        if cat:
            search_url = "{}/{}/{}/{}/page-{},{}".format(
                self.base_url,
                self.url_search,
                cat,
                query.replace(' ', '+'),
                page,
                self.seeders_desc
            )
        else:
            search_url = "{}/{}/{}/page-{},{}".format(
                self.base_url,
                self.url_search,
                query.replace(' ', '+'),
                page,
                self.seeders_desc
            )
        tree_html = super(Cpasbien, self)._get_html(search_url)
        return self._get_rows(tree_html, limit)

    def get_top(self):
        top_url = "http://www.cpasbien.io/view_cat.php?categorie=films&trie=seeds-d"
        response = requests.get(top_url).text
        torrents = self._parse_page(response)
        return torrents

    def _get_torrent_link(self, url):
        filename = re.search("([^/]+)\.html", url).group(1)
        return urljoin(self.base_url, self.url_download + filename + '.torrent')

    def _get_rows(self, html, limit):
        rows = html.xpath('//div[contains(@class, "ligne")]')
        for line in rows[:limit]:
            t = Torrent()
            t.title = (line.xpath('a/text()'))[0]
            t.size = line.xpath('div[@class="poid"]/text()')[0].strip()
            t.seeds = line.xpath(
                'div[@class="up"]/span[contains(@class, "seed_")]/text()')[0]
            t.seeds = line.xpath('div[@class="down"]/text()')[0]
            t.torrent_url = self._get_torrent_link(line.xpath('a/@href')[0])

            yield t
