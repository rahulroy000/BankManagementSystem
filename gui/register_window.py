import tkinter as tk
from tkinter import messagebox

from gui.theme import COLORS, FONTS, button


class RegisterWindow(tk.Frame):
    """Modern registration screen with required mobile-number registration."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["background"])
        self.app = app
        self.bank_service = app.bank_service
        self.password_visible = False
        self.confirm_visible = False
        self.build()

    def field(self, parent, label, show=""):
        tk.Label(
            parent,
            text=label,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["small_bold"],
        ).pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(
            parent,
            show=show,
            font=(FONTS["body"][0], 11),
            relief="solid",
            bd=1,
        )
        entry.pack(fill="x", ipady=7, pady=(0, 12))
        return entry

    def build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        outer = tk.Frame(self, bg=COLORS["background"])
        outer.grid(row=0, column=0, sticky="nsew", padx=42, pady=30)
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(0, weight=1)

        card = tk.Frame(
            outer,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=650)

        tk.Label(
            card,
            text="Create your MyBank account",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(FONTS["page"][0], 24, "bold"),
        ).pack(anchor="w", padx=40, pady=(28, 4))

        tk.Label(
            card,
            text="Register your personal details. Your mobile number is used for account recovery.",
            bg=COLORS["surface"],
            fg=COLORS["text_secondary"],
            font=FONTS["body"],
        ).pack(anchor="w", padx=40, pady=(0, 18))

        form = tk.Frame(card, bg=COLORS["surface"])
        form.pack(fill="x", padx=40)
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        def grid_field(row, col, label, show=""):
            box = tk.Frame(form, bg=COLORS["surface"])
            box.grid(row=row, column=col, sticky="ew", padx=(0 if col == 0 else 12, 12 if col == 0 else 0))
            tk.Label(box, text=label, bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["small_bold"]).pack(anchor="w", pady=(0, 5))
            e = tk.Entry(box, show=show, font=(FONTS["body"][0], 11), relief="solid", bd=1)
            e.pack(fill="x", ipady=7, pady=(0, 12))
            return e

        self.name_entry = grid_field(0, 0, "FULL NAME")
        self.dob_entry = grid_field(0, 1, "DATE OF BIRTH")
        self.phone_entry = grid_field(1, 0, "MOBILE NUMBER *")
        self.email_entry = grid_field(1, 1, "EMAIL ADDRESS")

        address_box = tk.Frame(form, bg=COLORS["surface"])
        address_box.grid(row=2, column=0, columnspan=2, sticky="ew")
        tk.Label(address_box, text="ADDRESS", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["small_bold"]).pack(anchor="w", pady=(0, 5))
        self.address_text = tk.Text(address_box, height=3, font=(FONTS["body"][0], 10), relief="solid", bd=1)
        self.address_text.pack(fill="x", pady=(0, 12))

        self.password_entry = grid_field(3, 0, "PASSWORD", "*")
        self.confirm_entry = grid_field(3, 1, "CONFIRM PASSWORD", "*")
        self.account_type = grid_field(4, 0, "ACCOUNT TYPE")
        self.account_type.destroy()
        # Replace the last generated entry with a combobox.
        account_box = tk.Frame(form, bg=COLORS["surface"])
        account_box.grid(row=4, column=0, sticky="ew", padx=(0, 12))
        tk.Label(account_box, text="ACCOUNT TYPE", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["small_bold"]).pack(anchor="w", pady=(0, 5))
        from tkinter import ttk
        self.account_type = ttk.Combobox(account_box, values=["SAVINGS", "CURRENT"], state="readonly")
        self.account_type.pack(fill="x", ipady=5, pady=(0, 12))
        self.account_type.current(0)

        deposit_box = tk.Frame(form, bg=COLORS["surface"])
        deposit_box.grid(row=4, column=1, sticky="ew", padx=(12, 0))
        tk.Label(deposit_box, text="INITIAL DEPOSIT", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["small_bold"]).pack(anchor="w", pady=(0, 5))
        self.deposit_entry = tk.Entry(deposit_box, font=(FONTS["body"][0], 11), relief="solid", bd=1)
        self.deposit_entry.pack(fill="x", ipady=7, pady=(0, 12))

        note = tk.Label(
            card,
            text="✓ New accounts start as INACTIVE for security.\n✓ Activate from the login screen using your registered mobile + temporary OTP.",
            bg=COLORS["primary_soft"],
            fg=COLORS["text_secondary"],
            justify="left",
            anchor="w",
            font=FONTS["small"],
            padx=14,
            pady=9,
        )
        note.pack(fill="x", padx=40, pady=(2, 15))

        actions = tk.Frame(card, bg=COLORS["surface"])
        actions.pack(fill="x", padx=40)
        create = tk.Button(actions, text="CREATE ACCOUNT", command=self.register)
        button(create, "primary").pack(side="left", fill="x", expand=True, ipady=4)
        back = tk.Button(actions, text="BACK TO LOGIN", command=self.app.show_login)
        button(back, "secondary").pack(side="left", fill="x", expand=True, padx=(10, 0), ipady=4)

        self.name_entry.focus()

    def register(self):
        full_name = self.name_entry.get().strip()
        date_of_birth = self.dob_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        account_type = self.account_type.get().strip()
        deposit_text = self.deposit_entry.get().strip()

        required = [
            (full_name, self.name_entry, "Please enter your full name."),
            (date_of_birth, self.dob_entry, "Please enter your date of birth."),
            (phone, self.phone_entry, "Please enter your mobile number."),
            (email, self.email_entry, "Please enter your email."),
            (address, self.address_text, "Please enter your address."),
            (password, self.password_entry, "Please enter a password."),
            (deposit_text, self.deposit_entry, "Please enter an initial deposit."),
        ]
        for value, widget, msg in required:
            if not value:
                messagebox.showwarning("Input Required", msg, parent=self)
                widget.focus()
                return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.", parent=self)
            self.confirm_entry.focus()
            return

        try:
            initial_deposit = float(deposit_text)
            if initial_deposit < 0:
                raise ValueError("Initial deposit cannot be negative.")
        except ValueError as error:
            messagebox.showerror("Invalid Amount", str(error), parent=self)
            self.deposit_entry.focus()
            return

        try:
            result = self.bank_service.register_user(
                full_name=full_name,
                date_of_birth=date_of_birth,
                phone=phone,
                email=email,
                address=address,
                password=password,
                account_type=account_type,
                initial_deposit=initial_deposit,
            )

            messagebox.showinfo(
                "Account Created",
                "Your MyBank account has been created successfully.\n\n"
                f"Account Number: {result['account_number']}\n"
                f"Mobile Number: {phone}\n"
                "Status: INACTIVE\n\n"
                "Go to the login screen, click ACTIVE ACCOUNT, enter your registered mobile number, then verify the temporary OTP.",
                parent=self,
            )
            self.app.show_login()
        except ValueError as error:
            messagebox.showerror("Registration Failed", str(error), parent=self)
        except Exception as error:
            messagebox.showerror("System Error", f"Something went wrong:\n{error}", parent=self)
