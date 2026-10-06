COLORS = {
    "primary": "#1F5EFF",
    "primary_dark": "#12213F",
    "primary_hover": "#1749C7",
    "primary_soft": "#EEF4FF",
    "background": "#F7F8FA",
    "surface": "#FFFFFF",
    "border": "#E5E7EB",
    "text": "#111827",
    "text_secondary": "#6B7280",
    "text_muted": "#9CA3AF",
    "success": "#15803D",
    "success_soft": "#ECFDF3",
    "danger": "#DC2626",
    "warning": "#B45309",
}
FONT = "Segoe UI"
FONTS = {
    "hero": (FONT, 28, "bold"),
    "page": (FONT, 22, "bold"),
    "section": (FONT, 15, "bold"),
    "card": (FONT, 11, "bold"),
    "body": (FONT, 10),
    "body_bold": (FONT, 10, "bold"),
    "small": (FONT, 9),
    "small_bold": (FONT, 9, "bold"),
    "balance": (FONT, 28, "bold"),
}
SPACE = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "xxl": 32}

def button(widget, kind="primary"):
    palette = {
        "primary": (COLORS["primary"], "#FFFFFF", COLORS["primary_hover"], "#FFFFFF"),
        "secondary": (COLORS["surface"], COLORS["primary"], "#F3F6FA", COLORS["primary"]),
        "ghost": (COLORS["surface"], COLORS["text"], "#F3F4F6", COLORS["text"]),
        "danger": (COLORS["surface"], COLORS["danger"], "#FEF2F2", COLORS["danger"]),
        "success": (COLORS["success"], "#FFFFFF", "#166534", "#FFFFFF"),
        "success_small": (COLORS["primary"], "#FFFFFF", COLORS["primary_hover"], "#FFFFFF"),
    }.get(kind, (COLORS["primary"], "#FFFFFF", COLORS["primary_hover"], "#FFFFFF"))
    widget.configure(
        relief="solid" if kind != "primary" else "flat",
        bd=1 if kind != "primary" else 0,
        cursor="hand2",
        font=FONTS["body_bold"],
        padx=14,
        pady=7,
        bg=palette[0],
        fg=palette[1],
        highlightthickness=0,
        activebackground=palette[2],
        activeforeground=palette[3],
    )
    return widget
