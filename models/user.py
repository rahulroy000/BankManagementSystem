class User:
    def __init__(
        self,
        full_name,
        date_of_birth,
        phone,
        email,
        address,
        password_hash=None,
        user_id=None
    ):
        self.user_id = user_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.email = email
        self.address = address
        self.password_hash = password_hash

    def display_info(self):
        print(f"Name: {self.full_name}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Phone: {self.phone}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")