from database.database import Database
from utils.security import verify_password


class AuthService:
    def __init__(self, database=None):
        self.database = database if database is not None else Database()

    def login(self, account_number, password):
        connection = self.database.connect()
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT
                    users.id,
                    users.full_name,
                    users.phone,
                    users.password_hash,
                    accounts.id,
                    accounts.account_number,
                    accounts.account_type,
                    accounts.balance,
                    accounts.status
                FROM users
                INNER JOIN accounts ON users.id = accounts.user_id
                WHERE accounts.account_number = ?
            """, (account_number,))
            user = cursor.fetchone()
            if user is None:
                return {"success": False, "message": "Invalid account number or password."}
            (user_id, full_name, phone, password_hash, account_id, account_number,
             account_type, balance, status) = user
            if status != "ACTIVE":
                return {"success": False, "message": "This account is not active."}
            if not verify_password(password, password_hash):
                return {"success": False, "message": "Invalid account number or password."}
            return {
                "success": True,
                "message": "Login successful.",
                "user_id": user_id,
                "full_name": full_name,
                "phone": phone,
                "account_id": account_id,
                "account_number": account_number,
                "account_type": account_type,
                "balance": balance,
                "status": status,
            }
        finally:
            connection.close()
