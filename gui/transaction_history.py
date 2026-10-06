from gui.theme import COLORS, FONTS, SPACE, button

import tkinter as tk
from tkinter import ttk, messagebox
from services.transaction_service import TransactionService


class TransactionHistory(tk.Frame):
    def __init__(self, parent, app, user_data):
        super().__init__(parent, bg="#f4f7fb")
        self.app = app
        self.user_data = user_data
        self.transaction_service = TransactionService()
        self.transactions = []
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="ALL")
        self._build()
        self.load_transactions()

    def _build(self):
        top = tk.Frame(self, bg="#f4f7fb")
        top.pack(fill="x", padx=30, pady=(25, 15))
        tk.Button(top, text="← Dashboard", command=self.go_back, relief="flat",
                  bg="#eaf2ff", fg="#1769e0", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", padx=12, pady=7).pack(side="left")
        tk.Label(top, text="Transaction History", bg="#f4f7fb", fg="#12213f",
                 font=("Segoe UI", 24, "bold")).pack(side="left", padx=18)

        tk.Label(self, text=f"Account • {self.user_data['account_number']}",
                 bg="#f4f7fb", fg="#667085", font=("Segoe UI", 10)).pack(anchor="w", padx=32)

        controls = tk.Frame(self, bg="white", highlightbackground="#e4e9f0", highlightthickness=1)
        controls.pack(fill="x", padx=30, pady=18, ipady=7)
        tk.Label(controls, text="Search", bg="white", fg="#344054",
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(15, 6))
        search = tk.Entry(controls, textvariable=self.search_var, relief="solid", bd=1, width=35)
        search.pack(side="left", ipady=6)
        search.bind("<KeyRelease>", lambda e: self.apply_filters())

        tk.Label(controls, text="Type", bg="white", fg="#344054",
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(20, 6))
        ttk.Combobox(controls, textvariable=self.filter_var,
                     values=("ALL", "DEPOSIT", "WITHDRAW", "INITIAL_DEPOSIT"),
                     state="readonly", width=18).pack(side="left")
        self.filter_var.trace_add("write", lambda *args: self.apply_filters())
        tk.Button(controls, text="Refresh", command=self.load_transactions, relief="flat",
                  bg="#eaf2ff", fg="#1769e0", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", padx=12, pady=6).pack(side="right", padx=12)

        table_card = tk.Frame(self, bg="white", highlightbackground="#e4e9f0", highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=30, pady=(0, 18))
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_card, columns=("date", "type", "amount", "description"), show="headings")
        for col, title, width in [("date", "Date", 180), ("type", "Transaction Type", 160),
                                  ("amount", "Amount", 130), ("description", "Description", 400)]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns", pady=12)
        self.tree.configure(yscrollcommand=scroll.set)

        bottom = tk.Frame(self, bg="#f4f7fb")
        bottom.pack(fill="x", padx=32, pady=(0, 15))
        self.total_label = tk.Label(bottom, text="", bg="#f4f7fb", fg="#667085",
                                    font=("Segoe UI", 9))
        self.total_label.pack(side="left")

    def load_transactions(self):
        try:
            self.transactions = self.transaction_service.get_transactions(self.user_data["account_id"])
            self.apply_filters()
        except Exception as error:
            messagebox.showerror("Error", f"Unable to load transactions:\n{error}", parent=self)

    def apply_filters(self):
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip().lower()
        kind = self.filter_var.get()
        visible = []
        for tx in self.transactions:
            _, tx_type, amount, description, created_at = tx
            if kind != "ALL" and tx_type != kind:
                continue
            haystack = f"{tx_type} {description} {created_at} {amount}".lower()
            if query and query not in haystack:
                continue
            visible.append(tx)
            self.tree.insert("", tk.END, values=(created_at, tx_type, f"₹{amount:,.2f}", description))

        self.total_label.config(text=f"Showing {len(visible)} of {len(self.transactions)} transactions")

    def go_back(self):
        self.app.show_dashboard(self.user_data)
