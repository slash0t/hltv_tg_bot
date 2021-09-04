import asyncio
import logging
from datetime import datetime, timedelta

from data.config import CHANNEL_ID
from keyboards.inline.news_url import get_url_keyboard
from loader import bot
from utils.db_api.commands.article import get_last_article, save_article
from utils.db_api.models import Article
from utils.news_parser.parser import parse_hltv

DATE_FORMAT = '%a, %d %b %Y %H:%M GMT'


async def publish_news(sleep_time):
    last_post = get_last_article()
    if last_post:
        last_post_date = last_post.date
    else:
        last_post_date = datetime.utcnow() - timedelta(days=7)

    articles_data = parse_hltv(last_post_date)

    for article_data in articles_data[::-1]:
        article: Article = save_article(**article_data)

        if article.event:
            info_text = f'<em>{article.place} - {article.event}</em>'
        else:
            info_text = f'<em>{article.place}</em>'
        fragment_text = f'{article.fragment}\n' if article.fragment else ''
        date_text = article.date.strftime(DATE_FORMAT)

        news_message_text = f'<b>{article.title}</b>\n' \
                            f'{info_text}\n\n' \
                            f'{fragment_text}' \
                            f'<em>by {article.author}, at {date_text}</em>\n'

        await bot.send_message(CHANNEL_ID,
                               news_message_text,
                               reply_markup=await get_url_keyboard(article.url)
                               )
        logging.info(f'Saved article: {article.title}')
        await asyncio.sleep(3)

    logging.info(f'{sleep_time} seconds until next news update')
    await asyncio.sleep(sleep_time)
    await publish_news(sleep_time)


async def start_news_publishing(sleep_time):
    logging.info('News publishing loop started')
    await publish_news(sleep_time)
