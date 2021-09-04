from sqlmodel import select

from utils.db_api.commands.commands import save, select_first
from utils.db_api.models import Article


def save_article(id, url, title, date, author, event, place, fragment):
    article = Article(id=id,
                      url=url,
                      title=title,
                      date=date,
                      author=author,
                      event=event,
                      place=place,
                      fragment=fragment
                      )
    return save(article)


def get_last_article():
    statement = select(Article).order_by(Article.date.desc())
    return select_first(statement)
