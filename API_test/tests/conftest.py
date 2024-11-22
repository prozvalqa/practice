import pytest
from faker import Faker
from API_test.classes.classes import ApiClient
from API_test.classes.classes import Auth
from API_test.classes.classes import BookingManager
from utils.utils import load_all_schemas


@pytest.fixture(scope="session")
def all_schemas():
    return load_all_schemas("/Users/valeryprozorov/PycharmProjects/Pomidor_mentoring/API_test/schemas")


@pytest.fixture
def auth():
    # Создаём экземпляр класса Auth
    auth = Auth()
    return auth


@pytest.fixture
def auth_token(auth):
    # Получаем токен через Auth
    token = auth.get_token(username="admin", password="password123")
    return token


@pytest.fixture
# Создаём экземпляр класса ApiClient с токеном
def api_client(auth_token):
    api_client = ApiClient(token=auth_token)
    return api_client


@pytest.fixture
# Создаём экземпляр класса BookingManager
def booking_manager(auth_token):
    booking_manager = BookingManager(token=auth_token)
    return booking_manager


@pytest.fixture()
def booking_data():
    fake = Faker()
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }


