import re


def validate_name(name):
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    if len(name.strip()) < 3:
        raise ValueError("Name must contain at least 3 characters.")

    return True


def validate_phone(phone):
    pattern = r"^[0-9]{10}$"

    if not re.match(pattern, phone):
        raise ValueError(
            "Phone number must contain exactly 10 digits."
        )

    return True


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        raise ValueError("Invalid email address.")

    return True


def validate_password(password):
    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    return True


def validate_initial_deposit(amount):
    if amount < 0:
        raise ValueError(
            "Initial deposit cannot be negative."
        )

    return True