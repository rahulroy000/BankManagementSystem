from database.database import Database
from gui.app import BankApp


def main():
    database = Database()
    database.create_tables()

    app = BankApp()
    app.mainloop()


if __name__ == "__main__":
    main()
