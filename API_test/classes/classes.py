from API_test.constant import BASE_URL
import requests


class ApiClient:
    def __init__(self, token=None):
        self.token = token

    def create_headers(self):
        return {
            "Cookie": f"token={self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def post(self, endpoint, payload, headers=None):
        if headers is None:
            headers = self.create_headers()
        response = requests.post(
            f"{BASE_URL}{endpoint}", json=payload, headers=headers
        )
        # Если нет тела ответа
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
        # Попытка распарсить json
            except ValueError:
                return response.text, response.status_code
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{BASE_URL}{endpoint}", params=params, headers=self.create_headers()
        )
        # Если нет тела ответа
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.text, response.status_code
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def delete(self, endpoint, payload=None):
        response = requests.delete(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если нет тела ответа
        if response.status_code == 201 and response.content:
            try:
                return response.status_code, response.text
            # Попытка распарсить json
            except ValueError:
                return response.text, response.status_code
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def put(self, endpoint, payload):
        response = requests.put(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если нет тела ответа
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.text, response.status_code
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def patch(self, endpoint, payload):
        response = requests.patch(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если нет тела ответа
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.text, response.status_code
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text


class Auth(ApiClient):

    def create_headers(self):
        return {
            "Content-Type": "application/json"
        }

    def get_token(self, username, password):
        status_code, response_json = self.post(
            endpoint="auth",
            payload={"username": username, "password": password},
            headers=self.create_headers()
        )
        if status_code != 200:
            raise ValueError(f"Authentication failed: {response_json}")
        token = response_json.get("token")
        if not token:
            raise ValueError(f"Token not found in response: {response_json}")
        return token


class BookingManager(ApiClient):
    def __init__(self, token=None):
        super().__init__(token)

    def create_booking(self, booking_data):
        status_code, response_json = self.post(
            endpoint="booking",
            payload=booking_data
        )
        print(response_json)
        if status_code != 200:
            raise ValueError(f"Booking creation failed: {response_json}")
        booking_id = response_json.get("bookingid")
        if not booking_id:
            raise ValueError(f"Bookingid not found in response: {response_json}")
        return status_code, response_json, booking_id

    def receive_current_booking(self, booking_id):
        status_code, response_json = self.get(
            endpoint=f"booking/{booking_id}"
        )
        if status_code == 404:
            return status_code, {"error": "Booking not found"}
        if status_code != 200:
            raise ValueError(f"Getting a booking failed: {response_json}")
        return status_code, response_json

    def delete_booking(self, booking_id):
        status_code, response_text = self.delete(endpoint=f"booking/{booking_id}")
        if status_code != 201:
            raise ValueError(f"Booking deletion failed: {response_text}")
        return status_code
