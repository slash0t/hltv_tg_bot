import logging
import time
from datetime import datetime, timedelta
from typing import List

from bs4 import BeautifulSoup, Tag

import requests

from utils.news_parser.errors import Not200Answer

URL = 'https://www.hltv.org'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'accept': '*/*',
}
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def get_html(url, params=None):
    result = requests.get(url, headers=HEADERS, params=params)
    if result.status_code == 200:
        return result
    else:
        raise Not200Answer()


def get_article_info(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    article = soup.find('article', class_='newsitem')
    article_info = article.find('div', class_='article-info')

    fragment_div = article.find('div', class_='newsdsl')
    fragment_p = fragment_div.find('div', class_='newstext-con').find('p', class_='headertext')
    if fragment_p:
        fragment = fragment_p.text
        # clear unneeded symbols
        fragment = fragment.replace('\u2060', '')
    else:
        fragment = None

    author_div = article_info.find('div', class_='author')
    author = author_div.find('a', class_='authorName').find('span').text

    date_div = article_info.find('div', class_='date')
    data_unix = int(date_div.get('data-unix'))

    # getting time difference between UTC time and server
    gmt_dif = datetime.now() - datetime.utcnow()
    date = datetime.fromtimestamp(data_unix/1000) - gmt_dif
    date = date - timedelta(microseconds=date.microsecond)

    event_div = article.find('div', class_='author-date-con')
    if event_div:
        event = event_div.find('div', class_='event').find('a').text.strip()
    else:
        event = None

    return {
        'fragment': fragment,
        'author': author,
        'date': date,
        'event': event,
    }


def parse_hltv(last_post_date):
    html = get_html(URL)
    soup = BeautifulSoup(html.text, 'html.parser')

    articles: List[Tag] = soup.find_all('a', class_='article')

    articles_data = []
    for article in articles:
        relative_url = article.get('href')
        article_url = URL + relative_url
        article_data = {
            'id': int(relative_url.split('/')[2]),
            'url': article_url,
            'title': article.find('div', class_='newstext').text,
            'place': article.find('img', class_='newsflag').get('title'),
        }
        article_data.update(get_article_info(article_url))

        logging.info(f'Parsed article: {article_data["title"]}')
        if article_data['date'] > last_post_date:
            articles_data.append(article_data)
            # sleep to not get banned
            time.sleep(1)
        else:
            break
    return articles_data


if __name__ == '__main__':
    parse_hltv(datetime.now() - timedelta(days=1))
