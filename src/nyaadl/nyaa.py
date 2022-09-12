from datetime import datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests


@dataclass
class Torrent:
    page_url: str
    torrent_url: str
    magnet_url: str
    date: datetime
    name: str
    category: str
    size: str
    seeds: int
    peers: int
    downloads: int


SUKEBEI_URL = 'https://sukebei.nyaa.si'
NYAA_URL = 'https://nyaa.si'


def lookup(search_words: list[str], sukebei=False) -> list[Torrent]:
    base_url = SUKEBEI_URL if sukebei else NYAA_URL
    response = requests.get(base_url, params={'q': ' '.join(search_words)})
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for tr in soup.select('.torrent-list tbody tr'):
        columns = tr.find_all('td')
        link = columns[1].find_all('a')[-1]
        torrent = Torrent(
            category=columns[0].find('a')['title'],
            name=link.string,
            torrent_url=(
                base_url
                + columns[2].select_one('.fa-download').parent['href']
            ),
            magnet_url=columns[2].select_one('.fa-magnet').parent['href'],
            page_url=link['href'],
            size=columns[3].string,
            date=datetime.fromtimestamp(int(columns[4]['data-timestamp'])),
            seeds=int(columns[5].string),
            peers=int(columns[6].string),
            downloads=int(columns[7].string),
        )
        results.append(torrent)
    return results
