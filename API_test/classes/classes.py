from API_test.constant import BASE_URL
import requests


class ApiClient:
    def __init__(self, token=None):
        self.token = token

    def post(self, endpoint, payload, headers):
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

    def get(self, endpoint, headers, params=None):
        response = requests.get(
            f"{BASE_URL}{endpoint}", params=params, headers=headers
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

    def delete(self, endpoint, headers, payload=None):
        response = requests.delete(
            f"{BASE_URL}{endpoint}", json=payload, headers=headers
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

    def put(self, endpoint, payload, headers):

        response = requests.put(
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

    def patch(self, endpoint, payload, headers):
        response = requests.patch(
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


class Auth(ApiClient):

    def create_auth_headers(self):
        return {
            "Content-Type": "application/json"
        }

    def get_token(self, username, password):
        status_code, response_json = self.post(
            endpoint="auth",
            payload={"username": username, "password": password},
            headers=self.create_auth_headers()
        )
        print(response_json)
        if status_code == 200:
            token = response_json.get("token")
            return token
        else:
            return status_code


class BookingManager(ApiClient):
    def __init__(self, token=None):
        super().__init__(token)

    def create_booking(self, booking_data, headers):
        status_code, response_json = self.post(
            endpoint="booking",
            payload=booking_data,
            headers=headers
        )
        print(headers)
        print(response_json)
        booking_id = response_json.get("bookingid") if isinstance(response_json, dict) else None
        return status_code, booking_id, response_json

    def receive_current_booking(self, booking_id, headers):
        status_code, response_json = self.get(
            endpoint=f"booking/{booking_id}",
            headers=headers
        )
        return status_code, response_json

    def delete_booking(self, booking_id, headers):
        status_code, _ = self.delete(
            endpoint=f"booking/{booking_id}",
            headers=headers
        )
        print(headers)
        print(status_code)
        return status_code

    def put_booking(self, booking_id, booking_data, headers=None):
        status_code, response_json = self.put(
            endpoint=f"booking/{booking_id}",
            payload=booking_data,
            headers=headers
        )
        print(headers)
        print(response_json)
        return status_code, response_json
