from aiogram import types
from aiogram.filters import CommandStart
from loader import bot, dp
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import json

@dp.message(CommandStart())
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Здравствуйте, я существую!")

@dp.message()
async def agregate(message: types.Message):
        # Подключаемся к sampleDB
        client = MongoClient("localhost", 27017)
        db = client["sampleDB"]
        collection = db["sample_collection"]
        input_text = message.text

        # Преобразуем сообщение от пользователя в json
        # Получаем dt_from, dt_upto, group_type
        input_json = json.loads(input_text)
        dt_from = datetime.fromisoformat(input_json["dt_from"])
        dt_upto = datetime.fromisoformat(input_json["dt_upto"])
        group_type = input_json["group_type"].replace("day", "dayOfYear")

        # Рассматриваем наш временной промежуток от dt_from до dt_upto
        # Считаем сумы по group_type
        # Сортируем по датам и возвращаем наши данные
        documents = collection.aggregate([
                {"$match": {
                        "dt": {
                                "$gte": dt_from,
                                "$lt": dt_upto + timedelta(seconds=1)
                                }
                        }
                },
                {"$group": {
                        "_id": {
                                f"{group_type}": {f"${group_type}": "$dt"}
                                },
                        "total": {"$sum": "$value"},
                        "label": {"$first": "$dt"},
                        }
                },
                {"$sort": {"_id": 1}},
                {"$project": {
                        "_id": 1,
                        "label": 1,
                        "total": 1
                        }
                }
        ])