class Account:
    def __init__(
        self,
        account_number,
        account_type,
        balance=0,
        status="ACTIVE",
        account_id=None,
        user_id=None
    ):
        self.account_id = account_id
        self.user_id = user_id
        self.account_number = account_number
        self.account_type = account_type
        self._balance = balance
        self.status = status

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self._balance:
            raise ValueError("Insufficient balance.")

        self._balance -= amount

    def get_balance(self):
        return self._balance

    def display_account(self):
        print(f"Account Number: {self.account_number}")
        print(f"Account Type: {self.account_type}")
        print(f"Balance: ₹{self._balance:.2f}")
        print(f"Status: {self.status}")