from utils.utils import validate_schema
from utils.utils import receive_and_check_booking_id


def test_create_booking(booking_manager, booking_data, all_schemas):
    creation_status_code, creation_response_json, booking_id = booking_manager.create_booking(
        booking_data=booking_data
    )
    assert creation_status_code == 200

    # Схема валидации
    booking_schema = all_schemas["booking_schema"]
    validate_schema(creation_response_json, booking_schema)

    # Получение и проверка созданного букинга
    receive_and_check_booking_id(
        booking_id=booking_id, booking_manager=booking_manager, booking_data=booking_data
    )

    # Удаление букинга
    delete_booking_status_code = booking_manager.delete_booking(
        booking_id=booking_id
    )
    assert delete_booking_status_code == 201

    # Попытка получения удаленного букинга
    deleted_booking_status_code, _ = booking_manager.receive_current_booking(
        booking_id=booking_id
    )
    assert deleted_booking_status_code == 404


def test_change_booking(booking_manager, booking_data):
    creation_status_code, creation_response_json, booking_id = booking_manager.create_booking(booking_data)
    assert creation_status_code == 200

    # Получение и проверка созданного букинга
    receiving_response_json = receive_and_check_booking_id(
        booking_id=booking_id, booking_manager=booking_manager, booking_data=booking_data
    )

    # Замена имени
    receiving_response_json["firstname"] = "Valera"

    # Изменение созданного букинга
    change_status_code, change_response_json = booking_manager.put_booking(
        booking_id=booking_id, booking_data=receiving_response_json
    )
    assert change_status_code == 200

    # Получение и проверка измененного букинга
    receive_and_check_booking_id(
        booking_id=booking_id, booking_manager=booking_manager, booking_data=change_response_json
    )
