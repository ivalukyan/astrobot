import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
from os import getenv
from service.redis import User

load_dotenv()

router = Router()
ADMIN = getenv("ADMINS")

class BroadcastState(StatesGroup):
    waiting_for_message = State()

@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        await message.answer(f"Здравствуйте, {message.from_user.first_name}.", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Рассылка", callback_data="admin_mailing")]
            ]
        ))


@router.callback_query(lambda c: c.data == "admin_mailing")
async def admin_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите сообщение для рассылки:")
    await state.set_state(BroadcastState.waiting_for_message)


@router.message(BroadcastState.waiting_for_message)
async def broadcast_message(message: Message, state: FSMContext):
    users = await User.get_all_from_redis()
    for user in users:
        if user.approved:
            try:
                if message.photo:
                    await message.bot.send_photo(user.id, message.photo[-1].file_id, caption=message.caption)
                elif message.video:
                    await message.bot.send_video(user.id, message.video.file_id, caption=message.caption)
                elif message.document:
                    await message.bot.send_document(user.id, message.document.file_id, caption=message.caption)
                else:
                    await message.bot.send_message(user.id, message.text)
            except Exception as e:
                logging.info(f"Ошибка отправки пользователю {user.id}: {e}")
        else:
            await message.answer("Скорее заполните форму, Вы упускаете полезную информацию!")
    await state.clear()
