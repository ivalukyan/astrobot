import asyncio
import logging
import sys

from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)
from dotenv import load_dotenv

from handlers.start_form import router as start_form_router
from handlers.admin import router as admin_router
from keyboards.form_keyboards import start_form_keyboard
from service.redis import User
from utils.texts import START_TEXT_BOT
from datetime import datetime
from service.notification import send_not

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

router = Router()

bot_object = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    exist_user = await User.exist_in_redis(message.from_user.id)
    foto = FSInputFile("img/foto1.jpg")
    if not exist_user:
        await message.answer_photo(photo=foto, caption=f"Здравствуйте, {message.from_user.first_name}, " + START_TEXT_BOT,
                                   reply_markup=start_form_keyboard())

        user = User(id=message.from_user.id, username=message.from_user.username, approved=False,
                    date_joined=datetime.now())
        await user.save_to_redis()
    else:
        user = await User.get_from_redis(message.from_user.id)
        if user.approved:
            await message.answer_photo(photo=foto, caption=f"Здравствуйте, {message.from_user.first_name}, "
                                                           + START_TEXT_BOT)
            f = FSInputFile("files/guide.pdf")
            await message.answer_document(f)
            logging.info("Файл отправлен.")
        else:
            await message.answer("Вы не до конца заполнили форму!")


async def main():
    dp.include_routers(start_form_router, admin_router, router)
    asyncio.create_task(send_not(bot_object))
    await dp.start_polling(bot_object)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
