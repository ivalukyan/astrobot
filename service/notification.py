import logging
from asyncio import sleep
from datetime import datetime, timedelta
from aiogram import Bot
from service.redis import User


async def notification(bot: Bot, user: User):
    if not user.approved:
        now_date = datetime.now()
        if now_date - user.date_joined < timedelta(days=1):
            await bot.send_message(chat_id=user.id, text="Заполните форму до конца!!!")
        else:
            await user.update_in_redis(approved=True)


async def send_not(bot: Bot):
    while True:
        logging.info("Рассылка пользователям, не закончившим форму")
        all_users = await User.get_all_from_redis()  # Предполагается, что у вас есть такой метод
        for user in all_users:
            if not user.approved:
                await notification(bot, user)
        await sleep(1800)
