from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def url_keyboard()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Узнай как...", url=getenv('PROFILE_URL'))],
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
            [
                InlineKeyboardButton(
                    text="УЗНАЙ КАК РЕШИТЬ СВОЙ ЗАПРОС",
                    switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                        query="Привет, хочу на экспресс разбор, расскажи подробнее☺️",  # Текст, который будет вставлен
                        allow_user_chats=True,  # Разрешить выбор личных чатов
                        allow_bot_chats=False,  # Запретить выбор чатов с ботами
                        allow_group_chats=False,  # Запретить выбор групповых чатов
                        allow_channel_chats=False,  # Запретить выбор каналов
                    ),
                )
            ],
        ]
    )