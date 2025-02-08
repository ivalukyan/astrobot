from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from os import getenv
from service.redis import User

load_dotenv()

router = Router()
ADMIN = getenv("ADMINS")


@router.message(Command("admin"))
async def admin(message: Message):
    if str(message.from_user.id) in ADMIN:
        users = await User.get_all_from_redis()
        for user in users:
            if user.approved:
                pass
                # TODO: Дописать рассылку (текст, фото, видео)
            else:
                await message.answer("Скорее заполните форму, Вы упускаете полезную информацию!")
