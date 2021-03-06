from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.news_parser.news_publisher import start_news_publishing
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def setup_sqlmodel():
    from utils.db_api.db import SQLModel, engine

    SQLModel.metadata.create_all(engine)


async def on_startup(dispatcher):
    await setup_sqlmodel()

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)

    await start_news_publishing(60)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
