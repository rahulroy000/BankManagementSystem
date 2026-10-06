class Transaction:
    def __init__(
        self,
        account_id,
        transaction_type,
        amount,
        description="",
        transaction_id=None
    ):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description

    def display(self):
        print(
            f"{self.transaction_type}: "
            f"₹{self.amount:.2f} - "
            f"{self.description}"
        )