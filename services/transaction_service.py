from database.database import Database


class TransactionService:

    def __init__(self):
        self.database = Database()

    def create_transaction(
        self,
        connection,
        account_id,
        transaction_type,
        amount,
        description=""
    ):

        if amount <= 0:
            raise ValueError(
                "Transaction amount must be greater than zero."
            )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO transactions (
                account_id,
                transaction_type,
                amount,
                description
            )
            VALUES (?, ?, ?, ?)
        """, (
            account_id,
            transaction_type,
            amount,
            description
        ))

        return cursor.lastrowid

    def get_transactions(self, account_id):

        connection = self.database.connect()
        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    transaction_type,
                    amount,
                    description,
                    created_at
                FROM transactions
                WHERE account_id = ?
                ORDER BY created_at DESC, id DESC
            """, (account_id,))

            return cursor.fetchall()

        finally:
            connection.close()