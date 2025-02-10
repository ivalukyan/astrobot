import asyncio
import logging

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError

# Функция для авторизации
def authorize():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("files/cred.json", scope)
    client = gspread.authorize(creds)
    return client

# Асинхронный метод для работы с Google Sheets с повторными попытками
async def async_get_sheet(retries=3, delay=2):
    for attempt in range(retries):
        try:
            client = await asyncio.to_thread(authorize)  # Авторизация
            sheet = await asyncio.to_thread(client.open, "Контакты")  # Открываем таблицу
            worksheet = await asyncio.to_thread(sheet.get_worksheet, 0)  # Получаем лист
            return worksheet  # Успешный результат
        except APIError as e:
            if e.response.status_code == 503:  # Ошибка временной недоступности
                logging.info(f"Google API недоступен. Попытка {attempt + 1}/{retries}")
                await asyncio.sleep(delay * (2 ** attempt))  # Экспоненциальная задержка
            else:
                raise  # Прочие ошибки не обрабатываем
    logging.info("Google Sheets API недоступен после нескольких попыток.")
