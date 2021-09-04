from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_url_keyboard(url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Article', url=url)
            ],
        ],
    )
