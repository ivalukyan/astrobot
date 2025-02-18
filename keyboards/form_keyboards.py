from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def url_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Жми тут", url=getenv('GUIDE_URL'))],
        ]
    )