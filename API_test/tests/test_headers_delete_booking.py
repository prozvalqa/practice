from utils.utils import receive_and_check_booking_id
from utils.utils import create_headers


# Функция для создания и получение букинга
def setup_preconditions(booking_manager, booking_data):
    # Создание букинга
    creation_status_code, creation_response_json, booking_id = booking_manager.create_booking(
        booking_data=booking_data
    )
    assert creation_status_code == 200

    # Получение и проверка созданного букинга
    receive_and_check_booking_id(
        booking_id=booking_id, booking_manager=booking_manager, booking_data=booking_data
    )
    return booking_id


def test_invalid_token(booking_manager, booking_data):
    # Выполнение предварительных шагов
    booking_id = setup_preconditions(
        booking_manager=booking_manager, booking_data=booking_data
    )

    # Создание заголовков
    headers = create_headers(booking_manager, auth_type="invalid")

    # Удаление букинга
    delete_booking_status_code = booking_manager.delete_booking(
        booking_id=booking_id, headers=headers
    )
    assert delete_booking_status_code == 403


def test_empty_token(booking_manager, booking_data):
    # Выполнение предварительных шагов
    booking_id = setup_preconditions(
        booking_manager=booking_manager, booking_data=booking_data
    )

    # Создание заголовков
    headers = create_headers(booking_manager, auth_type="empty")

    # Удаление букинга
    delete_booking_status_code = booking_manager.delete_booking(
        booking_id=booking_id, headers=headers
    )
    assert delete_booking_status_code == 403


def test_empty_string_token(booking_manager, booking_data):
    # Выполнение предварительных шагов
    booking_id = setup_preconditions(
        booking_manager=booking_manager, booking_data=booking_data
    )

    # Создание заголовков
    headers = create_headers(booking_manager, auth_type="empty_string")

    # Удаление букинга
    delete_booking_status_code = booking_manager.delete_booking(
        booking_id=booking_id, headers=headers
    )
    assert delete_booking_status_code == 403


def test_without_token(booking_manager, booking_data):
    # Выполнение предварительных шагов
    booking_id = setup_preconditions(
        booking_manager=booking_manager, booking_data=booking_data
    )

    # Создание заголовков
    headers = create_headers(booking_manager, auth_type="without")

    # Удаление букинга
    delete_booking_status_code = booking_manager.delete_booking(
        booking_id=booking_id, headers=headers
    )
    assert delete_booking_status_code == 403