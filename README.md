# RLTBot
 Телеграм бот аггрегирующий статистические данные о зарплатах сотрудников компании по временным промежуткам
 
 **Стек**: Python3, Asyncio, MongoDB, aiogram, datetime, logging, json
## Описание задачи:
Вашей задачей в рамках этого тестового задания будет написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам. Ссылка на скачивание коллекции со статистическими данными, которую необходимо использовать при выполнении задания, находится в конце документа.
На обычном языке пример задачи выглядит следующим образом: “Необходимо посчитать суммы всех выплат с {28.02.2022} по {31.03.2022}, единица группировки - {день}”.

 Входные данные:
| Имя        | Описание                                         |
| ---        | ---                                              |
| dt_from    | Начало временного промежутка в ISO формате       |
| dt_upto    | Конец временного промежутка в ISO формате        |
| group_type | Тип агрегации. (month, day, hour)                |

Выходные данные:
| Имя      | Описание                                                         | 
| ---      | ---                                                              |
| dataset  | Агрегированный массив данных                                     |
| labels   | Подписи к значениям агрегированного массива данных в ISO формате |

Пример входных данных:
{
"dt_from":"2022-09-01T00:00:00",
"dt_upto":"2022-12-31T23:59:00",
"group_type":"month"
}

**Комментарий к входным данным**: вам необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, тип агрегации по месяцу
На выходе ваш алгоритм формирует ответ содержащий:
Агрегированный массив данных (далее dataset)
Подписи к значениям агрегированного массива данных в ISO формате (далее labels)

Пример ответа:
{"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}

**Комментарий к ответу**: в нулевом элементе датасета содержится сумма всех выплат за сентябрь, в первом элементе сумма всех выплат за октябрь и т.д. В лейблах подписи соответственно элементам датасета.
