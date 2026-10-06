import tkinter as tk
from tkinter import messagebox

from gui.theme import COLORS, FONTS, button


class ForgotAccountWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.title("Recover Account Number")
        self.geometry("500x380")
        self.resizable(False, False)
        self.configure(bg=COLORS["background"])
        self.transient(app)
        self.grab_set()

        self._center_on_parent()
        self._build()

    def _center_on_parent(self):
        self.update_idletasks()
        px, py = self.app.winfo_rootx(), self.app.winfo_rooty()
        pw, ph = self.app.winfo_width(), self.app.winfo_height()
        w, h = 500, 380
        x = px + max(0, (pw - w) // 2)
        y = py + max(0, (ph - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        card = tk.Frame(
            self,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=330)

        tk.Label(
            card,
            text="Recover Account",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(FONTS["page"][0], 23, "bold")
        ).pack(pady=(30, 5))

        tk.Label(
            card,
            text="Enter your registered mobile number",
            bg=COLORS["surface"],
            fg=COLORS["text_secondary"],
            font=FONTS["body"]
        ).pack(pady=(0, 25))

        tk.Label(
            card,
            text="REGISTERED MOBILE",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["small_bold"]
        ).pack(anchor="w", padx=42, pady=(0, 5))

        self.phone_entry = tk.Entry(
            card,
            font=(FONTS["body"][0], 11),
            relief="solid",
            bd=1
        )
        self.phone_entry.pack(fill="x", padx=42, ipady=8)

        recover = tk.Button(
            card,
            text="RECOVER ACCOUNT",
            command=self.recover_account
        )
        button(recover, "primary")
        recover.pack(fill="x", padx=42, pady=(20, 10), ipady=5)

        tk.Button(
            card,
            text="Cancel",
            command=self.destroy,
            relief="flat",
            bd=0,
            bg=COLORS["surface"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["surface"],
            font=FONTS["small_bold"],
            cursor="hand2"
        ).pack()

        self.phone_entry.focus()
        self.phone_entry.bind("<Return>", lambda event: self.recover_account())

    def recover_account(self):
        phone = self.phone_entry.get().strip()

        if not phone:
            messagebox.showerror(
                "Error", "Please enter your mobile number.", parent=self
            )
            self.phone_entry.focus()
            return

        try:
            account_number = self.app.bank_service.recover_account_number(phone)

            messagebox.showinfo(
                "Account Recovered",
                f"Your account number is:\n\n{account_number}",
                parent=self
            )
            self.destroy()

        except ValueError as error:
            messagebox.showerror(
                "Recovery Failed", str(error), parent=self
            )
        except Exception as error:
            messagebox.showerror(
                "System Error",
                f"Something went wrong:\n{error}",
                parent=self
            )
