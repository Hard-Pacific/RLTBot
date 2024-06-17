from aiogram import types
from aiogram.filters import CommandStart
from loader import bot, dp

@dp.message(CommandStart())
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Здравствуйте, я существую!")
