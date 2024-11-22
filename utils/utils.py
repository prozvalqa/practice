import json
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from API_test.classes.classes import Auth


# Функция для создания базовых хедеров
def create_headers(class_object, auth_type="valid", content_type="valid", accept="valid"):

    token = class_object.token
    headers = {}

    # Обработка заголовка Authorization
    if auth_type == "invalid":
        headers["Cookie"] = f"Bearer 'invalid_token'"
    elif auth_type == "empty":
        headers["Cookie"] = None  # type: ignore
    elif auth_type == "without":
        pass  # Не добавляем Cookie
    elif auth_type == "empty_string":
        headers["Cookie"] = ""
    else:  # valid
        headers["Cookie"] = f"token={token}"

    # Обработка заголовка Content-Type
    if content_type == "invalid":
        headers["Content-Type"] = "text/plain"
    elif content_type == "empty":
        headers["Content-Type"] = None  # type: ignore
    elif content_type == "without":
        pass  # Не добавляем Content-Type
    elif content_type == "empty_string":
        headers["Content-Type"] = ""
    else:  # valid
        headers["Content-Type"] = "application/json"

    # Обработка заголовка Accept
    if accept == "invalid":
        headers["Accept"] = "text/plain"
    elif accept == "empty":
        headers["Accept"] = None  # type: ignore
    elif accept == "without":
        pass  # Не добавляем Accept
    elif accept == "empty_string":
        headers["Accept"] = ""
    else:  # valid
        headers["Accept"] = "application/json"

    return headers


# Функция для загрузки схем
def load_all_schemas(directory="API_test/schemas"):
    schemas = {}
    for schema_file in Path(directory).glob("*.json"):  # Загружаем все JSON файлы в директории
        with open(schema_file, "r") as file:
            schemas[schema_file.stem] = json.load(file)  # Сохраняем под именем файла без расширения
    return schemas


# Функция для валидации схем
def validate_schema(response_json, schema):
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Ошибка валидации схемы: {e.message}")


# Функция для получения и проверки созданного букинга
def receive_and_check_booking_id(booking_id, booking_manager, booking_data):
    receiving_status_code, receiving_response_json = booking_manager.receive_current_booking(booking_id=booking_id)
    assert receiving_status_code == 200
    assert receiving_response_json['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
    assert receiving_response_json['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
    assert receiving_response_json['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
    assert receiving_response_json['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
    assert receiving_response_json['bookingdates']['checkin'] == booking_data['bookingdates'][
        'checkin'], "Дата заезда не совпадает"
    assert receiving_response_json['bookingdates']['checkout'] == booking_data['bookingdates'][
        'checkout'], "Дата выезда не совпадает"
    return receiving_response_json
