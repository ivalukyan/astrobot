import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)

router = Router()


class StartForm(StatesGroup):
    name = State()
    phone = State()
    email = State()


@router.callback_query(lambda c: c.data == "start_form")
async def start_form(c: CallbackQuery, state: FSMContext):
    await state.set_state(StartForm.name)
    await c.message.edit_text("Напишите свое имя")


@router.message(StartForm.name)
async def name_case(mes: Message, state: FSMContext):
    await state.update_data(name=mes.text)
    await state.set_state(StartForm.phone)
    await mes.answer("""Напишите свой номер телефона
    
- Номер должен начинаться с 7
- Без тире, скобок, пробелов
    """)


@router.message(StartForm.phone)
async def phone_case(mes: Message, state: FSMContext):
    await state.update_data(phone=mes.text)
    await state.set_state(StartForm.email)
    await mes.answer("Напишите свой email (необязательно)", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_email")]
        ]
    ))


@router.message(StartForm.email)
async def email_case(mes: Message, state: FSMContext):
    await state.update_data(email=mes.text)
    data = await state.get_data()
    # Saving data in Google Table
    await state.clear()

    f = FSInputFile("files/guide.pdf")
    await mes.answer_document(f)


@router.callback_query(lambda c: c.data == "skip_email")
async def skip_email(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Сохранение в Google Table
    await state.clear()

    f = FSInputFile("files/guide.pdf")
    await c.message.answer_document(f)
