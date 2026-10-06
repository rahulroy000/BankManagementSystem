import tkinter as tk
from tkinter import ttk
from services.bank_service import BankService
from services.auth_service import AuthService
from gui.theme import COLORS, FONTS

class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyBank | Secure Banking")
        self.geometry("1180x720")
        self.minsize(980, 620)
        self.configure(bg=COLORS["background"])
        self.current_user = None
        self.bank_service = BankService()
        self.auth_service = AuthService()
        self.configure_style()
        self.container = tk.Frame(self, bg=COLORS["background"])
        self.container.pack(fill="both", expand=True)
        self.show_login()

    def configure_style(self):
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure(".", font=FONTS["body"], background=COLORS["background"], foreground=COLORS["text"])
        style.configure("Treeview", rowheight=38, font=FONTS["body"],
                        background=COLORS["surface"], fieldbackground=COLORS["surface"], foreground=COLORS["text"])
        style.configure("Treeview.Heading", font=FONTS["body_bold"],
                        background="#EEF3F9", foreground="#344054", relief="flat")
        style.map("Treeview", background=[("selected", "#DCE9FF")], foreground=[("selected", COLORS["text"])])
        style.configure("TCombobox", padding=7)

    def clear_screen(self):
        for widget in self.container.winfo_children(): widget.destroy()

    def show_login(self):
        self.clear_screen()
        from gui.login_window import LoginWindow
        LoginWindow(self.container, self).pack(fill="both", expand=True)

    def show_register(self):
        self.clear_screen()
        from gui.register_window import RegisterWindow
        RegisterWindow(self.container, self).pack(fill="both", expand=True)

    def show_dashboard(self, user_data):
        self.clear_screen()
        self.current_user = user_data
        from gui.dashboard import Dashboard
        Dashboard(self.container, self, user_data).pack(fill="both", expand=True)

    def show_transaction_history(self):
        self.clear_screen()
        from gui.transaction_history import TransactionHistory
        TransactionHistory(self.container, self, self.current_user).pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()
