# MyBank - Bank Management System

A desktop Bank Management System built with **Python, Tkinter, SQLite, and Object-Oriented Programming (OOP)**.

MyBank provides a modern banking interface for account registration, account activation, authentication, deposits, withdrawals, transfers, transaction history, and account management.

> ⚠️ **IMPORTANT:** This project is an educational/demo banking application. It is not intended for real financial transactions or production banking use.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Account Activation](#account-activation)
- [Banking Operations](#banking-operations)
- [Account Management](#account-management)
- [Database](#database)
- [Project Structure](#project-structure)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## How It Works

MyBank is a local desktop banking application.

The general workflow is:

```text
Start Application
       ↓
Login Screen
       ↓
Create New Account
       ↓
Register User + Mobile Number
       ↓
Account Created
       ↓
Activate Account
       ↓
Registered Mobile Number
       ↓
Temporary OTP
       ↓
Verify OTP
       ↓
Account becomes ACTIVE
       ↓
Login
       ↓
Bank Dashboard
       ↓
Deposit / Withdraw / Transfer / Transactions
```

The application stores its banking data locally in an SQLite database.

---

## Features

### Authentication

- Account number login
- Password authentication
- Show/hide password
- Forgot Account Number
- Forgot Password
- Account activation from the login screen

### Registration

- Full name
- Date of birth
- Mobile number
- Email
- Address
- Password
- Account type
- Initial deposit

### Account Activation

- Activation from the login screen
- Registered mobile number verification
- Temporary OTP generation
- OTP verification
- Account status changes to `ACTIVE`
- User can then log in normally

### Dashboard

- Available balance
- Account status
- Registered mobile number
- Account number
- Account type
- Recent transactions
- Quick banking actions
- Refresh balance/data
- Balance show/hide

### Banking Operations

- Cash deposit
- Cash withdrawal
- Account-to-account transfer
- Transaction history
- Transfer validation
- Insufficient balance validation

### Account Management

- Deactivate account
- Reactivate through mobile/OTP activation flow
- Permanently delete account
- Delete transaction history associated with the account
- Permanent deletion confirmation using `DELETE`
- Account deletion requires zero balance

---

## Prerequisites

Before running MyBank, install:

- **Python 3.x**
- Tkinter
- SQLite

Tkinter and SQLite are included with standard Python installations on most systems.

Check Python:

```bash
python --version
```

Example:

```text
Python 3.14.0
```

---

## Installation

### Option 1 - Download ZIP

1. Open the GitHub repository.
2. Click **Code**.
3. Select **Download ZIP**.
4. Extract the ZIP.
5. Open the extracted project folder.

### Option 2 - Clone with Git

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then:

```bash
cd BankManagementSystem
```

---

## Run the Application

From the project root:

```bash
python main.py
```

The application will initialize the SQLite database and create the required tables if they do not already exist.

You may see:

```text
Database tables created successfully.
```

This is normal.

---

## Usage

### 1. Create an Account

From the login screen, click:

**Create New Account**

Enter the requested registration information:

- Full name
- Date of birth
- Mobile number
- Email
- Address
- Password
- Account type
- Initial deposit

Complete the registration process.

---

### 2. Activate Your Account

If the account is inactive, return to the login screen and select:

**Activate Account**

Enter the **same mobile number used during registration**.

The application generates a temporary OTP.

Enter the OTP and verify it.

After successful verification:

```text
INACTIVE
   ↓
OTP Verification
   ↓
ACTIVE
```

The account can then be used for normal login.

> ℹ️ The current project uses a temporary/demo OTP displayed by the application. It does not send a real SMS.

---

### 3. Login

Enter:

```text
Account Number
Password
```

Then click:

**LOGIN**

Only an active account can complete normal login.

---

## Account Activation

The activation flow is intentionally available from the login screen.

```text
Login Screen
     │
     └── Activate Account
              │
              ↓
      Registered Mobile
              │
              ↓
       Generate OTP
              │
              ↓
         Enter OTP
              │
              ↓
        Verify OTP
              │
              ↓
      Account = ACTIVE
              │
              ↓
            Login
```

The registered mobile number must match the mobile number stored for the account.

---

## Banking Operations

### Deposit

1. Open **Deposit**.
2. Enter the amount.
3. Confirm the deposit.
4. The account balance is updated.
5. A deposit transaction is recorded.

### Withdraw

1. Open **Withdraw**.
2. Enter the amount.
3. Confirm the withdrawal.
4. The system checks the available balance.
5. The balance and transaction history are updated.

Withdrawal is not allowed when the account does not have sufficient balance.

### Transfer

1. Open **Transfer**.
2. Enter the recipient account number.
3. Enter the transfer amount.
4. Review the transfer.
5. Confirm.

The system validates:

- Sender account
- Recipient account
- Active account status
- Available balance
- Transfer amount

A successful transfer creates transaction records for both sides.

---

## Transaction History

The transaction section displays account activity such as:

```text
INITIAL_DEPOSIT
DEPOSIT
WITHDRAW
TRANSFER_OUT
TRANSFER_IN
```

Transactions include information such as date, type, amount, and description.

---

## Account Management

Open the **Account** section from the dashboard.

### Deactivate Account

Deactivation changes:

```text
ACTIVE → INACTIVE
```

The account data is retained.

The user is logged out after deactivation.

An inactive account cannot perform normal login until it is activated again.

### Delete Account

Permanent deletion is protected by confirmation.

The account must have:

```text
Balance = ₹0
```

The application asks the user to type:

```text
DELETE
```

Only the exact confirmation text is accepted.

Permanent deletion removes the account and its associated transaction data according to the application's database logic.

> ⚠️ Permanent deletion cannot be undone.

---

## Database

MyBank uses **SQLite** for local persistent storage.

The database is created locally by the application.

Typical location:

```text
data/bank.db
```

### Important

The database file should **NOT** be uploaded to GitHub.

It can contain:

- User information
- Mobile numbers
- Account information
- Password hashes
- Balances
- Transaction history

The repository should contain the database **code/schema**, not your personal/local database.

When another user downloads the project, their local database can be created automatically when they run the application.

---

## Project Structure

```text
BankManagementSystem/
│
├── main.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── account.py
│   └── transaction.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── bank_service.py
│   └── transaction_service.py
│
├── gui/
│   ├── __init__.py
│   ├── app.py
│   ├── login_window.py
│   ├── register_window.py
│   ├── dashboard.py
│   ├── transaction_history.py
│   ├── forgot_account_window.py
│   ├── forgot_password_window.py
│   └── theme.py
│
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   ├── security.py
│   └── helpers.py
│
└── data/
    └── bank.db
```

> `data/bank.db` is a local runtime file and should normally be excluded from Git.

---

## Security Notes

This project is designed for learning and demonstration.

It should **not** be used for real banking or financial transactions.

Do not commit the following to a public repository:

```text
data/bank.db
real customer information
real mobile numbers
real account numbers
private credentials
API keys
secrets
```

Use a `.gitignore` file:

```gitignore
data/bank.db
data/*.db
__pycache__/
*.py[cod]
venv/
.venv/
.vscode/
.idea/
*.log
```

---

## Troubleshooting

### `python` is not recognized

Check that Python is installed:

```bash
python --version
```

If necessary, install Python and enable the option to add Python to PATH.

### Database error

Make sure you are running the application from the project root:

```bash
cd BankManagementSystem
python main.py
```

### Account is not active

Use:

```text
Activate Account
→ Registered Mobile Number
→ Generate OTP
→ Enter OTP
→ Verify OTP
```

Then try logging in again.

### Transfer does not work

Check:

- Recipient account number is correct.
- Recipient account exists.
- Both accounts are active.
- Sender has sufficient balance.
- Transfer amount is valid.

### Database should not be shared

If you downloaded the project from GitHub, you do not need someone else's `bank.db`.

Run:

```bash
python main.py
```

and use the application's registration flow.

---

## FAQ

### Does the project require MySQL?

No.

MyBank uses SQLite.

### Does the user need to manually create the database?

Normally, no. The application initializes the database when it starts.

### Is the OTP sent by SMS?

No. The current project uses a temporary/demo OTP displayed by the application.

### Can an inactive account log in?

No. The account must be activated first.

### Can an account with money be deleted?

No. The account must have a zero balance before permanent deletion.

### Is the database included on GitHub?

It should not be. The local `bank.db` should be excluded with `.gitignore`.

### Is this a real banking application?

No. It is an educational/demo project.

---

## Contributing

Contributions are welcome.

Suggested workflow:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the application.
5. Commit your changes.
6. Open a pull request.

Example:

```bash
git checkout -b feature/new-feature
```

Then:

```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

## Future Enhancements

Possible future improvements include:

- Real SMS OTP integration
- Email OTP
- Multi-factor authentication
- Password reset improvements
- Admin dashboard
- Account statements
- PDF statement export
- Better transfer receipts
- Transaction search and filtering
- Profile editing
- Real-time notifications
- Improved database migrations
- Automated testing
- Packaging as a Windows executable
- Production-grade security

---

## License

Add your preferred open-source license here.

For example:

```text
MIT License
```

if the project is released under MIT.
