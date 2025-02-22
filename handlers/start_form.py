import asyncio
import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery, Message, FSInputFile
)
from dotenv import load_dotenv

from keyboards.form_keyboards import url_keyboard, person_send_keyboard, problem_keyboard, guide_keyboard
from service.google_sheets import async_get_sheet
from service.redis import User
from utils.texts import SECONDARY_TEXT, THIRD_TEXT, FIVE_TEXT, FOUR_TEXT
from utils.validations import check_name, check_email

load_dotenv()

router = Router()


class StartForm(StatesGroup):
    name = State()
    phone = State()
    email = State()


@router.callback_query(lambda c: c.data == "start_form")
async def start_form(c: CallbackQuery):
    await c.message.answer(text=SECONDARY_TEXT, parse_mode="html", reply_markup=problem_keyboard())


@router.callback_query(lambda c: c.data == "second_message")
async def problem(c: CallbackQuery):
    await c.message.answer(text=THIRD_TEXT, parse_mode="html", reply_markup=guide_keyboard())


@router.callback_query(lambda c: c.data == "third_message")
async def guide(c: CallbackQuery, state: FSMContext):
    user = await User.get_from_redis(c.message.chat.id)
    if user:
        if user.approved:
            # await c.message.answer("Спасибо, что заполнили форму! Прямо сейчас отправим Вам гайд!")
            f = FSInputFile("files/guide.pdf")
            await c.message.answer_document(f)
            logging.info("Файл отправлен.")

            logging.info("Запущен таймер на 1.30 мин")
            await asyncio.sleep(90)
            await c.message.answer(FOUR_TEXT, reply_markup=person_send_keyboard(), parse_mode="html")

            logging.info("Запущен таймер на 1.30 мин")
            await asyncio.sleep(90)
            s = FSInputFile("img/foto2.jpg")
            await c.message.answer_photo(photo=s, caption=FIVE_TEXT, reply_markup=url_keyboard())
        else:
            await state.set_state(StartForm.name)
            await c.message.answer(text="Для начала пройдем небольшую форму.\nНапишите свое имя:")
    else:
        logging.info(f"Пользователь {c.message.chat.id} не существует в redis.")


@router.message(StartForm.name)
async def name_case(mes: Message, state: FSMContext):
    if await check_name(mes.text):
        await state.update_data(name=mes.text)

        await state.set_state(StartForm.email)
        await mes.answer("Напишите свой email")
    else:
        await mes.answer("Введите корректно имя!")


@router.message(StartForm.email)
async def email_case(mes: Message, state: FSMContext):
    if await check_email(mes.text):
        await state.update_data(email=mes.text)
        data = await state.get_data() # Get all data form

        # Saving data in Google Table
        sheet = await async_get_sheet()
        sheet.append_row([mes.from_user.id, data["name"], data["email"]])

        # update data in redis
        user = await User.get_from_redis(mes.from_user.id)
        await user.update_in_redis(name=data["name"], email=data["email"], approved=True)

        await state.clear() # Cleaning data storge
        await mes.answer("Спасибо, что заполнили форму! Прямо сейчас отправим Вам гайд!")
        f = FSInputFile("files/guide.pdf")
        await mes.answer_document(f)
        logging.info("Файл отправлен.")

        logging.info("Запущен таймер на 1.30 мин")
        await asyncio.sleep(90)
        await mes.answer(FOUR_TEXT, reply_markup=person_send_keyboard(), parse_mode="html")

        logging.info("Запущен таймер на 1.30 мин")
        await asyncio.sleep(90)
        s = FSInputFile("img/foto2.jpg")
        await mes.answer_photo(photo=s, caption=FIVE_TEXT, reply_markup=url_keyboard())
    else:
        await mes.answer("Введите e-mail корректно!")
