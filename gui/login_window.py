import secrets
import time
import tkinter as tk
from tkinter import messagebox

from gui.forgot_account_window import ForgotAccountWindow
from gui.forgot_password_window import ForgotPasswordWindow
from gui.theme import COLORS, FONTS, button


class LoginWindow(tk.Frame):
    """MyBank login screen with mobile + temporary OTP account activation."""

    OTP_VALID_SECONDS = 300

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["background"])
        self.app = app
        self.auth_service = app.auth_service
        self.bank_service = app.bank_service
        self.password_visible = False
        self.activation_account = None
        self.activation_otp = None
        self.activation_expires_at = 0
        self.build()

    def build(self):
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        left = tk.Frame(self, bg=COLORS["primary_dark"])
        left.grid(row=0, column=0, sticky="nsew")

        content = tk.Frame(left, bg=COLORS["primary_dark"])
        content.place(relx=0.5, rely=0.5, anchor="center", width=430)

        tk.Label(
            content, text="MYBANK", bg=COLORS["primary_dark"], fg="#FFFFFF",
            font=(FONTS["hero"][0], 30, "bold")
        ).pack(anchor="w")
        tk.Label(
            content, text="Banking made simple.", bg=COLORS["primary_dark"], fg="#DCE7FF",
            font=(FONTS["hero"][0], 18, "normal")
        ).pack(anchor="w", pady=(8, 6))
        tk.Label(
            content, text="A simple and secure way to manage your bank account.",
            bg=COLORS["primary_dark"], fg="#AFC5E9", font=FONTS["body"]
        ).pack(anchor="w")

        right = tk.Frame(self, bg=COLORS["background"])
        right.grid(row=0, column=1, sticky="nsew")

        card = tk.Frame(
            right, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=555)

        tk.Label(
            card, text="Welcome back", bg=COLORS["surface"], fg=COLORS["text"],
            font=(FONTS["page"][0], 23, "bold")
        ).pack(anchor="w", padx=38, pady=(30, 4))
        tk.Label(
            card, text="Sign in to continue to your account", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["body"]
        ).pack(anchor="w", padx=38, pady=(0, 22))

        tk.Label(
            card, text="ACCOUNT NUMBER", bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["small_bold"]
        ).pack(anchor="w", padx=38)
        self.account_entry = tk.Entry(card, font=(FONTS["body"][0], 11), relief="solid", bd=1)
        self.account_entry.pack(fill="x", padx=38, pady=(6, 17), ipady=8)

        tk.Label(
            card, text="PASSWORD", bg=COLORS["surface"], fg=COLORS["text"],
            font=FONTS["small_bold"]
        ).pack(anchor="w", padx=38)

        password_row = tk.Frame(card, bg=COLORS["surface"])
        password_row.pack(fill="x", padx=38, pady=(6, 20))
        self.password_entry = tk.Entry(
            password_row, show="*", font=(FONTS["body"][0], 11), relief="solid", bd=1
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8)
        tk.Button(
            password_row, text="Show", command=self.toggle_password, relief="flat", bd=0,
            bg=COLORS["surface"], fg=COLORS["primary"], activebackground=COLORS["surface"],
            activeforeground=COLORS["primary"], font=FONTS["small_bold"], cursor="hand2"
        ).pack(side="right", padx=(7, 0))

        login = tk.Button(card, text="LOGIN", command=self.login)
        button(login, "primary").pack(fill="x", padx=38, ipady=5)

        links = tk.Frame(card, bg=COLORS["surface"])
        links.pack(pady=(12, 8))
        for text, command in [
            ("Forgot Account?", self.open_forgot_account),
            ("Forgot Password?", self.open_forgot_password),
        ]:
            tk.Button(
                links, text=text, command=command, relief="flat", bd=0,
                bg=COLORS["surface"], fg=COLORS["primary"], activebackground=COLORS["surface"],
                activeforeground=COLORS["primary"], font=FONTS["small"], cursor="hand2"
            ).pack(side="left", padx=7)

        # Natural login-style activation link, alongside Forgot Account / Forgot Password.
        activation_links = tk.Frame(card, bg=COLORS["surface"])
        activation_links.pack(pady=(10, 8))
        tk.Label(
            activation_links, text="Account inactive?", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small"]
        ).pack(side="left")
        tk.Button(
            activation_links, text="Activate Account", command=self.open_activation,
            relief="flat", bd=0, bg=COLORS["surface"], fg=COLORS["primary"],
            activebackground=COLORS["surface"], activeforeground=COLORS["primary"],
            font=FONTS["small"], cursor="hand2"
        ).pack(side="left", padx=(4, 0))

        create = tk.Button(card, text="Create New Account", command=self.app.show_register)
        button(create, "secondary").pack(fill="x", padx=38, ipady=4)

        self.account_entry.focus()
        self.password_entry.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.password_entry.config(show="" if self.password_visible else "*")

    def open_forgot_account(self):
        ForgotAccountWindow(self.app)

    def open_forgot_password(self):
        ForgotPasswordWindow(self.app)

    def login(self):
        account = self.account_entry.get().strip()
        password = self.password_entry.get()
        if not account:
            messagebox.showwarning("Input Required", "Please enter your account number.", parent=self)
            self.account_entry.focus()
            return
        if not password:
            messagebox.showwarning("Input Required", "Please enter your password.", parent=self)
            self.password_entry.focus()
            return
        try:
            result = self.auth_service.login(account, password)
        except Exception as error:
            messagebox.showerror("System Error", f"Something went wrong:\n{error}", parent=self)
            return
        if result["success"]:
            self.app.show_dashboard(result)
        else:
            messagebox.showerror("Login Failed", result["message"], parent=self)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def open_activation(self):
        """Start the requested Mobile -> temporary OTP -> Activate flow."""
        dialog = tk.Toplevel(self)
        dialog.title("Activate Account")
        dialog.geometry("470x350")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS["background"])
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        card = tk.Frame(dialog, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=18, pady=18)

        tk.Label(card, text="Activate your account", bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONTS["page"][0], 20, "bold")).pack(anchor="w", padx=28, pady=(22, 4))
        tk.Label(card, text="Enter the mobile number you used during registration.",
                 bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["body"],
                 wraplength=380, justify="left").pack(anchor="w", padx=28, pady=(0, 20))

        tk.Label(card, text="REGISTERED MOBILE NUMBER", bg=COLORS["surface"], fg=COLORS["text"],
                 font=FONTS["small_bold"]).pack(anchor="w", padx=28)
        mobile = tk.Entry(card, font=(FONTS["body"][0], 11), relief="solid", bd=1)
        mobile.pack(fill="x", padx=28, pady=(6, 16), ipady=8)
        mobile.focus()

        def request_otp():
            phone = mobile.get().strip()
            if not phone:
                messagebox.showwarning("Mobile Required", "Please enter your registered mobile number.", parent=dialog)
                mobile.focus()
                return
            try:
                account = self.bank_service.get_activation_account(phone)
            except ValueError as error:
                messagebox.showerror("Activation Failed", str(error), parent=dialog)
                return
            except Exception as error:
                messagebox.showerror("System Error", f"Something went wrong:\n{error}", parent=dialog)
                return

            self.activation_account = account
            self.activation_otp = f"{secrets.randbelow(1_000_000):06d}"
            self.activation_expires_at = time.time() + self.OTP_VALID_SECONDS
            self.show_otp_dialog(dialog)

        btn = tk.Button(card, text="GENERATE TEMP OTP", command=request_otp)
        button(btn, "primary").pack(fill="x", padx=28, ipady=5)
        tk.Button(card, text="Cancel", command=dialog.destroy, relief="flat", bd=0,
                  bg=COLORS["surface"], fg=COLORS["text_secondary"], cursor="hand2").pack(pady=8)
        dialog.bind("<Return>", lambda event: request_otp())

    def show_otp_dialog(self, mobile_dialog):
        mobile_dialog.grab_release()
        mobile_dialog.destroy()

        dialog = tk.Toplevel(self)
        dialog.title("Verify OTP")
        dialog.geometry("500x430")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS["background"])
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        card = tk.Frame(dialog, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=18, pady=18)

        account = self.activation_account
        masked = self.mask_phone(account["phone"])
        tk.Label(card, text="Verify your mobile number", bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONTS["page"][0], 20, "bold")).pack(anchor="w", padx=28, pady=(22, 4))
        tk.Label(card, text=f"OTP generated for {masked}\nAccount: {account['account_number']}",
                 bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["body"],
                 justify="left").pack(anchor="w", padx=28, pady=(0, 12))

        # Local-project OTP display: no SMS gateway is configured.
        otp_box = tk.Frame(card, bg="#EEF5FF", highlightbackground="#BFD3F7", highlightthickness=1)
        otp_box.pack(fill="x", padx=28, pady=(0, 18))
        tk.Label(otp_box, text="TEMP OTP (DEMO)", bg="#EEF5FF", fg=COLORS["text_secondary"],
                 font=FONTS["small_bold"]).pack(pady=(9, 0))
        tk.Label(otp_box, text=self.activation_otp, bg="#EEF5FF", fg=COLORS["primary"],
                 font=(FONTS["page"][0], 25, "bold")).pack(pady=(1, 8))
        tk.Label(otp_box, text="Valid for 5 minutes • displayed here because no SMS gateway is configured",
                 bg="#EEF5FF", fg=COLORS["text_secondary"], font=FONTS["small"],
                 wraplength=360).pack(pady=(0, 9))

        tk.Label(card, text="ENTER OTP", bg=COLORS["surface"], fg=COLORS["text"],
                 font=FONTS["small_bold"]).pack(anchor="w", padx=28)
        otp_entry = tk.Entry(card, font=(FONTS["body"][0], 13), justify="center", relief="solid", bd=1)
        otp_entry.pack(fill="x", padx=28, pady=(6, 14), ipady=8)
        otp_entry.focus()

        def verify():
            entered = otp_entry.get().strip()
            if time.time() > self.activation_expires_at:
                messagebox.showerror("OTP Expired", "This temporary OTP has expired. Generate a new OTP.", parent=dialog)
                dialog.destroy()
                self.open_activation()
                return
            if entered != self.activation_otp:
                messagebox.showerror("Invalid OTP", "The OTP is incorrect. Please try again.", parent=dialog)
                otp_entry.delete(0, tk.END)
                otp_entry.focus()
                return
            try:
                self.bank_service.activate_account(self.activation_account["account_id"])
            except Exception as error:
                messagebox.showerror("Activation Failed", str(error), parent=dialog)
                return

            account_number = self.activation_account["account_number"]
            dialog.grab_release()
            dialog.destroy()
            self.activation_otp = None
            self.activation_account = None
            self.activation_expires_at = 0
            self.account_entry.delete(0, tk.END)
            self.account_entry.insert(0, account_number)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
            messagebox.showinfo(
                "Account Activated",
                f"Your account {account_number} is now ACTIVE.\n\nPlease enter your password and click LOGIN.",
                parent=self,
            )

        verify_btn = tk.Button(card, text="VERIFY OTP & ACTIVATE ACCOUNT", command=verify)
        button(verify_btn, "primary").pack(fill="x", padx=28, ipady=5)
        tk.Button(card, text="Cancel", command=dialog.destroy, relief="flat", bd=0,
                  bg=COLORS["surface"], fg=COLORS["text_secondary"], cursor="hand2").pack(pady=8)
        dialog.bind("<Return>", lambda event: verify())

    @staticmethod
    def mask_phone(phone):
        phone = str(phone)
        if len(phone) <= 4:
            return "*" * len(phone)
        return "*" * (len(phone) - 4) + phone[-4:]
