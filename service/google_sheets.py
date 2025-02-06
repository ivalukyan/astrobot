import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Функция для авторизации (обычный синхронный код)
def authorize():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service/cred.json", scope)
    client = gspread.authorize(creds)
    return client

# Асинхронный метод для работы с Google Sheets
async def async_get_sheet():
    client = await asyncio.to_thread(authorize)  # Запуск в фоновом потоке
    sheet = await asyncio.to_thread(client.open, "api_test")  # Открываем таблицу
    worksheet = await asyncio.to_thread(sheet.get_worksheet, 0)
    return worksheet

