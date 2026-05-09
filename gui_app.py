
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tea_inventory_system import TeaInventorySystem
from backup_manager import BackupManager
from operation_logger import OperationLogger
from cloud_sync import CloudSyncManager
from config_manager import ConfigManager
import pandas as pd
from prettytable import PrettyTable
from datetime import datetime

from styles import Styles
from views.product_view import ProductViewMixin
from views.sales_view import SalesViewMixin
from views.purchase_view import PurchaseViewMixin
from views.supplier_view import SupplierViewMixin
from views.customer_view import CustomerViewMixin
from views.stats_view import StatsViewMixin
from views.settings_view import SettingsViewMixin


class TeaInventoryGUI(ProductViewMixin, SalesViewMixin, PurchaseViewMixin, SupplierViewMixin, CustomerViewMixin, StatsViewMixin, SettingsViewMixin):
    """茶叶进销存管理系统图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("茶叶进销存管理系统——狗拿耗子")
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 加载主窗口保存的大小
        win_width, win_height = self.config_manager.load_window_size(
            "main_window", 
            Styles.WINDOW_WIDTH, 
            Styles.WINDOW_HEIGHT
        )
        self.root.geometry(f"{win_width}x{win_height}")
        self.root.configure(bg=Styles.BACKGROUND_COLOR)
        
        # 绑定主窗口关闭事件，保存窗口大小
        self.root.protocol("WM_DELETE_WINDOW", self._on_main_window_close)
        
        self.system = TeaInventorySystem()
        
        # 初始化备份管理器、日志记录器和云同步管理器
        self.backup_manager = BackupManager()
        self.operation_logger = OperationLogger()
        self.cloud_sync_manager = CloudSyncManager()

        # 创建全局样式
        self.style = ttk.Style()
        self._configure_styles()

        self.create_main_menu()
    
    def _on_main_window_close(self):
        """主窗口关闭时保存窗口大小"""
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            self.config_manager.save_window_size("main_window", width, height)
        except Exception as e:
            print(f"保存主窗口大小失败: {e}")
        self.root.destroy()
    
    def _create_toplevel_with_size(self, window_id: str, size_category: str = "medium", parent=None, modal: bool = False) -> tk.Toplevel:
        """创建带大小记忆和居中定位的Toplevel窗口

        Args:
            window_id: 窗口唯一标识符
            size_category: 尺寸分类 (large/medium/small)
            parent: 父窗口（默认为self.root）
            modal: 是否为模态窗口

        Returns:
            Toplevel窗口对象
        """
        if parent is None:
            parent = self.root
        top = tk.Toplevel(parent)

        default_w, default_h = Styles.WINDOW_SIZES.get(size_category, (800, 550))
        width, height = self.config_manager.load_window_size(window_id, default_w, default_h)

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        top.geometry(f"{width}x{height}+{x}+{y}")
        top.resizable(True, True)

        if modal:
            top.transient(parent)
            top.grab_set()

        def on_close():
            try:
                w = top.winfo_width()
                h = top.winfo_height()
                self.config_manager.save_window_size(window_id, w, h)
            except Exception as e:
                pass
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_close)

        return top

    def _configure_styles(self):
        """配置ttk控件样式 - 生产级现代化设计"""
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure("Modern.TButton", 
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=Styles.PRIMARY_COLOR,
                            foreground="white",
                            borderwidth=0,
                            relief="flat",
                            focuscolor=Styles.PRIMARY_COLOR)
        self.style.map("Modern.TButton", 
                      background=[("active", Styles.PRIMARY_DARK),
                                 ("pressed", Styles.PRIMARY_DARK),
                                 ("!disabled", Styles.PRIMARY_COLOR)],
                      foreground=[("!disabled", "white")],
                      relief=[("pressed", "flat"),
                              ("!pressed", "flat")])
        
        # 配置次要按钮
        self.style.configure("Secondary.TButton", 
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=Styles.SURFACE_COLOR,
                            foreground=Styles.TEXT_PRIMARY,
                            borderwidth=1,
                            relief="flat",
                            focuscolor=Styles.SURFACE_COLOR)
        self.style.map("Secondary.TButton", 
                      background=[("active", Styles.BORDER_LIGHT),
                                 ("pressed", Styles.BORDER_COLOR),
                                 ("!disabled", Styles.SURFACE_COLOR)],
                      foreground=[("!disabled", Styles.TEXT_PRIMARY)],
                      relief=[("pressed", "flat"),
                              ("!pressed", "flat")])
        
        # 配置成功按钮
        self.style.configure("Success.TButton", 
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=Styles.SUCCESS_COLOR,
                            foreground="white",
                            borderwidth=0,
                            relief="flat")
        self.style.map("Success.TButton", 
                      background=[("active", Styles.SUCCESS_COLOR),
                                 ("pressed", Styles.SECONDARY_DARK),
                                 ("!disabled", Styles.SUCCESS_COLOR)],
                      foreground=[("!disabled", "white")])
        
        # 配置危险按钮
        self.style.configure("Danger.TButton", 
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=Styles.ERROR_COLOR,
                            foreground="white",
                            borderwidth=0,
                            relief="flat")
        self.style.map("Danger.TButton", 
                      background=[("active", "#DC2626"),
                                 ("pressed", "#B91C1C"),
                                 ("!disabled", Styles.ERROR_COLOR)],
                      foreground=[("!disabled", "white")])
        
        # 配置标签样式
        self.style.configure("TLabel", 
                            font=Styles.LABEL_FONT,
                            background=Styles.BACKGROUND_COLOR,
                            foreground=Styles.TEXT_PRIMARY)
        
        # 配置标题标签
        self.style.configure("Title.TLabel", 
                            font=Styles.TITLE_FONT,
                            background=Styles.BACKGROUND_COLOR,
                            foreground=Styles.TEXT_PRIMARY)
        
        # 配置输入框样式
        self.style.configure("TEntry", 
                            font=Styles.TEXT_FONT,
                            padding=(10, 8),
                            fieldbackground=Styles.SURFACE_COLOR,
                            foreground=Styles.TEXT_PRIMARY,
                            borderwidth=1,
                            relief="solid")
        self.style.map("TEntry",
                      fieldbackground=[("focus", Styles.SURFACE_COLOR)],
                      bordercolor=[("focus", Styles.PRIMARY_COLOR)])
        
        # 配置树状表格样式
        self.style.configure("Treeview", 
                            font=Styles.TEXT_FONT,
                            background=Styles.SURFACE_COLOR,
                            foreground=Styles.TEXT_PRIMARY,
                            rowheight=32,
                            borderwidth=0,
                            relief="flat")
        self.style.configure("Treeview.Heading", 
                            font=Styles.LABEL_FONT,
                            background=Styles.BACKGROUND_COLOR,
                            foreground=Styles.TEXT_SECONDARY,
                            borderwidth=1,
                            relief="flat")
        self.style.map("Treeview", 
                      background=[("selected", Styles.PRIMARY_COLOR)],
                      foreground=[("selected", "white")])
        self.style.map("Treeview.Heading",
                      background=[("active", Styles.BORDER_LIGHT)])
        
        # 配置框架样式
        self.style.configure("Card.TFrame",
                            background=Styles.SURFACE_COLOR,
                            relief="flat",
                            borderwidth=0)
        
        # 配置分隔线
        self.style.configure("TSeparator",
                            background=Styles.BORDER_COLOR)

    def create_main_menu(self):
        """创建主菜单 - 卡片式现代化设计"""
        self.clear_window()
        
        # 恢复窗口高度到原始大小
        self.root.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")

        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_LG, pady=Styles.SPACING_LG)

        # 顶部标题区域
        header_frame = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, Styles.SPACING_LG))

        # 主标题
        title_label = tk.Label(
            header_frame,
            text="茶叶进销存管理系统",
            font=("微软雅黑", 22, "bold"),
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_PRIMARY
        )
        title_label.pack(anchor=tk.W)

        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="狗拿耗子工作室 · 专业库存管理解决方案",
            font=Styles.LABEL_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor=tk.W, pady=(Styles.SPACING_SM, 0))

        # 卡片网格
        card_grid = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        card_grid.pack(fill=tk.BOTH, expand=True)

        buttons = [
            ("商品管理", self.product_management, "📦"),
            ("销售功能", self.sales_management, "💰"),
            ("进货管理", self.stock_management, "📥"),
            ("供应商管理", self.supplier_management, "🤝"),
            ("客户管理", self.customer_management, "👥"),
            ("销售记录管理", self.sales_record_management, "📋"),
            ("统计分析", self.statistics_analysis, "📊"),
            ("系统管理", self.system_management, "⚙️")
        ]

        # 创建3列网格
        for i, (text, command, icon) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            self._create_menu_card(card_grid, text, command, icon, row, col)

        # 底部版权信息
        footer_frame = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        footer_frame.pack(fill=tk.X, pady=(Styles.SPACING_MD, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2026 茶叶进销存管理系统——狗拿耗子",
            font=Styles.TEXT_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_MUTED
        )
        footer_label.pack(anchor=tk.CENTER)

    def _create_menu_card(self, parent, text, command, icon, row, col):
        """创建菜单卡片"""
        card = tk.Frame(
            parent,
            bg=Styles.SURFACE_COLOR,
            highlightbackground=Styles.BORDER_COLOR,
            highlightthickness=1
        )
        card.grid(row=row, column=col, padx=Styles.SPACING_SM, pady=Styles.SPACING_SM, sticky="nsew")
        
        # 使卡片可伸缩
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        # 卡片内容
        content = tk.Frame(card, bg=Styles.SURFACE_COLOR)
        content.pack(expand=True, padx=Styles.SPACING_LG, pady=Styles.SPACING_LG)
        
        # 图标
        icon_label = tk.Label(
            content,
            text=icon,
            font=("微软雅黑", 24),
            bg=Styles.SURFACE_COLOR,
            fg=Styles.PRIMARY_COLOR
        )
        icon_label.pack()
        
        # 文本
        text_label = tk.Label(
            content,
            text=text,
            font=("微软雅黑", 14),
            bg=Styles.SURFACE_COLOR,
            fg=Styles.TEXT_PRIMARY
        )
        text_label.pack(pady=(Styles.SPACING_XS, 0))
        
        # 悬停效果
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
        
        # 点击事件
        card.bind("<Button-1>", lambda e: command())
        content.bind("<Button-1>", lambda e: command())
        icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())

    def clear_window(self):
        """清空窗口"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _create_page_header(self, parent, title, subtitle=None):
        """创建统一的页面标题区域"""
        header_frame = tk.Frame(parent, bg=Styles.BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, pady=(10, 5))
        
        # 标题
        title_label = tk.Label(
            header_frame,
            text=title,
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_PRIMARY
        )
        title_label.pack(anchor=tk.W)
        
        # 副标题（可选）
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

    def _create_back_button(self, parent, command):
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

    def _create_button_grid(self, parent, buttons, columns=None):
        """创建统一的卡片式按钮网格
        
        Args:
            parent: 父容器
            buttons: 按钮列表，格式为 [(text, command, icon), ...]
            columns: 列数（自动判断如果为None）
        """
        button_grid = tk.Frame(parent, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # 智能判断列数 - 更合理的分布
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
        
        # 先配置所有列和行的weight，确保均匀分布
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
            
            # 创建卡片
            card = tk.Frame(
                button_grid,
                bg=Styles.SURFACE_COLOR,
                highlightbackground=Styles.BORDER_COLOR,
                highlightthickness=1
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # 卡片内容容器
            content_frame = tk.Frame(card, bg=Styles.SURFACE_COLOR)
            content_frame.pack(expand=True, fill=tk.BOTH)
            
            # 卡片内容 - 使用grid居中
            content = tk.Frame(content_frame, bg=Styles.SURFACE_COLOR)
            content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            content_frame.grid_rowconfigure(0, weight=1)
            content_frame.grid_columnconfigure(0, weight=1)
            
            # 配置 content 的行和列权重
            content.grid_rowconfigure(0, weight=3)
            content.grid_rowconfigure(1, weight=2)
            content.grid_columnconfigure(0, weight=1)
            
            # 图标 - 更小更紧凑
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
            
            # 文本 - 更紧凑
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
            
            # 使用默认参数绑定当前值
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
            
            # 点击事件 - 同样用默认参数
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

    def _select_product_dialog(self, target_var):
        """商品选择弹窗 - 双击选择商品
        
        Args:
            target_var: 要填充的StringVar变量
        """
        df = self.system.excel_manager.get_all_commodities()
        
        top = self._create_toplevel_with_size("select_product", "large")
        top.title("选择商品")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame,
            text="选择商品（双击选择）",
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()
        
        if df.empty:
            tk.Label(top, text="暂无商品数据", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
            
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            
            btn_add = tk.Button(btn_frame, text="手动添加商品", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=lambda: [top.destroy(), self.add_product_gui()],
                               bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            btn_add.bind("<Enter>", lambda e, b=btn_add: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn_add.bind("<Leave>", lambda e, b=btn_add: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                                   width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                                   command=top.destroy,
                                   bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            return
        
        list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        list_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(list_frame, style="Treeview", show="headings")
        tree["columns"] = ("商品编号", "商品名称", "茶类", "品种", "当前库存", "零售价")
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(
                row['商品编号'],
                row['商品名称'],
                row['茶类'],
                row['品种'],
                row['当前库存'],
                row['零售价']
            ))
        
        def on_double_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                com_id = item['values'][0]
                target_var.set(com_id)
                top.destroy()
        
        tree.bind('<Double-1>', on_double_click)
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_add = tk.Button(btn_frame, text="手动添加商品", font=Styles.BUTTON_FONT,
                           width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                           command=lambda: [top.destroy(), self.add_product_gui()],
                           bg=Styles.SECONDARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=top.destroy,
                               bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
    
    def _select_supplier_dialog(self, target_var):
        """供应商选择弹窗 - 双击选择供应商
        
        Args:
            target_var: 要填充的StringVar变量
        """
        df = self.system.excel_manager.get_all_suppliers()
        
        top = self._create_toplevel_with_size("select_supplier", "large")
        top.title("选择供应商")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame,
            text="选择供应商（双击选择）",
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()
        
        if df.empty:
            tk.Label(top, text="暂无供应商数据", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
            
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            
            btn_add = tk.Button(btn_frame, text="手动添加供应商", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=lambda: [top.destroy(), self.add_supplier_gui()],
                               bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            btn_add.bind("<Enter>", lambda e, b=btn_add: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn_add.bind("<Leave>", lambda e, b=btn_add: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                                   width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                                   command=top.destroy,
                                   bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            return
        
        list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        list_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(list_frame, style="Treeview", show="headings")
        tree["columns"] = ("供应商编号", "供应商名称", "联系电话", "地址", "累计交易金额")
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(
                row.get('供应商编号', ''),
                row.get('供应商名称', ''),
                '' if pd.isna(row.get('联系电话')) else row.get('联系电话', ''),
                '' if pd.isna(row.get('地址')) else row.get('地址', ''),
                row.get('累计交易金额', 0) if pd.notna(row.get('累计交易金额')) else 0
            ))
        
        def on_double_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                supplier_name = item['values'][1]
                target_var.set(supplier_name)
                top.destroy()
        
        tree.bind('<Double-1>', on_double_click)
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_add = tk.Button(btn_frame, text="手动添加供应商", font=Styles.BUTTON_FONT,
                           width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                           command=lambda: [top.destroy(), self.add_supplier_gui()],
                           bg=Styles.SECONDARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=top.destroy,
                               bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
    
    def _select_customer_dialog(self, target_var):
        """客户选择弹窗 - 双击选择客户
        
        Args:
            target_var: 要填充的StringVar变量
        """
        df = self.system.excel_manager.get_all_customers()
        
        top = self._create_toplevel_with_size("select_customer", "large")
        top.title("选择客户")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame,
            text="选择客户（双击选择）",
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()
        
        if df.empty:
            tk.Label(top, text="暂无客户数据", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
            
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            
            btn_add = tk.Button(btn_frame, text="手动添加客户", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=lambda: [top.destroy(), self.add_customer_gui()],
                               bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            btn_add.bind("<Enter>", lambda e, b=btn_add: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn_add.bind("<Leave>", lambda e, b=btn_add: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                                   width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                                   command=top.destroy,
                                   bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            return
        
        list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        list_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(list_frame, style="Treeview", show="headings")
        tree["columns"] = ("客户编号", "客户名称", "联系电话", "地址", "累计消费")
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(
                row.get('客户编号', ''),
                row.get('客户名称', ''),
                '' if pd.isna(row.get('联系电话')) else row.get('联系电话', ''),
                '' if pd.isna(row.get('地址')) else row.get('地址', ''),
                row.get('累计消费', 0) if pd.notna(row.get('累计消费')) else 0
            ))
        
        def on_double_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                customer_name = item['values'][1]
                target_var.set(customer_name)
                top.destroy()
        
        tree.bind('<Double-1>', on_double_click)
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_add = tk.Button(btn_frame, text="手动添加客户", font=Styles.BUTTON_FONT,
                           width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                           command=lambda: [top.destroy(), self.add_customer_gui()],
                           bg=Styles.SECONDARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                               width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                               command=top.destroy,
                               bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
    
    def show_dataframe_window(self, df, title):
        """显示DataFrame的窗口（带分页功能）"""
        # 基于标题生成窗口ID（替换特殊字符）
        window_id = "dataframe_" + title.replace(" ", "_").replace("（", "").replace("）", "").replace("-", "_")
        top = self._create_toplevel_with_size(window_id, "large")
        top.title(title)
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        PAGE_SIZE = 100
        total_rows = len(df)
        total_pages = (total_rows + PAGE_SIZE - 1) // PAGE_SIZE
        current_page_var = tk.IntVar(value=1)

        # 打印数据信息
        print(f"show_dataframe_window: 标题={title}, 行数={len(df)}, 列数={len(df.columns)}, 是否为空={df.empty}")
        if not df.empty:
            print(f"列名: {list(df.columns)}")
            print(f"前5行数据:")
            print(df.head())

        if df.empty:
            # 居中显示无数据提示
            frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            frame.pack(expand=True, fill=tk.BOTH)
            
            tk.Label(
                frame, 
                text="暂无数据", 
                font=Styles.SUB_HEADER_FONT,
                bg=Styles.BACKGROUND_COLOR,
                fg=Styles.TEXT_COLOR
            ).pack(expand=True)
            
            # 添加关闭按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            
            tk.Button(
                btn_frame, 
                text="关闭", 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=top.destroy,
                bg=Styles.ERROR_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            ).pack()
            return

        # 创建标题栏（包含分页信息）
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text=title, 
            font=Styles.LABEL_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)

        # 确保列名是字符串类型
        df.columns = [str(col) for col in df.columns]
        
        # 如果是销售记录表格，将销售数量统一转换为斤为单位
        if '销售单位' in df.columns and '销售数量' in df.columns:
            df = df.copy()  # 创建副本以避免修改原始数据
            for idx, row in df.iterrows():
                if row['销售单位'] == '克' and pd.notna(row['销售数量']):
                    # 将克转换为斤
                    df.at[idx, '销售数量'] = row['销售数量'] / 500
                    df.at[idx, '销售单位'] = '斤'
        
        # 实收金额保留一位小数
        if '实收金额' in df.columns:
            df = df.copy()
            for idx, row in df.iterrows():
                val = row['实收金额']
                if pd.notna(val):
                    try:
                        df.at[idx, '实收金额'] = round(float(val), 1)
                    except:
                        pass
        
        # 创建表格区域
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        # 创建树状表格
        tree = ttk.Treeview(table_frame, style="Treeview")
        columns = list(df.columns)
        tree["columns"] = columns
        tree["show"] = "headings"

        # 配置列宽 - 扩展支持所有可能的列名
        column_widths = {
            '茶类': 100,
            '品种': 120,
            '商品编号': 100,
            '商品名称': 150,
            '销售数量(斤)': 100,
            '实收金额': 100,
            '销售成本': 100,
            '利润': 100,
            '利润率(%)': 100,
            '日期': 120,
            '日': 100,
            '周': 120,
            '月': 100,
            '供应商编号': 100,
            '供应商名称': 150,
            '联系人': 100,
            '联系电话': 120,
            '客户编号': 100,
            '客户名称': 150,
            '累计消费': 100,
            '客户等级': 100,
            '销售编号': 120,
            '进货编号': 120,
            '销售日期': 120,
            '进货日期': 120,
            '销售单位': 80,
            '进货单位': 80,
            '公司': 120,
            '产区': 100,
            '规格': 80,
            '成本价': 80,
            '零售价': 80,
            '生产日期': 100,
            '保质期(月)': 90,
            '当前库存': 90,
            '品质特征': 150,
            '年份': 60,
            '等级': 60,
            '单位': 60,
            '销售数量': 90,
            '进货数量': 90,
            '单价': 80,
            '进货单价': 90,
            '应收金额': 100,
            '供应商': 120,
            '地址': 150,
            '备注': 120,
            '电子邮箱': 150,
            '订单数': 80,
            '最后购买日期': 120,
            '创建日期': 120,
            '是否作废': 80,
            '预警级别': 90,
            '过期日期': 120,
            '剩余天数': 90
        }

        for col in columns:
            tree.heading(col, text=str(col))
            width = column_widths.get(str(col), 120)
            tree.column(col, width=width, anchor=tk.CENTER)

        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        
        tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        # 布局控件
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 定义加载数据函数
        def load_page(page_num):
            """加载指定页的数据"""
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)
            
            # 计算当前页的起始和结束索引
            start_idx = (page_num - 1) * PAGE_SIZE
            end_idx = min(start_idx + PAGE_SIZE, total_rows)
            
            # 获取当前页数据
            page_df = df.iloc[start_idx:end_idx]
            
            # 批量插入数据
            for _, row in page_df.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    if pd.isna(val):
                        values.append("")
                    elif col == "实收金额":
                        # 实收金额保留一位小数
                        try:
                            num_val = float(val)
                            values.append(f"{num_val:.1f}")
                        except:
                            values.append(str(val))
                    else:
                        values.append(str(val))
                tree.insert("", tk.END, values=values)
            
            # 更新页码信息
            page_info_label.config(text=f"第 {page_num} / {total_pages} 页 (共 {total_rows} 条记录)")
            
            # 更新按钮状态
            prev_btn.config(state=tk.NORMAL if page_num > 1 else tk.DISABLED)
            next_btn.config(state=tk.NORMAL if page_num < total_pages else tk.DISABLED)
            first_btn.config(state=tk.NORMAL if page_num > 1 else tk.DISABLED)
            last_btn.config(state=tk.NORMAL if page_num < total_pages else tk.DISABLED)
        
        # 定义翻页函数
        def go_first():
            current_page_var.set(1)
            load_page(1)
        
        def go_prev():
            current = current_page_var.get()
            if current > 1:
                current_page_var.set(current - 1)
                load_page(current - 1)
        
        def go_next():
            current = current_page_var.get()
            if current < total_pages:
                current_page_var.set(current + 1)
                load_page(current + 1)
        
        def go_last():
            current_page_var.set(total_pages)
            load_page(total_pages)
        
        # 创建分页控制区域（仅在多页时显示）
        if total_pages > 1:
            pagination_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            pagination_frame.pack(pady=Styles.PADY_SMALL)
            
            # 首页按钮
            first_btn = tk.Button(pagination_frame, text="首页", font=Styles.TEXT_FONT,
                               command=go_first, bg=Styles.PRIMARY_COLOR, fg="white",
                               relief=tk.FLAT, padx=10, pady=3)
            first_btn.pack(side=tk.LEFT, padx=5)
            
            # 上一页按钮
            prev_btn = tk.Button(pagination_frame, text="上一页", font=Styles.TEXT_FONT,
                              command=go_prev, bg=Styles.PRIMARY_COLOR, fg="white",
                              relief=tk.FLAT, padx=10, pady=3)
            prev_btn.pack(side=tk.LEFT, padx=5)
            
            # 页码信息标签
            page_info_label = tk.Label(pagination_frame, text="", 
                                      font=Styles.LABEL_FONT,
                                      bg=Styles.BACKGROUND_COLOR,
                                      fg=Styles.TEXT_COLOR)
            page_info_label.pack(side=tk.LEFT, padx=20)
            
            # 下一页按钮
            next_btn = tk.Button(pagination_frame, text="下一页", font=Styles.TEXT_FONT,
                              command=go_next, bg=Styles.PRIMARY_COLOR, fg="white",
                              relief=tk.FLAT, padx=10, pady=3)
            next_btn.pack(side=tk.LEFT, padx=5)
            
            # 末页按钮
            last_btn = tk.Button(pagination_frame, text="末页", font=Styles.TEXT_FONT,
                               command=go_last, bg=Styles.PRIMARY_COLOR, fg="white",
                               relief=tk.FLAT, padx=10, pady=3)
            last_btn.pack(side=tk.LEFT, padx=5)
            
            # 加载第一页数据
            load_page(1)
        else:
            # 单页时直接加载全部数据
            # 批量插入数据
            for _, row in df.iterrows():
                values = []
                for col in columns:
                    val = row[col]
                    if pd.isna(val):
                        values.append("")
                    else:
                        values.append(str(val))
                tree.insert("", tk.END, values=values)

        # 添加双击事件，双击查看详情
        def show_detail(e):
            """显示选中条目的详细信息"""
            selected = tree.selection()
            if not selected:
                return
            
            item = tree.item(selected[0])
            values = item['values']
            
            # 确定表格类型并获取相应的ID
            if '商品编号' in columns:
                # 商品表格
                com_id_idx = columns.index('商品编号')
                com_id = values[com_id_idx]
                
                commodity = self.system.excel_manager.get_commodity_by_id(com_id)
                if commodity is not None:
                    info_top = self._create_toplevel_with_size("dataframe_product_detail", "medium", parent=top)
                    info_top.title("商品详情")
                    info_top.configure(bg=Styles.BACKGROUND_COLOR)
                    info_top.resizable(True, True)
                    
                    frame = tk.Frame(info_top, bg=Styles.BACKGROUND_COLOR)
                    frame.pack(pady=Styles.PADY_LARGE, padx=Styles.PADX_LARGE)
                    
                    for i, (key, value) in enumerate(commodity.items()):
                        row_frame = tk.Frame(frame, bg=Styles.BACKGROUND_COLOR)
                        row_frame.pack(fill=tk.X, pady=5)
                        
                        tk.Label(row_frame, text=f"{key}:", 
                                font=Styles.LABEL_FONT,
                                bg=Styles.BACKGROUND_COLOR,
                                fg=Styles.HEADER_COLOR,
                                width=15, anchor=tk.W).pack(side=tk.LEFT)
                        
                        tk.Label(row_frame, text=str(value) if pd.notna(value) else "",
                                font=Styles.TEXT_FONT,
                                bg=Styles.BACKGROUND_COLOR,
                                fg=Styles.TEXT_COLOR,
                                anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    tk.Button(info_top, text="关闭", 
                             font=Styles.BUTTON_FONT,
                             width=Styles.BUTTON_WIDTH,
                             height=Styles.BUTTON_HEIGHT,
                             command=info_top.destroy,
                             bg=Styles.ERROR_COLOR,
                             fg="white",
                             relief=tk.FLAT,
                             padx=10,
                             pady=5).pack(pady=Styles.PADY_MEDIUM)
            
            elif '供应商编号' in columns:
                # 供应商表格 - 双击直接进入修改界面
                supplier_id_idx = columns.index('供应商编号')
                supplier_id = values[supplier_id_idx]
                
                df = self.system.excel_manager.get_all_suppliers()
                if not df.empty:
                    supplier = df[df['供应商编号'] == supplier_id]
                    if not supplier.empty:
                        supplier_row = supplier.iloc[0]
                        
                        # 创建修改窗口
                        edit_top = self._create_toplevel_with_size("dataframe_edit_supplier", "medium", parent=top)
                        edit_top.title("修改供应商信息")
                        edit_top.configure(bg=Styles.BACKGROUND_COLOR)
                        edit_top.resizable(True, True)
                        
                        # 创建标题区域
                        edit_title_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        edit_title_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        tk.Label(
                            edit_title_frame, 
                            text="修改供应商信息", 
                            font=Styles.SUB_HEADER_FONT,
                            bg=Styles.BACKGROUND_COLOR,
                            fg=Styles.HEADER_COLOR
                        ).pack()
                        
                        form_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        form_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        # 创建变量
                        vars = {}
                        fields = [
                            ("供应商名称", "供应商名称", supplier_row['供应商名称']),
                            ("联系人", "联系人", supplier_row['联系人']),
                            ("联系电话", "联系电话", supplier_row['联系电话']),
                            ("地址", "地址", supplier_row['地址']),
                            ("备注", "备注", supplier_row['备注'])
                        ]
                        
                        for i, (label, key, value) in enumerate(fields):
                            tk.Label(form_frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=i, column=0, sticky='w', pady=5)
                            var = tk.StringVar(value=str(value))
                            vars[key] = var
                            tk.Entry(form_frame, textvariable=var, width=30, font=Styles.TEXT_FONT).grid(row=i, column=1, pady=5)
                        
                        def save():
                            updates = {}
                            for key, var in vars.items():
                                value = var.get().strip()
                                updates[key] = value if value else ""
                            
                            if updates:
                                # 获取所有供应商数据
                                all_suppliers = self.system.excel_manager.get_all_suppliers()
                                # 找到要修改的供应商
                                idx = all_suppliers[all_suppliers['供应商编号'] == supplier_id].index
                                if len(idx) > 0:
                                    # 更新数据
                                    for key, value in updates.items():
                                        # 确保值不为空字符串时再更新
                                        if value:
                                            all_suppliers.at[idx[0], key] = value
                                        else:
                                            # 对于空值，保持原有值不变
                                            pass
                                    # 写回Excel
                                    self.system.excel_manager.write_sheet("供应商", all_suppliers)
                                    messagebox.showinfo("成功", "供应商信息更新成功！")
                                    edit_top.destroy()
                                    top.destroy()
                                    self.view_all_suppliers()
                                else:
                                    messagebox.showerror("错误", "更新失败！")
                            else:
                                messagebox.showinfo("提示", "未做任何修改。")
                        
                        btn_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        btn_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        btn_save = tk.Button(btn_frame, text="保存修改", font=Styles.BUTTON_FONT,
                                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=save,
                                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                        btn_save.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                        btn_save.bind("<Enter>", lambda e, b=btn_save: b.config(bg=Styles.BUTTON_HOVER_COLOR))
                        btn_save.bind("<Leave>", lambda e, b=btn_save: b.config(bg=Styles.PRIMARY_COLOR))
                        
                        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=edit_top.destroy,
                                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            
            elif '客户编号' in columns:
                # 客户表格 - 双击直接进入修改界面
                customer_id_idx = columns.index('客户编号')
                customer_id = values[customer_id_idx]
                
                df = self.system.excel_manager.get_all_customers()
                if not df.empty:
                    customer = df[df['客户编号'] == customer_id]
                    if not customer.empty:
                        customer_row = customer.iloc[0]
                        
                        # 创建修改窗口
                        edit_top = self._create_toplevel_with_size("dataframe_edit_customer", "medium", parent=top)
                        edit_top.title("修改客户信息")
                        edit_top.configure(bg=Styles.BACKGROUND_COLOR)
                        edit_top.resizable(True, True)
                        
                        # 创建标题区域
                        edit_title_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        edit_title_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        tk.Label(
                            edit_title_frame, 
                            text="修改客户信息", 
                            font=Styles.SUB_HEADER_FONT,
                            bg=Styles.BACKGROUND_COLOR,
                            fg=Styles.HEADER_COLOR
                        ).pack()
                        
                        form_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        form_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        # 创建变量
                        vars = {}
                        fields = [
                            ("客户名称", "客户名称", customer_row['客户名称']),
                            ("联系电话", "联系电话", customer_row['联系电话']),
                            ("电子邮箱", "电子邮箱", customer_row['电子邮箱']),
                            ("地址", "地址", customer_row['地址']),
                            ("备注", "备注", customer_row['备注'])
                        ]
                        
                        for i, (label, key, value) in enumerate(fields):
                            tk.Label(form_frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=i, column=0, sticky='w', pady=5)
                            var = tk.StringVar(value=str(value) if pd.notna(value) else "")
                            vars[key] = var
                            tk.Entry(form_frame, textvariable=var, width=30, font=Styles.TEXT_FONT).grid(row=i, column=1, pady=5)
                        
                        def save():
                            updates = {}
                            for key, var in vars.items():
                                value = var.get().strip()
                                updates[key] = value if value else ""
                            
                            if updates:
                                # 获取所有客户数据
                                all_customers = self.system.excel_manager.get_all_customers()
                                # 找到要修改的客户
                                idx = all_customers[all_customers['客户编号'] == customer_id].index
                                if len(idx) > 0:
                                    # 更新数据
                                    for key, value in updates.items():
                                        # 确保值不为空字符串时再更新
                                        if value:
                                            all_customers.at[idx[0], key] = value
                                        else:
                                            # 对于空值，保持原有值不变
                                            pass
                                    # 写回Excel
                                    self.system.excel_manager.write_sheet("客户信息", all_customers)
                                    messagebox.showinfo("成功", "客户信息更新成功！")
                                    edit_top.destroy()
                                    top.destroy()
                                    self.view_all_customers()
                                else:
                                    messagebox.showerror("错误", "更新失败！")
                            else:
                                messagebox.showinfo("提示", "未做任何修改。")
                        
                        btn_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
                        btn_frame.pack(pady=Styles.PADY_MEDIUM)
                        
                        btn_save = tk.Button(btn_frame, text="保存修改", font=Styles.BUTTON_FONT,
                                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=save,
                                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                        btn_save.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                        btn_save.bind("<Enter>", lambda e, b=btn_save: b.config(bg=Styles.BUTTON_HOVER_COLOR))
                        btn_save.bind("<Leave>", lambda e, b=btn_save: b.config(bg=Styles.PRIMARY_COLOR))
                        
                        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=edit_top.destroy,
                                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            

        
        tree.bind('<Double-1>', show_detail)

        # 添加状态栏
        status_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        status_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            status_frame, 
            text=f"共 {len(df)} 条记录", 
            font=Styles.TEXT_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg="#666666"
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)

        # 添加操作按钮
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        # 如果是供应商列表，添加删除按钮
        if '供应商编号' in columns:
            # 删除选中供应商
            def delete_selected_supplier():
                """删除选中的供应商"""
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("提示", "请先选择要删除的供应商")
                    return
                
                item = tree.item(selected[0])
                values = item['values']
                supplier_id_idx = columns.index('供应商编号')
                supplier_id = values[supplier_id_idx]
                supplier_name_idx = columns.index('供应商名称')
                supplier_name = values[supplier_name_idx]
                
                if messagebox.askyesno("确认", f"确定要删除供应商 '{supplier_name}' 吗？"):
                    # 从供应商表中删除
                    all_suppliers = self.system.excel_manager.get_all_suppliers()
                    new_suppliers = all_suppliers[all_suppliers['供应商编号'] != supplier_id]
                    self.system.excel_manager.write_sheet("供应商", new_suppliers)
                    messagebox.showinfo("成功", "供应商删除成功！")
                    top.destroy()
                    self.view_all_suppliers()
            
            tk.Button(
                btn_frame, 
                text="删除选中供应商", 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=delete_selected_supplier,
                bg=Styles.ERROR_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=10)
        
        # 如果是客户列表，添加删除按钮
        if '客户编号' in columns:
            # 删除选中客户
            def delete_selected_customer():
                """删除选中的客户"""
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("提示", "请先选择要删除的客户")
                    return
                
                item = tree.item(selected[0])
                values = item['values']
                customer_id_idx = columns.index('客户编号')
                customer_id = values[customer_id_idx]
                customer_name_idx = columns.index('客户名称')
                customer_name = values[customer_name_idx]
                
                if messagebox.askyesno("确认", f"确定要删除客户 '{customer_name}' 吗？"):
                    # 从客户表中删除
                    all_customers = self.system.excel_manager.get_all_customers()
                    new_customers = all_customers[all_customers['客户编号'] != customer_id]
                    self.system.excel_manager.write_sheet("客户信息", new_customers)
                    messagebox.showinfo("成功", "客户删除成功！")
                    top.destroy()
                    self.view_all_customers()
            
            tk.Button(
                btn_frame, 
                text="删除选中客户", 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=delete_selected_customer,
                bg=Styles.ERROR_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.ERROR_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=10)


def main():
    root = tk.Tk()
    app = TeaInventoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

