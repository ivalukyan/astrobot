from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def url_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Жми тут", url=getenv('GUIDE_URL'))]
        ]
    )


def start_form_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Заполнить форму", callback_data="start_form")]
        ]
    )


def person_send_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="УЗНАЙ КАК РЕШИТЬ СВОЙ ЗАПРОС", url=getenv('PROFILE_URL'))],
        ]
    )