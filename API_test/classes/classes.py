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
        # Если есть тело ответа и код 200
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
        # Попытка распарсить json
            except ValueError:
                return response.status_code, response.text
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{BASE_URL}{endpoint}", params=params, headers=self.create_headers()
        )
        # Если есть тело ответа и код 200
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.status_code, response.text
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def delete(self, endpoint, payload=None):
        response = requests.delete(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если есть тело ответа и код 201
        if response.status_code == 201:
            try:
                return response.status_code, response.text
            # Попытка распарсить json
            except ValueError:
                return response.status_code, response.text
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def put(self, endpoint, payload):
        response = requests.put(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если есть тело ответа и код 200
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.status_code, response.text
        # Возврат для случаев с ошибками или пустым телом
        return response.status_code, response.text

    def patch(self, endpoint, payload):
        response = requests.patch(
            f"{BASE_URL}{endpoint}", json=payload, headers=self.create_headers()
        )
        # Если есть тело ответа и код 200
        if response.status_code == 200 and response.content:
            try:
                response_json = response.json()
                return response.status_code, response_json
            # Попытка распарсить json
            except ValueError:
                return response.status_code, response.text
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
        if status_code == 200:
            token = response_json.get("token")
            return token
        else:
            return status_code


class BookingManager(ApiClient):
    def __init__(self, token=None):
        super().__init__(token)

    def create_booking(self, booking_data):
        status_code, response_json = self.post(
            endpoint="booking",
            payload=booking_data
        )
        print("Создание букинга", response_json)
        if status_code == 200:
            booking_id = response_json.get("bookingid")
            return status_code, response_json, booking_id
        else:
            return status_code, None, None

    def receive_current_booking(self, booking_id):
        status_code, response_json = self.get(
            endpoint=f"booking/{booking_id}"
        )
        print("Получение букинга", response_json)
        if status_code == 200:
            return status_code, response_json
        else:
            return status_code, None

    def delete_booking(self, booking_id):
        status_code, _ = self.delete(endpoint=f"booking/{booking_id}")
        return status_code

    def put_booking(self, booking_id, booking_data):
        status_code, response_json = self.put(
            endpoint=f"booking/{booking_id}",
            payload=booking_data
        )
        print("Изменение букинга", response_json)
        if status_code == 200:
            return status_code, response_json
        else:
            return status_code, None
