from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def url_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ЧТО ГОВОРЯТ", url=getenv('CHANEL_URL'))]
        ]
    )


def start_form_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ПРОВЕРИМ", callback_data="start_form")]
        ]
    )


def person_send_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="КОНСУЛЬТАЦИЯ В 🎁", url=getenv('PROFILE_URL'))],
        ]
    )


def problem_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="А ЧЕМ ПРОБЛЕМА?", callback_data="second_message")]
        ]
    )


def guide_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ЗАБРАТЬ ГАЙД", callback_data="third_message")]
    ])