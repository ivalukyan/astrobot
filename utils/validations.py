import re
import asyncio


async def check_phone(phone: str) -> bool:
    pattern = re.compile(r"^79[0-9]{9}$")
    if not pattern.match(phone):
        return False
    return True


async def check_name(name: str) -> bool:
    pattern = re.compile(r"^[А-Я][а-я]+$")

    # Проверка по регулярному выражению
    if not pattern.match(name):
        return False

    with open("../files/bad_words.txt") as f:
        bad_words = [line.strip() for line in f]

    # Проверка на содержание плохих слов
    if name.lower() in bad_words:
        return False

    return True



async def check_email(email: str) -> bool:
    pattern = re.compile(r"^[a-z0-9_]{4,}@[a-z]{4,}.[a-z]{2,}$")
    if not pattern.match(email):
        return False
    return True
