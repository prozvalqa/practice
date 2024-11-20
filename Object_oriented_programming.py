import pytest

class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Сумма для депозита должна быть положительной.")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            raise ValueError("Сумма снятия превышает доступную")

    def get_balance(self):
        return self.__balance


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0, interest_rate: float = 0.05):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)


class CheckingAccount(BankAccount):
    def withdraw(self, amount: float):
        self._BankAccount__balance -= amount


account = SavingsAccount("Alice")
print(account.get_balance())

account.deposit(500)
print(account.get_balance())

account.withdraw(100)
print(account.get_balance())

account.apply_interest()
print(account.get_balance())


def test_expected_summ():
    try:
        current_balance = account.get_balance()
        assert current_balance > 0, "Итоговый баланс после всех операций больше 0"
    except Exception as exception:
        pytest.fail(f"Тест провалился с исключением: {exception}")
