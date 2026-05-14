import tkinter as tk
from tkinter import ttk
from styles import Styles


def create_menu_card(parent, text, command, icon, row, col):
    """创建菜单卡片"""
    card = tk.Frame(
        parent,
        bg=Styles.SURFACE_COLOR,
        highlightbackground=Styles.BORDER_COLOR,
        highlightthickness=1
    )
    card.grid(row=row, column=col, padx=Styles.SPACING_SM, pady=Styles.SPACING_SM, sticky="nsew")

    parent.grid_columnconfigure(col, weight=1)
    parent.grid_rowconfigure(row, weight=1)

    content = tk.Frame(card, bg=Styles.SURFACE_COLOR)
    content.pack(expand=True, padx=Styles.SPACING_LG, pady=Styles.SPACING_LG)

    icon_label = tk.Label(
        content,
        text=icon,
        font=("微软雅黑", 24),
        bg=Styles.SURFACE_COLOR,
        fg=Styles.PRIMARY_COLOR
    )
    icon_label.pack()

    text_label = tk.Label(
        content,
        text=text,
        font=("微软雅黑", 14),
        bg=Styles.SURFACE_COLOR,
        fg=Styles.TEXT_PRIMARY
    )
    text_label.pack(pady=(Styles.SPACING_XS, 0))

    def on_enter(e):
        card.config(highlightbackground=Styles.PRIMARY_COLOR, bg=Styles.BORDER_LIGHT)
        content.config(bg=Styles.BORDER_LIGHT)
        icon_label.config(bg=Styles.BORDER_LIGHT)
        text_label.config(bg=Styles.BORDER_LIGHT)

    def on_leave(e):
        card.config(highlightbackground=Styles.BORDER_COLOR, bg=Styles.SURFACE_COLOR)
        content.config(bg=Styles.SURFACE_COLOR)
        icon_label.config(bg=Styles.SURFACE_COLOR)
        text_label.config(bg=Styles.SURFACE_COLOR)

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    content.bind("<Enter>", on_enter)
    content.bind("<Leave>", on_leave)

    card.bind("<Button-1>", lambda e: command())
    content.bind("<Button-1>", lambda e: command())
    icon_label.bind("<Button-1>", lambda e: command())
    text_label.bind("<Button-1>", lambda e: command())


def clear_window(parent):
    """清空窗口"""
    for widget in parent.winfo_children():
        widget.destroy()


def create_page_header(parent, title, subtitle=None):
    """创建统一的页面标题区域"""
    header_frame = tk.Frame(parent, bg=Styles.BACKGROUND_COLOR)
    header_frame.pack(fill=tk.X, pady=(10, 5))

    title_label = tk.Label(
        header_frame,
        text=title,
        font=Styles.SUB_HEADER_FONT,
        bg=Styles.BACKGROUND_COLOR,
        fg=Styles.TEXT_PRIMARY
    )
    title_label.pack(anchor=tk.W)

    if subtitle:
        subtitle_label = tk.Label(
            header_frame,
            text=subtitle,
            font=Styles.LABEL_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))

    return header_frame


def create_back_button(parent, command):
    """创建返回按钮"""
    btn_frame = tk.Frame(parent, bg=Styles.BACKGROUND_COLOR)
    btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 10))

    btn = ttk.Button(
        btn_frame,
        text="← 返回主菜单",
        command=command,
        style="Secondary.TButton"
    )
    btn.pack(anchor=tk.W, padx=0)
    return btn


def create_button_grid(parent, buttons, columns=None):
    """创建统一的卡片式按钮网格

    Args:
        parent: 父容器
        buttons: 按钮列表，格式为 [(text, command, icon), ...]
        columns: 列数（自动判断如果为None）
    """
    button_grid = tk.Frame(parent, bg=Styles.BACKGROUND_COLOR)
    button_grid.pack(pady=10, fill=tk.BOTH, expand=True)

    num_buttons = len(buttons)
    if columns is None:
        if num_buttons <= 1:
            columns = 1
        elif num_buttons <= 2:
            columns = 2
        elif num_buttons <= 4:
            columns = 2
        elif num_buttons <= 6:
            columns = 3
        elif num_buttons <= 8:
            columns = 4
        else:
            columns = 4

    max_rows = (num_buttons + columns - 1) // columns
    for col in range(columns):
        button_grid.grid_columnconfigure(col, weight=1, uniform="column")
    for row in range(max_rows):
        button_grid.grid_rowconfigure(row, weight=1, uniform="row")

    for i, item in enumerate(buttons):
        if len(item) == 3:
            text, command, icon = item
        else:
            text, command = item
            icon = "📋"

        row = i // columns
        col = i % columns

        card = tk.Frame(
            button_grid,
            bg=Styles.SURFACE_COLOR,
            highlightbackground=Styles.BORDER_COLOR,
            highlightthickness=1
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        content_frame = tk.Frame(card, bg=Styles.SURFACE_COLOR)
        content_frame.pack(expand=True, fill=tk.BOTH)

        content = tk.Frame(content_frame, bg=Styles.SURFACE_COLOR)
        content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        content.grid_rowconfigure(0, weight=3)
        content.grid_rowconfigure(1, weight=2)
        content.grid_columnconfigure(0, weight=1)

        icon_label = tk.Label(
            content,
            text=icon,
            font=("微软雅黑", 36),
            bg=Styles.SURFACE_COLOR,
            fg=Styles.PRIMARY_COLOR,
            anchor=tk.CENTER,
            justify=tk.CENTER
        )
        icon_label.grid(row=0, column=0, sticky="nsew", pady=(5, 0))

        text_label = tk.Label(
            content,
            text=text,
            font=Styles.LABEL_FONT,
            bg=Styles.SURFACE_COLOR,
            fg=Styles.TEXT_PRIMARY,
            wraplength=160,
            justify=tk.CENTER
        )
        text_label.grid(row=1, column=0, sticky="n", pady=(5, 5))

        def make_on_enter(c=card, ct=content, il=icon_label, tl=text_label, cf=content_frame):
            def on_enter(e):
                c.config(highlightbackground=Styles.PRIMARY_COLOR, bg=Styles.BORDER_LIGHT)
                cf.config(bg=Styles.BORDER_LIGHT)
                ct.config(bg=Styles.BORDER_LIGHT)
                il.config(bg=Styles.BORDER_LIGHT)
                tl.config(bg=Styles.BORDER_LIGHT)
            return on_enter

        def make_on_leave(c=card, ct=content, il=icon_label, tl=text_label, cf=content_frame):
            def on_leave(e):
                c.config(highlightbackground=Styles.BORDER_COLOR, bg=Styles.SURFACE_COLOR)
                cf.config(bg=Styles.SURFACE_COLOR)
                ct.config(bg=Styles.SURFACE_COLOR)
                il.config(bg=Styles.SURFACE_COLOR)
                tl.config(bg=Styles.SURFACE_COLOR)
            return on_leave

        on_enter = make_on_enter()
        on_leave = make_on_leave()

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        text_label.bind("<Enter>", on_enter)
        text_label.bind("<Leave>", on_leave)

        def make_click(cmd=command):
            def click(e):
                cmd()
            return click

        click_handler = make_click()

        card.bind("<Button-1>", click_handler)
        content_frame.bind("<Button-1>", click_handler)
        content.bind("<Button-1>", click_handler)
        icon_label.bind("<Button-1>", click_handler)
        text_label.bind("<Button-1>", click_handler)

    return button_grid