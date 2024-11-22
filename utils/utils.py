import json
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError


# Функция для валидации схем
def load_all_schemas(directory="API_test/schemas"):
    schemas = {}
    for schema_file in Path(directory).glob("*.json"):  # Загружаем все JSON файлы в директории
        with open(schema_file, "r") as file:
            schemas[schema_file.stem] = json.load(file)  # Сохраняем под именем файла без расширения
    return schemas


def validate_schema(response_json, schema):
    try:
        validate(instance=response_json, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Ошибка валидации схемы: {e.message}")


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
