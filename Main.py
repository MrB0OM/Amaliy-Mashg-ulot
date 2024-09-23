
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN
from aiogram import F
import asyncio

API_TOKEN = TOKEN


def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY,
        keyword VARCHAR(200),
        response VARCHAR(200)
    )
    ''')
    responses_data = [
        ("salom", "Salom👋! Qanday yordam bera olishim mumkin?"),
        ("qalaysan?", "Yaxshi👍, rahmat! Sizni qanday yordam bera olishim mumkin?"),
        ("qalesan", "Yaxshi ozingizchi👍!"),
        ("menga hazil ayt", "Nima uchun kompyuter muzlamaydi🧊? Chunki u doim qizib ketadi🔥!"),
        ("isming nima", "mening ismim yoq lekn meni Amaliy desangiz boladi !"),
        ("Amaliy qalesan", "yaxshi ozingiz yaxshimisz👍!"),
        ("Yoshing nechchida", "🔥men 1 kun ishlashim boladi🔥!"),

    ]
    cursor.executemany('''
    INSERT OR IGNORE INTO responses (keyword, response) VALUES (?, ?)
    ''', responses_data)
    conn.commit()
    conn.close()


initialize_database()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Salom user👋 menga xabar yoz📝 !! :) .")


@dp.message(F.text)
async def echo(message: types.Message):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT response FROM responses WHERE keyword = ?', (message.text,))
    result = cursor.fetchone()

    if result:
        await message.reply(result[0])
    else:
        await message.reply("Kechirasiz, bu savolga javobim yo'q.")

    conn.close()


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
