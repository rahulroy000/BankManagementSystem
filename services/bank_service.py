from database.database import Database
from models.user import User
from models.account import Account

from utils.security import hash_password
from utils.validators import (
    validate_name,
    validate_phone,
    validate_email,
    validate_password,
    validate_initial_deposit
)

from utils.helpers import generate_account_number
from services.transaction_service import TransactionService


class BankService:

    def __init__(self, database=None):
        self.database = database if database is not None else Database()
        self.transaction_service = TransactionService()

    def register_user(
        self,
        full_name,
        date_of_birth,
        phone,
        email,
        address,
        password,
        account_type,
        initial_deposit
    ):
        validate_name(full_name)
        validate_phone(phone)
        validate_email(email)
        validate_password(password)
        validate_initial_deposit(initial_deposit)

        password_hash = hash_password(password)

        user = User(
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone=phone,
            email=email,
            address=address,
            password_hash=password_hash
        )

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id
                FROM users
                WHERE phone = ? OR email = ?
            """, (phone, email))

            if cursor.fetchone():
                raise ValueError(
                    "Phone number or email already registered."
                )

            cursor.execute("""
                INSERT INTO users (
                    full_name,
                    date_of_birth,
                    phone,
                    email,
                    address,
                    password_hash
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user.full_name,
                user.date_of_birth,
                user.phone,
                user.email,
                user.address,
                user.password_hash
            ))

            user_id = cursor.lastrowid

            while True:
                account_number = generate_account_number()
                cursor.execute("""
                    SELECT id
                    FROM accounts
                    WHERE account_number = ?
                """, (account_number,))

                if cursor.fetchone() is None:
                    break

            account = Account(
                user_id=user_id,
                account_number=account_number,
                account_type=account_type,
                balance=initial_deposit
            )

            cursor.execute("""
                INSERT INTO accounts (
                    user_id,
                    account_number,
                    account_type,
                    balance,
                    status
                )
                VALUES (?, ?, ?, ?, 'INACTIVE')
            """, (
                account.user_id,
                account.account_number,
                account.account_type,
                account.get_balance()
            ))

            account_id = cursor.lastrowid

            if initial_deposit > 0:
                self.transaction_service.create_transaction(
                    connection=connection,
                    account_id=account_id,
                    transaction_type="INITIAL_DEPOSIT",
                    amount=initial_deposit,
                    description="Initial account deposit"
                )

            connection.commit()

            return {
                "success": True,
                "user_id": user_id,
                "account_id": account_id,
                "account_number": account_number
            }

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def get_activation_account(self, phone):
        """Return the account registered to this mobile number for activation."""
        phone = str(phone).strip()
        connection = self.database.connect()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    users.id,
                    users.full_name,
                    users.phone,
                    accounts.id,
                    accounts.account_number,
                    accounts.status
                FROM users
                INNER JOIN accounts ON users.id = accounts.user_id
                WHERE users.phone = ?
                LIMIT 1
            """, (phone,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError("No account is registered with this mobile number.")

            user_id, full_name, registered_phone, account_id, account_number, status = row
            if status == "ACTIVE":
                raise ValueError("This account is already active. You can log in normally.")

            return {
                "user_id": user_id,
                "full_name": full_name,
                "phone": registered_phone,
                "account_id": account_id,
                "account_number": account_number,
                "status": status,
            }
        finally:
            connection.close()

    def activate_account(self, account_id):
        """Activate an inactive account after successful OTP verification."""
        connection = self.database.connect()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT status
                FROM accounts
                WHERE id = ?
            """, (account_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError("Account not found.")
            if row[0] == "ACTIVE":
                return False

            cursor.execute("""
                UPDATE accounts
                SET status = 'ACTIVE'
                WHERE id = ?
            """, (account_id,))
            if cursor.rowcount != 1:
                raise ValueError("Account could not be activated.")
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def deposit(self, account_id, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT balance, status
                FROM accounts
                WHERE id = ?
            """, (account_id,))

            account = cursor.fetchone()

            if account is None:
                raise ValueError("Account not found.")

            current_balance, status = account

            if status != "ACTIVE":
                raise ValueError("This account is not active.")

            new_balance = current_balance + amount

            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE id = ?
            """, (new_balance, account_id))

            self.transaction_service.create_transaction(
                connection=connection,
                account_id=account_id,
                transaction_type="DEPOSIT",
                amount=amount,
                description="Cash deposit"
            )

            connection.commit()
            return new_balance

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def withdraw(self, account_id, amount):
        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT balance, status
                FROM accounts
                WHERE id = ?
            """, (account_id,))

            account = cursor.fetchone()

            if account is None:
                raise ValueError("Account not found.")

            current_balance, status = account

            if status != "ACTIVE":
                raise ValueError("This account is not active.")

            if amount > current_balance:
                raise ValueError("Insufficient balance.")

            new_balance = current_balance - amount

            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE id = ?
            """, (new_balance, account_id))

            self.transaction_service.create_transaction(
                connection=connection,
                account_id=account_id,
                transaction_type="WITHDRAW",
                amount=amount,
                description="Cash withdrawal"
            )

            connection.commit()
            return new_balance

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def transfer(self, from_account_id, to_account_number, amount):
        """Transfer money from one account to another account."""

        to_account_number = str(to_account_number).strip()

        if not to_account_number:
            raise ValueError("Please enter the recipient account number.")

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            # Get sender
            cursor.execute("""
                SELECT account_number, balance, status
                FROM accounts
                WHERE id = ?
            """, (from_account_id,))

            sender = cursor.fetchone()

            if sender is None:
                raise ValueError("Your account was not found.")

            sender_account_number, sender_balance, sender_status = sender

            if sender_status != "ACTIVE":
                raise ValueError("Your account is not active.")

            # Get recipient
            cursor.execute("""
                SELECT id, account_number, balance, status
                FROM accounts
                WHERE account_number = ?
            """, (to_account_number,))

            receiver = cursor.fetchone()

            if receiver is None:
                raise ValueError("Recipient account was not found.")

            receiver_id, receiver_account_number, receiver_balance, receiver_status = receiver

            if receiver_status != "ACTIVE":
                raise ValueError("Recipient account is not active.")

            if receiver_id == from_account_id:
                raise ValueError("You cannot transfer money to your own account.")

            if amount > sender_balance:
                raise ValueError("Insufficient balance.")

            new_sender_balance = sender_balance - amount
            new_receiver_balance = receiver_balance + amount

            # Update sender
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE id = ?
            """, (new_sender_balance, from_account_id))

            # Update receiver
            cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE id = ?
            """, (new_receiver_balance, receiver_id))

            # Record sender transaction
            self.transaction_service.create_transaction(
                connection=connection,
                account_id=from_account_id,
                transaction_type="TRANSFER_OUT",
                amount=amount,
                description=f"Transfer to {receiver_account_number}"
            )

            # Record receiver transaction
            self.transaction_service.create_transaction(
                connection=connection,
                account_id=receiver_id,
                transaction_type="TRANSFER_IN",
                amount=amount,
                description=f"Transfer from {sender_account_number}"
            )

            connection.commit()

            return new_sender_balance

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def deactivate_account(self, account_id):
        """Deactivate an account without deleting its data."""

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT status
                FROM accounts
                WHERE id = ?
            """, (account_id,))

            account = cursor.fetchone()

            if account is None:
                raise ValueError("Account not found.")

            status = account[0]

            if status != "ACTIVE":
                raise ValueError("This account is already inactive.")

            cursor.execute("""
                UPDATE accounts
                SET status = 'INACTIVE'
                WHERE id = ?
            """, (account_id,))

            if cursor.rowcount != 1:
                raise ValueError("Account could not be deactivated.")

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def delete_account(self, account_id):
        """
        Permanently delete the account, user data and transactions.

        The account must have a zero balance so money cannot be
        accidentally destroyed by an account deletion.
        """

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT user_id, balance
                FROM accounts
                WHERE id = ?
            """, (account_id,))

            account = cursor.fetchone()

            if account is None:
                raise ValueError("Account not found.")

            user_id, balance = account

            if balance != 0:
                raise ValueError(
                    "Account cannot be deleted while the balance is not zero."
                )

            # Delete transaction history first.
            cursor.execute("""
                DELETE FROM transactions
                WHERE account_id = ?
            """, (account_id,))

            # Delete the bank account.
            cursor.execute("""
                DELETE FROM accounts
                WHERE id = ?
            """, (account_id,))

            if cursor.rowcount != 1:
                raise ValueError("Account could not be deleted.")

            # Delete the user only if this was the user's last account.
            cursor.execute("""
                SELECT COUNT(*)
                FROM accounts
                WHERE user_id = ?
            """, (user_id,))

            remaining_accounts = cursor.fetchone()[0]

            if remaining_accounts == 0:
                cursor.execute("""
                    DELETE FROM users
                    WHERE id = ?
                """, (user_id,))

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def recover_account_number(self, phone):
        phone = phone.strip()

        if not phone:
            raise ValueError("Please enter your mobile number.")

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT a.account_number
                FROM users u
                INNER JOIN accounts a
                    ON a.user_id = u.id
                WHERE u.phone = ?
            """, (phone,))

            row = cursor.fetchone()

            if row is None:
                raise ValueError(
                    "No account found with this mobile number."
                )

            return row[0]

        finally:
            connection.close()

    def reset_password(self, account_number, phone, new_password):
        account_number = account_number.strip()
        phone = phone.strip()

        if not account_number:
            raise ValueError("Please enter your account number.")

        if not phone:
            raise ValueError("Please enter your mobile number.")

        validate_password(new_password)

        # IMPORTANT:
        # This matches your existing security.py API:
        # hash_password(password) -> password_hash
        password_hash = hash_password(new_password)

        connection = self.database.connect()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT u.id
                FROM users u
                INNER JOIN accounts a
                    ON a.user_id = u.id
                WHERE a.account_number = ?
                  AND u.phone = ?
            """, (account_number, phone))

            row = cursor.fetchone()

            if row is None:
                raise ValueError(
                    "Account number and mobile number do not match."
                )

            cursor.execute("""
                UPDATE users
                SET password_hash = ?
                WHERE id = ?
            """, (password_hash, row[0]))

            if cursor.rowcount != 1:
                raise ValueError("Password could not be updated.")

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()
