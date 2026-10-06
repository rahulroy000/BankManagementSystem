import tkinter as tk
from tkinter import ttk, messagebox

from services.transaction_service import TransactionService
from gui.theme import COLORS, FONTS, button


class Dashboard(tk.Frame):
    """Post-login MyBank dashboard with a prominent, live account-status section."""

    def __init__(self, parent, app, user_data):
        super().__init__(parent, bg=COLORS["background"])
        self.app = app
        self.user_data = user_data
        self.bank_service = app.bank_service
        self.transaction_service = TransactionService()
        self.balance_visible = True
        self.account_status = str(user_data.get("status", "ACTIVE")).upper()
        self.mobile_number = user_data.get("phone", "-") or "-"
        self.build()
        self.refresh_dashboard()

    def build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR ----------------
        sidebar = tk.Frame(
            self, bg=COLORS["surface"], width=245,
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar, text="MYBANK", bg=COLORS["surface"], fg=COLORS["text"],
            font=(FONTS["page"][0], 22, "bold")
        ).pack(anchor="w", padx=24, pady=(28, 2))
        tk.Label(
            sidebar, text="Personal Banking", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small"]
        ).pack(anchor="w", padx=25, pady=(0, 18))

        # Prominent active-account section requested by the user.
        self.sidebar_status = tk.Frame(
            sidebar, bg=COLORS["success_soft"],
            highlightbackground=COLORS["success"], highlightthickness=1
        )
        self.sidebar_status.pack(fill="x", padx=14, pady=(0, 18))
        self.sidebar_status_title = tk.Label(
            self.sidebar_status, text="● ACTIVE ACCOUNT", bg=COLORS["success_soft"],
            fg=COLORS["success"], font=FONTS["small_bold"]
        )
        self.sidebar_status_title.pack(anchor="w", padx=14, pady=(10, 2))
        self.sidebar_status_detail = tk.Label(
            self.sidebar_status, text="Account is ready for banking", bg=COLORS["success_soft"],
            fg=COLORS["text_secondary"], font=FONTS["small"]
        )
        self.sidebar_status_detail.pack(anchor="w", padx=14, pady=(0, 10))

        items = [
            ("Dashboard", lambda: None),
            ("Deposit", self.open_deposit),
            ("Withdraw", self.open_withdraw),
            ("Transfer", self.open_transfer),
            ("Transactions", self.app.show_transaction_history),
            ("Account", self.open_account_settings),
        ]
        for text, command in items:
            active = text == "Dashboard"
            b = tk.Button(
                sidebar, text=text, command=command, anchor="w", relief="flat", bd=0,
                bg=COLORS["primary_soft"] if active else COLORS["surface"],
                fg=COLORS["primary"] if active else COLORS["text_secondary"],
                activebackground=COLORS["primary_soft"], activeforeground=COLORS["primary"],
                font=FONTS["body_bold"] if active else FONTS["body"],
                cursor="hand2", padx=24, pady=10
            )
            b.pack(fill="x", padx=10, pady=2)

        tk.Frame(sidebar, bg=COLORS["surface"]).pack(fill="both", expand=True)
        logout = tk.Button(sidebar, text="Logout", command=self.app.logout, anchor="w")
        button(logout, "danger").pack(fill="x", padx=20, pady=20)

        # ---------------- MAIN ----------------
        main = tk.Frame(self, bg=COLORS["background"])
        main.grid(row=0, column=1, sticky="nsew", padx=34, pady=26)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(5, weight=1)

        header = tk.Frame(main, bg=COLORS["background"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        tk.Label(
            header, text=f"Hello, {self.user_data.get('full_name', 'Customer')}",
            bg=COLORS["background"], fg=COLORS["text"],
            font=(FONTS["page"][0], 23, "bold")
        ).pack(side="left")
        refresh = tk.Button(header, text="Refresh", command=self.refresh_dashboard)
        button(refresh, "secondary").pack(side="right")

        # Balance card.
        balance = tk.Frame(main, bg=COLORS["primary"])
        balance.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        balance.grid_columnconfigure(0, weight=1)
        tk.Label(
            balance, text="AVAILABLE BALANCE", bg=COLORS["primary"], fg="#DCE7FF",
            font=FONTS["small_bold"]
        ).grid(row=0, column=0, sticky="w", padx=26, pady=(18, 2))
        self.balance_label = tk.Label(balance, bg=COLORS["primary"], fg="#FFFFFF", font=FONTS["balance"])
        self.balance_label.grid(row=1, column=0, sticky="w", padx=26)
        self.meta = tk.Label(balance, bg=COLORS["primary"], fg="#DCE7FF", font=FONTS["small"])
        self.meta.grid(row=2, column=0, sticky="w", padx=26, pady=(3, 18))
        hide = tk.Button(
            balance, text="Show / Hide", command=self.toggle_balance, relief="flat", bd=0,
            bg=COLORS["primary"], fg="#FFFFFF", activebackground=COLORS["primary"],
            activeforeground="#FFFFFF", font=FONTS["small_bold"], cursor="hand2"
        )
        hide.grid(row=0, column=1, rowspan=3, padx=24)

        # ---------------- LIVE ACTIVE ACCOUNT SECTION ----------------
        account_card = tk.Frame(
            main, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        account_card.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        account_card.grid_columnconfigure(1, weight=1)
        account_card.grid_columnconfigure(3, weight=1)

        tk.Label(
            account_card, text="ACCOUNT STATUS", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small_bold"]
        ).grid(row=0, column=0, sticky="w", padx=(20, 8), pady=(12, 2))
        self.status_badge = tk.Label(
            account_card, text="● ACTIVE", bg=COLORS["success_soft"],
            fg=COLORS["success"], font=FONTS["body_bold"], padx=12, pady=5
        )
        self.status_badge.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

        tk.Label(
            account_card, text="REGISTERED MOBILE", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small_bold"]
        ).grid(row=0, column=1, sticky="w", padx=18, pady=(12, 2))
        self.mobile_value = tk.Label(
            account_card, text="-", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["body_bold"]
        )
        self.mobile_value.grid(row=1, column=1, sticky="w", padx=18, pady=(0, 12))

        tk.Label(
            account_card, text="ACCOUNT NUMBER", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small_bold"]
        ).grid(row=0, column=2, sticky="w", padx=18, pady=(12, 2))
        self.account_number_value = tk.Label(
            account_card, text="-", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["body_bold"]
        )
        self.account_number_value.grid(row=1, column=2, sticky="w", padx=18, pady=(0, 12))

        tk.Label(
            account_card, text="ACCOUNT TYPE", bg=COLORS["surface"],
            fg=COLORS["text_secondary"], font=FONTS["small_bold"]
        ).grid(row=0, column=3, sticky="w", padx=18, pady=(12, 2))
        self.account_type_value = tk.Label(
            account_card, text="-", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["body_bold"]
        )
        self.account_type_value.grid(row=1, column=3, sticky="w", padx=18, pady=(0, 12))

        # Quick actions.
        actions = tk.Frame(main, bg=COLORS["background"])
        actions.grid(row=3, column=0, sticky="ew", pady=(0, 17))
        tk.Label(actions, text="Quick actions", bg=COLORS["background"], fg=COLORS["text"], font=FONTS["section"]).pack(anchor="w", pady=(0, 8))
        row = tk.Frame(actions, bg=COLORS["background"])
        row.pack(fill="x")
        for title, command in [
            ("Deposit", self.open_deposit),
            ("Withdraw", self.open_withdraw),
            ("Transfer", self.open_transfer),
            ("Transactions", self.app.show_transaction_history),
        ]:
            b = tk.Button(row, text=title, command=command)
            button(b, "secondary").pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Recent transactions.
        recent = tk.Frame(main, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        recent.grid(row=5, column=0, sticky="nsew")
        recent.grid_columnconfigure(0, weight=1)
        recent.grid_rowconfigure(1, weight=1)
        top = tk.Frame(recent, bg=COLORS["surface"])
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=13)
        tk.Label(top, text="Recent transactions", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["card"]).pack(side="left")
        tk.Button(
            top, text="View all", command=self.app.show_transaction_history, relief="flat", bd=0,
            bg=COLORS["surface"], fg=COLORS["primary"], activebackground=COLORS["surface"],
            font=FONTS["small_bold"], cursor="hand2"
        ).pack(side="right")
        self.tree = ttk.Treeview(recent, columns=("date", "type", "amount", "description"), show="headings", height=6)
        for col, title, width in [
            ("date", "Date", 150), ("type", "Type", 130),
            ("amount", "Amount", 110), ("description", "Description", 300)
        ]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="w")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

    def update_account_section(self):
        active = self.account_status == "ACTIVE"
        color = COLORS["success"] if active else COLORS["danger"]
        soft = COLORS["success_soft"] if active else COLORS.get("danger_soft", "#FDECEC")
        label = "ACTIVE" if active else self.account_status

        self.status_badge.config(text=f"● {label}", fg=color, bg=soft)
        self.sidebar_status.config(bg=soft, highlightbackground=color)
        self.sidebar_status_title.config(text=f"● {label} ACCOUNT", fg=color, bg=soft)
        self.sidebar_status_detail.config(
            text="Account is ready for banking" if active else "Banking actions are unavailable",
            bg=soft
        )
        self.mobile_value.config(text=self.mobile_number)
        self.account_number_value.config(text=self.user_data.get("account_number", "-"))
        self.account_type_value.config(text=self.user_data.get("account_type", "-"))

    def update_balance(self):
        balance = float(self.user_data.get("balance", 0) or 0)
        self.balance_label.config(text=f"₹{balance:,.2f}" if self.balance_visible else "₹ ••••••")
        self.meta.config(text=f"{self.user_data.get('account_type', '')}  •  A/C {self.user_data.get('account_number', '')}")
        self.update_account_section()

    def toggle_balance(self):
        self.balance_visible = not self.balance_visible
        self.update_balance()

    def refresh_dashboard(self):
        try:
            con = self.bank_service.database.connect()
            try:
                row = con.execute(
                    "SELECT balance, status, account_number, account_type FROM accounts WHERE id = ?",
                    (self.user_data["account_id"],)
                ).fetchone()
                user_row = con.execute(
                    "SELECT phone FROM users WHERE id = ?", (self.user_data["user_id"],)
                ).fetchone()
            finally:
                con.close()

            if row:
                self.user_data["balance"] = row[0]
                self.account_status = str(row[1] or "INACTIVE").upper()
                self.user_data["account_number"] = row[2]
                self.user_data["account_type"] = row[3]
                self.user_data["status"] = self.account_status
            if user_row:
                self.mobile_number = user_row[0] or "-"
                self.user_data["phone"] = self.mobile_number

            self.update_balance()
            self.load_recent()
        except Exception as error:
            messagebox.showerror("Refresh Failed", str(error), parent=self)

    def require_active(self):
        if self.account_status != "ACTIVE":
            messagebox.showwarning(
                "Account Inactive",
                "This account is not active. Banking actions are unavailable.",
                parent=self
            )
            return False
        return True

    def load_recent(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = self.transaction_service.get_transactions(self.user_data["account_id"])
            for tx in rows[:6]:
                _, kind, amount, description, created = tx
                self.tree.insert("", tk.END, values=(created, kind, f"₹{amount:,.2f}", description))
        except Exception:
            pass

    def amount_dialog(self, mode):
        if not self.require_active():
            return
        win = tk.Toplevel(self)
        win.title(mode)
        win.geometry("390x310")
        win.resizable(False, False)
        win.configure(bg=COLORS["surface"])
        win.transient(self)
        win.grab_set()
        tk.Label(win, text=mode, bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["page"]).pack(pady=(28, 5))
        tk.Label(win, text="Enter amount", bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["body"]).pack()
        entry = tk.Entry(win, font=(FONTS["body"][0], 14), justify="center", relief="solid", bd=1)
        entry.pack(fill="x", padx=42, pady=14, ipady=8)
        entry.focus()
        quick = tk.Frame(win, bg=COLORS["surface"])
        quick.pack()
        for amount in (500, 1000, 5000):
            b = tk.Button(quick, text=f"₹{amount}", command=lambda a=amount: (entry.delete(0, tk.END), entry.insert(0, str(a))))
            button(b, "secondary").pack(side="left", padx=4)

        def submit():
            try:
                amount = float(entry.get().strip())
                if mode == "Deposit":
                    new_balance = self.bank_service.deposit(self.user_data["account_id"], amount)
                else:
                    new_balance = self.bank_service.withdraw(self.user_data["account_id"], amount)
                self.user_data["balance"] = new_balance
                self.refresh_dashboard()
                messagebox.showinfo("Success", f"₹{amount:,.2f} {mode.lower()}ed successfully.\n\nNew balance: ₹{new_balance:,.2f}", parent=win)
                win.destroy()
            except (ValueError, TypeError) as error:
                messagebox.showerror(f"{mode} Failed", str(error), parent=win)
            except Exception as error:
                messagebox.showerror("System Error", str(error), parent=win)

        b = tk.Button(win, text=mode.upper(), command=submit)
        button(b, "primary").pack(fill="x", padx=42, pady=18, ipady=3)

    def open_deposit(self):
        self.amount_dialog("Deposit")

    def open_withdraw(self):
        self.amount_dialog("Withdraw")

    def open_transfer(self):
        if not self.require_active():
            return

        win = tk.Toplevel(self)
        win.title("Transfer Money")
        win.geometry("460x430")
        win.resizable(False, False)
        win.configure(bg=COLORS["background"])
        win.transient(self.winfo_toplevel())
        win.grab_set()

        card = tk.Frame(
            win, bg=COLORS["surface"],
            highlightbackground=COLORS["border"], highlightthickness=1
        )
        card.pack(fill="both", expand=True, padx=18, pady=18)

        tk.Label(
            card, text="Transfer Money", bg=COLORS["surface"], fg=COLORS["text"],
            font=(FONTS["page"][0], 20, "bold")
        ).pack(anchor="w", padx=28, pady=(22, 4))
        tk.Label(
            card, text=f"Available balance: ₹{float(self.user_data.get('balance', 0) or 0):,.2f}",
            bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["body"]
        ).pack(anchor="w", padx=28, pady=(0, 18))

        tk.Label(
            card, text="RECIPIENT ACCOUNT NUMBER", bg=COLORS["surface"],
            fg=COLORS["text"], font=FONTS["small_bold"]
        ).pack(anchor="w", padx=28)
        recipient = tk.Entry(card, font=(FONTS["body"][0], 11), relief="solid", bd=1)
        recipient.pack(fill="x", padx=28, pady=(6, 15), ipady=7)

        tk.Label(
            card, text="TRANSFER AMOUNT", bg=COLORS["surface"],
            fg=COLORS["text"], font=FONTS["small_bold"]
        ).pack(anchor="w", padx=28)
        amount = tk.Entry(card, font=(FONTS["body"][0], 11), relief="solid", bd=1)
        amount.pack(fill="x", padx=28, pady=(6, 18), ipady=7)

        def submit_transfer():
            target = recipient.get().strip()
            raw_amount = amount.get().strip()
            if not target:
                messagebox.showwarning("Recipient Required", "Enter the recipient account number.", parent=win)
                recipient.focus()
                return
            try:
                value = float(raw_amount)
            except ValueError:
                messagebox.showwarning("Invalid Amount", "Enter a valid transfer amount.", parent=win)
                amount.focus()
                return
            if value <= 0:
                messagebox.showwarning("Invalid Amount", "Transfer amount must be greater than zero.", parent=win)
                amount.focus()
                return
            if not messagebox.askyesno(
                "Confirm Transfer",
                f"Transfer ₹{value:,.2f} to account {target}?",
                parent=win
            ):
                return
            try:
                new_balance = self.bank_service.transfer(
                    self.user_data["account_id"], target, value
                )
                self.user_data["balance"] = new_balance
                self.update_balance()
                self.load_recent()
                messagebox.showinfo(
                    "Transfer Successful",
                    f"₹{value:,.2f} was transferred successfully.",
                    parent=win
                )
                win.destroy()
            except Exception as error:
                messagebox.showerror("Transfer Failed", str(error), parent=win)

        send = tk.Button(card, text="TRANSFER", command=submit_transfer)
        button(send, "primary").pack(fill="x", padx=28, ipady=5)
        tk.Button(
            card, text="Cancel", command=win.destroy, relief="flat", bd=0,
            bg=COLORS["surface"], fg=COLORS["text_secondary"],
            font=FONTS["small_bold"], cursor="hand2"
        ).pack(pady=8)
        recipient.focus()

    def open_account_settings(self):
        win = tk.Toplevel(self)
        win.title("Account Management")
        win.geometry("520x430")
        win.resizable(False, False)
        win.configure(bg=COLORS["background"])
        win.transient(self)
        win.grab_set()

        card = tk.Frame(win, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=370)
        tk.Label(card, text="Account Management", bg=COLORS["surface"], fg=COLORS["text"], font=(FONTS["page"][0], 20, "bold")).pack(pady=(25, 5))
        tk.Label(card, text=f"Status: {self.account_status}\nMobile: {self.mobile_number}\nAccount: {self.user_data.get('account_number', '-')}", bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["body"], justify="center").pack(pady=10)
        tk.Label(card, text="Deactivate keeps your data but blocks login.\nDelete permanently removes the account and history (balance must be ₹0).", bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["small"], justify="center").pack(pady=8)
        if self.account_status == "ACTIVE":
            deactivate = tk.Button(card, text="DEACTIVATE ACCOUNT", command=lambda: self.deactivate_account(win))
            button(deactivate, "danger").pack(fill="x", padx=40, pady=(10, 8), ipady=4)
        delete = tk.Button(card, text="DELETE ACCOUNT", command=lambda: self.delete_account(win))
        button(delete, "danger").pack(fill="x", padx=40, pady=8, ipady=4)
        tk.Button(card, text="Cancel", command=win.destroy, relief="flat", bd=0, bg=COLORS["surface"], fg=COLORS["text_secondary"], font=FONTS["small_bold"], cursor="hand2").pack(pady=8)

    def deactivate_account(self, parent):
        if not messagebox.askyesno("Deactivate Account", "Deactivate this account? You will be logged out and cannot log in until it is reactivated.", parent=parent):
            return
        try:
            self.bank_service.deactivate_account(self.user_data["account_id"])
            messagebox.showinfo("Account Deactivated", "Your account is now INACTIVE. You will be logged out.", parent=parent)
            parent.destroy()
            self.app.logout()
        except Exception as error:
            messagebox.showerror("Deactivation Failed", str(error), parent=parent)

    def delete_account(self, parent):
        if float(self.user_data.get("balance", 0) or 0) != 0:
            messagebox.showerror("Cannot Delete", "Your balance must be ₹0 before the account can be deleted.", parent=parent)
            return
        if not messagebox.askyesno("Delete Account", "This permanently deletes your account, personal data and transaction history. Continue?", parent=parent):
            return
        confirm = tk.Toplevel(parent)
        confirm.title("Confirm Permanent Deletion")
        confirm.geometry("430x220")
        confirm.configure(bg=COLORS["surface"])
        confirm.transient(parent)
        confirm.grab_set()
        tk.Label(confirm, text="Type DELETE to confirm", bg=COLORS["surface"], fg=COLORS["text"], font=FONTS["section"]).pack(pady=(30, 8))
        entry = tk.Entry(confirm, justify="center", font=(FONTS["body"][0], 12), relief="solid", bd=1)
        entry.pack(fill="x", padx=55, ipady=7)

        def perform():
            if entry.get().strip() != "DELETE":
                messagebox.showerror("Confirmation Required", "Type DELETE exactly.", parent=confirm)
                return
            try:
                self.bank_service.delete_account(self.user_data["account_id"])
                messagebox.showinfo("Account Deleted", "Your account and associated data have been permanently deleted.", parent=confirm)
                confirm.destroy()
                parent.destroy()
                self.app.logout()
            except Exception as error:
                messagebox.showerror("Deletion Failed", str(error), parent=confirm)

        b = tk.Button(confirm, text="PERMANENTLY DELETE", command=perform)
        button(b, "danger").pack(fill="x", padx=55, pady=18, ipady=4)
