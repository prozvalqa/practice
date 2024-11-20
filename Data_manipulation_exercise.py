from datetime import datetime


def get_operator():
    return {
        "email": "prozvalqa@gmail.com",
        "name": "Val"
    }


response = {
    "state": 0,
    "data": [
        {
            "_id": "3d8c861f-e2c0-442a-9d82-810ae5eb5f52",
            "count": 1,
            "brand_id": 84375,
            "delay": 1,
            "startedAt": "2024-03-21T16:48:03.513Z",
            "completedAt": "2024-03-21T16:48:03.513Z",
            "completed": 0,
            "wait_refund": 0,
            "refunded": 0
        },
        {
            "_id": "4816385b-a5a5-4341-aedf-6f80bedbdce4",
            "count": 2,
            "brand_id": 88339,
            "delay": 2,
            "startedAt": "2024-03-21T16:27:32.062Z",
            "completedAt": "2024-03-21T16:28:32.062Z",
            "completed": 0,
            "wait_refund": 2,
            "refunded": 0
        },
        {
            "_id": "7e0882b5-38b8-4dcb-9825-625158a92314",
            "count": 16,
            "brand_id": 88339,
            "delay": 3,
            "startedAt": "2024-03-21T16:17:04.723Z",
            "completedAt": "2024-03-21T16:17:04.723Z",
            "completed": 7,
            "wait_refund": 3,
            "refunded": 6
        }
    ]
}

# 1 Надо убедиться, что заказы вообще есть в ответе от сервера
if "data" in response and isinstance(response["data"], list) and len(response["data"]) > 0:
    count = len(response["data"])
    print(f"В ответе есть заказы, их количество: {count}")

# 2 Надо убедиться, что время выполнение первого и второго заказов не превышает 6 часов
if "data" in response and isinstance(response["data"], list) and len(response["data"]) >= 2:

    # Получаем startedAt и completedAt для первого заказа
    first_started_at = datetime.fromisoformat(response["data"][0].get("startedAt").replace("Z", "+00:00"))
    first_completed_at = datetime.fromisoformat(response["data"][1].get("completedAt").replace("Z", "+00:00"))

    # Получаем startedAt и completedAt для второго заказа
    second_started_at = datetime.fromisoformat(response["data"][0].get("startedAt").replace("Z", "+00:00"))
    second_completed_at = datetime.fromisoformat(response["data"][1].get("completedAt").replace("Z", "+00:00"))

    # Рассчитываем разницу во времени
    first_duration = (first_completed_at - first_started_at).total_seconds() / 3600  # в часах
    second_duration = (second_completed_at - second_started_at).total_seconds() / 3600  # в часах

    # Проверяем, укладывается ли в 6 часов
    if first_duration <= 6 and second_duration <= 6:
        print("Время выполнения первых двух заказов не превышает 6 часов.")
    else:
        print("Время выполнения одного или обоих заказов превышает 6 часов.")
else:
    print("Массив data пуст или содержит менее двух заказов.")

# 3 Надо убедиться, что для третьего заказа все услуги обработаны И выполнено не меньше половины. Ну или по крайней мере
# на текущий момент возвращено не больше, чем выполнено, а ожидают возврат не больше, чем уже возвращено

if "data" in response and isinstance(response["data"], list) and response["data"]:
    # Достаем нужные значения из третьего заказа
    third_order_count = response["data"][2].get("count")
    third_order_completed = response["data"][2].get("completed")
    third_order_wait_refund = response["data"][2].get("wait_refund")

    # Условия для выполнения
    third_order_refunded = response["data"][2].get("refunded")
    if (third_order_count - (third_order_refunded + third_order_completed + third_order_wait_refund) == 0
        and third_order_count / third_order_completed <= 2) or ((third_order_refunded <= third_order_completed) and
                                                                third_order_wait_refund <= third_order_refunded):
        print("Условие задания выполнено")
    else:
        print("Условие задания не выполнено")


# ID всех заказов
def orders_id(response):
    report = []
    for item in response["data"]:
        report.append(item["_id"])
    report.append("326b23a1-e6ab-4b4a-84a1-a3ecb33afc97")
    return report


# Подсчет статусов
def count_status(response):
    total_completed = 0
    total_wait_refund = 0
    total_refunded = 0
    for order in response["data"]:
        total_completed += order.get("completed")
        total_wait_refund += order.get("wait_refund")
        total_refunded += order.get("refunded")

    return {
        "completed": total_completed,
        "wait_refund": total_wait_refund,
        "refunded": total_refunded,
    }


report = {
    "Контакты": get_operator(),
    "ID всех заказов": orders_id(response),
    "Статусы заказов": count_status(response)
}
print(report)
