import asyncio
import logging
import sys

from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from dotenv import load_dotenv

from handlers.start_form import router as start_form_router
from service.redis import User
from datetime import datetime


load_dotenv()

TOKEN = getenv("BOT_TOKEN")

router = Router()

bot_object = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@router.message(CommandStart())
async def command_start(message: Message) -> None:

    await message.answer(f"Здравствуйте, {message.from_user.first_name}!", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Заполнить форму", callback_data="start_form")]
        ]
    ))

    user = User(id=message.from_user.id, username=message.from_user.username, approved=False, date_joined=datetime.now())
    await user.save_to_redis()


async def main():
    dp.include_routers(router, start_form_router)
    await dp.start_polling(bot_object)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())