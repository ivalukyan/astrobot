import logging


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)

from service.google_sheets import async_get_sheet
from service.redis import User

from utils.validations import check_name, check_email, check_phone
from utils.texts import PHONE_RECOMMENDATION

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
    if await check_name(mes.text):
        await state.update_data(name=mes.text)

        await state.set_state(StartForm.phone)
        await mes.answer(PHONE_RECOMMENDATION)
    else:
        await mes.answer("Введите корректно имя!")


@router.message(StartForm.phone)
async def phone_case(mes: Message, state: FSMContext):
    if await check_phone(mes.text):
        await state.update_data(phone=mes.text)

        await state.set_state(StartForm.email)
        await mes.answer("Напишите свой email (необязательно)", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Пропустить", callback_data="skip_email")]
            ]
        ))
    else:
        await mes.answer("Введите номер корректно!\n<i>Пример: 79651234556</i>")


@router.message(StartForm.email)
async def email_case(mes: Message, state: FSMContext):
    if await check_email(mes.text):
        await state.update_data(email=mes.text)
        data = await state.get_data() # Get all data form

        # Saving data in Google Table
        sheet = await async_get_sheet()
        sheet.append_row([mes.from_user.id, data["name"], data["phone"], data["email"]])

        # update data in redis
        user = await User.get_from_redis(mes.from_user.id)
        await user.update_in_redis(name=data["name"], phone=data["phone"], email=data["email"], approved=True)

        await state.clear() # Cleaning data storge
        await mes.answer("Спасибо, что заполнили форму! Прямо сейчас отправим Вам гайд!")
        f = FSInputFile("files/guide.pdf")
        await mes.answer_document(f)
        logging.info("Файл отправлен.")
    else:
        await mes.answer("Введите e-mail корректно!")


@router.callback_query(lambda c: c.data == "skip_email")
async def skip_email(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Сохранение в Google Table
    sheet = await async_get_sheet()
    sheet.append_row([c.message.chat.id, data["name"], data["phone"]])

    # update data in redis
    user = await User.get_from_redis(c.message.chat.id)
    await user.update_in_redis(name=data["name"], phone=data["phone"], approved=True)

    await state.clear()

    await c.message.answer("Спасибо, что заполнили форму! Прямо сейчас отправим Вам гайд!")
    f = FSInputFile("files/guide.pdf")
    await c.message.answer_document(f)
    logging.info("Файл отправлен.")
