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

        # dict необходим для замены апострофов на кавычки
        documents = list(documents)
        dict = { '"':"'", "'":'"' }
        dict_result = {"dataset": [], "labels": []}

        # Обнуляем минуты и секунды
        # В зависимости от group_type также обнуляем часы или приравниваем дни к 1
        if group_type == "dayOfYear":
                for document in documents:
                        dict_result["dataset"].append(document["total"])
                        dict_result["labels"].append(document["label"].replace(hour=0, minute=0, second=0))
        elif group_type == "month":
                for document in documents:
                        dict_result["dataset"].append(document["total"])
                        dict_result["labels"].append(document["label"].replace(day=1, hour=0, minute=0, second=0))
        elif group_type == "hour":
                for document in documents:
                        dict_result["dataset"].append(document["total"])
                        dict_result["labels"].append(document["label"].replace(minute=0, second=0))
  
        # Заполняем пропущенные даты
        # В dataset указываем 0 в пропусках
        if group_type == "dayOfYear":
                current_date = dt_from.replace(hour=0, minute=0, second=0)
                index = 0
                # Проходимся по всем датам с dt_from по dt_upto
                while current_date <= dt_upto :
                        if current_date not in dict_result["labels"]:
                                dict_result["labels"].insert(index, current_date)
                                dict_result["dataset"].insert(index, 0)
                        index += 1
                        current_date += timedelta(days=1)
        if group_type == "hour":
                current_date = dt_from.replace(minute=0, second=0)
                index = 0
                # Проходимся по всем датам с dt_from по dt_upto
                while current_date <= dt_upto :
                        if current_date not in dict_result["labels"]:
                                dict_result["labels"].insert(index, current_date)
                                dict_result["dataset"].insert(index, 0)
                        index += 1
                        current_date += timedelta(hours=1)

        # Приводим даты в читаемый ISO формат
        # Отправляем агрегированные данные в чат
        dict_result["labels"] = [i.isoformat() for i in dict_result["labels"]]
        await bot.send_message(message.from_user.id, ''.join(dict.get(c, c) for c in str(dict_result)))
