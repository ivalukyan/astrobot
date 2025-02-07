from asyncio import sleep
from datetime import datetime, timedelta
from aiogram.types import Message
from service.redis import User


async def notification(message: Message):
    user = await User.get_from_redis(message.from_user.id)
    if user:
        if not user.approved:
            now_date = datetime.now()
            if now_date - user.date_joined < timedelta(days=1):
                await message.answer("Заполните форму до конца!!!")
            else:
                user.update_in_redis(approved=True)



async def send_not(message: Message):
    user = await User.get_from_redis(message.from_user.id)
    while not user.approved:
        await notification(message)
        await sleep(1800)
