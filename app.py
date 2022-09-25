from aiogram import executor

from loader import dp
from utils.news_parser.news_publisher import start_news_publishing
from utils.notify_admins import on_startup_notify


async def setup_sqlmodel():
    from utils.db_api.db import SQLModel, engine

    SQLModel.metadata.create_all(engine)


async def on_startup(dispatcher):
    await setup_sqlmodel()

    await on_startup_notify(dispatcher)

    await start_news_publishing(60)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
