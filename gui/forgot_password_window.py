import tkinter as tk
from tkinter import messagebox

from utils.validators import validate_password
from gui.theme import COLORS, FONTS, button


class ForgotPasswordWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.title("Reset Password")
        self.geometry("500x560")
        self.minsize(500, 560)
        self.maxsize(500, 560)
        self.configure(bg=COLORS["background"])
        self.transient(app)
        self.grab_set()

        self._center_on_parent()
        self._build()

    def _center_on_parent(self):
        self.update_idletasks()

        parent_x = self.app.winfo_rootx()
        parent_y = self.app.winfo_rooty()
        parent_w = self.app.winfo_width()
        parent_h = self.app.winfo_height()

        width, height = 500, 560
        x = parent_x + max(0, (parent_w - width) // 2)
        y = parent_y + max(0, (parent_h - height) // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def field(self, parent, label, show=""):
        tk.Label(
            parent,
            text=label,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["small_bold"]
        ).pack(anchor="w", padx=42, pady=(0, 5))

        entry = tk.Entry(
            parent,
            font=(FONTS["body"][0], 11),
            relief="solid",
            bd=1,
            show=show
        )
        entry.pack(fill="x", padx=42, ipady=8, pady=(0, 14))
        return entry

    def _build(self):
        card = tk.Frame(
            self,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=510)

        tk.Label(
            card,
            text="Reset Password",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(FONTS["page"][0], 23, "bold")
        ).pack(pady=(28, 4))

        tk.Label(
            card,
            text="Verify your account and create a new password",
            bg=COLORS["surface"],
            fg=COLORS["text_secondary"],
            font=FONTS["body"]
        ).pack(pady=(0, 24))

        self.account_entry = self.field(card, "ACCOUNT NUMBER")
        self.phone_entry = self.field(card, "REGISTERED MOBILE")
        self.password_entry = self.field(card, "NEW PASSWORD", "*")
        self.confirm_entry = self.field(card, "CONFIRM PASSWORD", "*")

        reset = tk.Button(
            card,
            text="RESET PASSWORD",
            command=self.reset_password
        )
        button(reset, "primary")
        reset.pack(fill="x", padx=42, pady=(4, 10), ipady=5)

        cancel = tk.Button(
            card,
            text="Cancel",
            command=self.destroy,
            relief="flat",
            bd=0,
            bg=COLORS["surface"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["surface"],
            activeforeground=COLORS["text"],
            font=FONTS["small_bold"],
            cursor="hand2"
        )
        cancel.pack(pady=(2, 0))

        self.account_entry.focus()
        self.confirm_entry.bind("<Return>", lambda event: self.reset_password())

    def reset_password(self):
        account = self.account_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not account:
            messagebox.showerror(
                "Error", "Please enter your account number.", parent=self
            )
            self.account_entry.focus()
            return

        if not phone:
            messagebox.showerror(
                "Error", "Please enter your registered mobile number.", parent=self
            )
            self.phone_entry.focus()
            return

        if not password:
            messagebox.showerror(
                "Error", "Please enter a new password.", parent=self
            )
            self.password_entry.focus()
            return

        if password != confirm:
            messagebox.showerror(
                "Error", "Passwords do not match.", parent=self
            )
            self.confirm_entry.focus()
            return

        try:
            validate_password(password)
            self.app.bank_service.reset_password(account, phone, password)

            messagebox.showinfo(
                "Success",
                "Your password has been reset successfully.\n\n"
                "You can now login.",
                parent=self
            )
            self.destroy()

        except ValueError as error:
            messagebox.showerror(
                "Reset Failed", str(error), parent=self
            )
        except Exception as error:
            messagebox.showerror(
                "System Error",
                f"Something went wrong:\n{error}",
                parent=self
            )
