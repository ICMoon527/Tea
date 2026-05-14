import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tea_inventory_system import TeaInventorySystem
from backup_manager import BackupManager
from operation_logger import OperationLogger
from cloud_sync import CloudSyncManager
from config_manager import ConfigManager
from undo_manager import UndoManager
import pandas as pd
from prettytable import PrettyTable
from datetime import datetime
from logger import get_logger
from error_handler import setup_tk_exception_handler, setup_global_exception_handler

_logger = get_logger()

from styles import Styles
from gui_components import create_menu_card, clear_window, create_page_header, create_back_button, create_button_grid
from gui_dialogs import select_product_dialog, select_supplier_dialog, select_customer_dialog, show_dataframe_window
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
        
        # 读取主题配置
        theme = self.config_manager.get('ui.theme', 'light')
        Styles.is_dark_mode = (theme == 'dark')
        
        # 加载主窗口保存的大小
        win_width, win_height = self.config_manager.load_window_size(
            "main_window", 
            Styles.WINDOW_WIDTH, 
            Styles.WINDOW_HEIGHT
        )
        self.root.geometry(f"{win_width}x{win_height}")
        self.root.configure(bg=Styles.BACKGROUND_COLOR)
        
        setup_tk_exception_handler(self.root)
        
        # 绑定主窗口关闭事件，保存窗口大小
        self.root.protocol("WM_DELETE_WINDOW", self._on_main_window_close)
        
        self.system = TeaInventorySystem()
        
        # 初始化备份管理器、日志记录器和云同步管理器
        self.backup_manager = BackupManager()
        self.operation_logger = OperationLogger()
        self.cloud_sync_manager = CloudSyncManager()

        # 初始化撤销/重做管理器
        self.undo_manager = UndoManager()

        # 创建全局样式
        self.style = ttk.Style()
        self._configure_styles()

        self._status_bar = None
        self._create_status_bar()

        self.current_page = None
        self.create_main_menu()

        # 注册全局快捷键
        self.root.bind_all('<Control-z>', lambda e: self._undo_action())
        self.root.bind_all('<Control-y>', lambda e: self._redo_action())
        self.root.bind_all('<Control-Z>', lambda e: self._undo_action())
        self.root.bind_all('<Control-Y>', lambda e: self._redo_action())
        self._bind_shortcuts()

    def _on_main_window_close(self):
        """主窗口关闭时保存窗口大小"""
        try:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            self.config_manager.save_window_size("main_window", width, height)
        except Exception as e:
            _logger.error(f"保存主窗口大小失败: {e}")
        self.root.destroy()

    def toggle_theme(self):
        """切换亮色/暗色主题"""
        Styles.is_dark_mode = not Styles.is_dark_mode
        new_theme = 'dark' if Styles.is_dark_mode else 'light'
        self.config_manager.set('ui.theme', new_theme)
        self.apply_theme()

    def apply_theme(self):
        """应用当前主题配色到所有控件"""
        colors = Styles.get_colors()

        for key, value in colors.items():
            setattr(Styles, key, value)

        self.style.theme_use('clam')

        self.style.configure("TLabel",
                            font=Styles.LABEL_FONT,
                            background=colors['BACKGROUND_COLOR'],
                            foreground=colors['TEXT_PRIMARY'])

        self.style.configure("Title.TLabel",
                            font=Styles.TITLE_FONT,
                            background=colors['BACKGROUND_COLOR'],
                            foreground=colors['TEXT_PRIMARY'])

        self.style.configure("Modern.TButton",
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=colors['PRIMARY_COLOR'],
                            foreground='white',
                            borderwidth=0,
                            relief="flat",
                            focuscolor=colors['PRIMARY_COLOR'])
        self.style.map("Modern.TButton",
                      background=[("active", colors['PRIMARY_DARK']),
                                 ("pressed", colors['PRIMARY_DARK']),
                                 ("!disabled", colors['PRIMARY_COLOR'])],
                      foreground=[("!disabled", "white")],
                      relief=[("pressed", "flat"),
                              ("!pressed", "flat")])

        self.style.configure("Secondary.TButton",
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=colors['SURFACE_COLOR'],
                            foreground=colors['TEXT_PRIMARY'],
                            borderwidth=1,
                            relief="flat",
                            focuscolor=colors['SURFACE_COLOR'])
        self.style.map("Secondary.TButton",
                      background=[("active", colors['BORDER_LIGHT']),
                                 ("pressed", colors['BORDER_COLOR']),
                                 ("!disabled", colors['SURFACE_COLOR'])],
                      foreground=[("!disabled", colors['TEXT_PRIMARY'])],
                      relief=[("pressed", "flat"),
                              ("!pressed", "flat")])

        self.style.configure("Success.TButton",
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=colors['SUCCESS_COLOR'],
                            foreground='white',
                            borderwidth=0,
                            relief="flat")
        self.style.map("Success.TButton",
                      background=[("active", colors['SUCCESS_COLOR']),
                                 ("pressed", colors['SECONDARY_DARK']),
                                 ("!disabled", colors['SUCCESS_COLOR'])],
                      foreground=[("!disabled", "white")])

        self.style.configure("Danger.TButton",
                            font=Styles.BUTTON_FONT,
                            padding=(16, 10),
                            background=colors['ERROR_COLOR'],
                            foreground='white',
                            borderwidth=0,
                            relief="flat")
        self.style.map("Danger.TButton",
                      background=[("active", "#DC2626"),
                                 ("pressed", "#B91C1C"),
                                 ("!disabled", colors['ERROR_COLOR'])],
                      foreground=[("!disabled", "white")])

        self.style.configure("TEntry",
                            font=Styles.TEXT_FONT,
                            padding=(10, 8),
                            fieldbackground=colors['SURFACE_COLOR'],
                            foreground=colors['TEXT_PRIMARY'],
                            borderwidth=1,
                            relief="solid")
        self.style.map("TEntry",
                      fieldbackground=[("focus", colors['SURFACE_COLOR'])],
                      bordercolor=[("focus", colors['PRIMARY_COLOR'])])

        self.style.configure("Treeview",
                            font=Styles.TEXT_FONT,
                            background=colors['SURFACE_COLOR'],
                            foreground=colors['TEXT_PRIMARY'],
                            rowheight=32,
                            borderwidth=0,
                            relief="flat")
        self.style.configure("Treeview.Heading",
                            font=Styles.LABEL_FONT,
                            background=colors['BACKGROUND_COLOR'],
                            foreground=colors['TEXT_SECONDARY'],
                            borderwidth=1,
                            relief="flat")
        self.style.map("Treeview",
                      background=[("selected", colors['PRIMARY_COLOR'])],
                      foreground=[("selected", "white")])
        self.style.map("Treeview.Heading",
                      background=[("active", colors['BORDER_LIGHT'])])

        self.style.configure("Card.TFrame",
                            background=colors['SURFACE_COLOR'],
                            relief="flat",
                            borderwidth=0)

        self.style.configure("TSeparator",
                            background=colors['BORDER_COLOR'])

        self._recursive_apply_bg(self.root, colors['BACKGROUND_COLOR'])

    def _recursive_apply_bg(self, widget, default_bg):
        """递归更新非ttk控件的背景和前景色"""
        colors = Styles.get_colors()
        try:
            widget_class = widget.winfo_class()
        except Exception:
            return

        if widget_class in ('Frame', 'Toplevel', 'Tk', 'Labelframe'):
            try:
                widget.configure(bg=colors['BACKGROUND_COLOR'])
            except Exception:
                pass
        elif widget_class == 'Label':
            try:
                widget.configure(
                    bg=colors['BACKGROUND_COLOR'],
                    fg=colors['TEXT_PRIMARY']
                )
            except Exception:
                pass
        elif widget_class == 'Button':
            pass
        elif widget_class == 'Entry':
            try:
                widget.configure(
                    bg=colors['SURFACE_COLOR'],
                    fg=colors['TEXT_PRIMARY'],
                    insertbackground=colors['TEXT_PRIMARY']
                )
            except Exception:
                pass
        elif widget_class == 'Listbox':
            try:
                widget.configure(
                    bg=colors['SURFACE_COLOR'],
                    fg=colors['TEXT_PRIMARY']
                )
            except Exception:
                pass

        for child in widget.winfo_children():
            self._recursive_apply_bg(child, default_bg)
    
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
        self.current_page = "main_menu"
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
            ("商品管理\n(Ctrl+1)", self.product_management, "📦"),
            ("销售功能\n(Ctrl+3)", self.sales_management, "💰"),
            ("进货管理\n(Ctrl+2)", self.stock_management, "📥"),
            ("供应商管理", self.supplier_management, "🤝"),
            ("客户管理", self.customer_management, "👥"),
            ("销售记录管理", self.sales_record_management, "📋"),
            ("统计分析\n(Ctrl+4)", self.statistics_analysis, "📊"),
            ("系统管理\n(Ctrl+Shift+S)", self.system_management, "⚙️")
        ]

        # 创建3列网格
        for i, (text, command, icon) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            create_menu_card(card_grid, text, command, icon, row, col)

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
        return create_menu_card(parent, text, command, icon, row, col)

    def clear_window(self):
        """清空窗口（保留状态栏）"""
        self.current_page = None
        for widget in self.root.winfo_children():
            if widget is self._status_bar:
                continue
            widget.destroy()
        self._ensure_status_bar()

    def _create_page_header(self, parent, title, subtitle=None):
        return create_page_header(parent, title, subtitle)

    def _create_back_button(self, parent, command):
        return create_back_button(parent, command)

    def _create_button_grid(self, parent, buttons, columns=None):
        """创建统一的卡片式按钮网格

        Args:
            parent: 父容器
            buttons: 按钮列表，格式为 [(text, command, icon), ...]
            columns: 列数（自动判断如果为None）
        """
        return create_button_grid(parent, buttons, columns)

    def _select_product_dialog(self, target_var):
        select_product_dialog(self, target_var)
    
    def _select_supplier_dialog(self, target_var):
        select_supplier_dialog(self, target_var)
    
    def _select_customer_dialog(self, target_var):
        select_customer_dialog(self, target_var)
    
    def show_dataframe_window(self, df, title):
        """显示DataFrame的窗口（带分页功能）"""
        show_dataframe_window(self, df, title)

    def _bind_shortcuts(self):
        """绑定键盘快捷键"""
        self.root.bind('<Control-n>', lambda e: self.show_create_sale_page())
        self.root.bind('<Control-p>', lambda e: self.show_add_product_page())
        self.root.bind('<Control-i>', lambda e: self.show_stock_in_page())
        self.root.bind('<Control-b>', lambda e: self._on_backup())
        self.root.bind('<Control-Shift-B>', lambda e: self._on_restore_backup())
        self.root.bind('<F5>', lambda e: self._on_f5_refresh())
        self.root.bind('<Escape>', self._on_escape)
        self.root.bind('<Control-Key-1>', lambda e: self.show_product_management_page())
        self.root.bind('<Control-Key-2>', lambda e: self.show_purchase_management_page())
        self.root.bind('<Control-Key-3>', lambda e: self.show_sales_management_page())
        self.root.bind('<Control-Key-4>', lambda e: self.show_statistics_page())
        self.root.bind('<Control-d>', lambda e: self.show_export_page())
        self.root.bind('<Control-Shift-S>', lambda e: self.show_settings_page())

    def _on_escape(self, event):
        """Escape 键：只在非主菜单页面起作用"""
        if self.current_page != "main_menu":
            self.show_main_menu()

    def _on_f5_refresh(self):
        """F5 刷新数据"""
        self.system.excel_manager.clear_cache()
        self.show_main_menu()
        messagebox.showinfo("刷新", "数据已刷新")

    def _on_backup(self):
        """Ctrl+B 备份数据"""
        try:
            backup_path = self.backup_manager.create_backup()
            messagebox.showinfo("备份成功", f"备份文件：{backup_path}")
            self.operation_logger.log_operation(
                operation_type="备份",
                module="系统管理",
                details=f"快捷鍵创建数据备份: {backup_path}"
            )
        except Exception as e:
            messagebox.showerror("备份失败", str(e))

    def _on_restore_backup(self):
        """Ctrl+Shift+B 恢复备份"""
        backups = self.backup_manager.list_backups()
        if not backups:
            messagebox.showinfo("提示", "没有可用的备份文件")
            return
        top = tk.Toplevel(self.root)
        top.title("选择备份文件恢复")
        top.geometry("600x400")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.transient(self.root)
        top.grab_set()

        tk.Label(top, text="请选择要恢复的备份文件",
                 font=Styles.SUB_HEADER_FONT, bg=Styles.BACKGROUND_COLOR,
                 fg=Styles.TEXT_PRIMARY).pack(pady=10)

        tree = ttk.Treeview(top, columns=("filename", "size", "time"), show="headings")
        tree.heading("filename", text="备份文件")
        tree.heading("size", text="文件大小")
        tree.heading("time", text="创建时间")
        tree.column("filename", width=300)
        tree.column("size", width=100, anchor=tk.CENTER)
        tree.column("time", width=180, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for b in backups:
            tree.insert("", tk.END, values=(b['filename'], b['size_formatted'],
                         b['created_time'].strftime('%Y-%m-%d %H:%M:%S')))

        def do_restore():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("提示", "请先选择一个备份文件")
                return
            item = tree.item(sel[0])
            filename = item['values'][0]
            backup_info = next((b for b in backups if b['filename'] == filename), None)
            if not backup_info:
                messagebox.showerror("错误", "备份文件不存在")
                return
            if messagebox.askyesno("确认恢复", f"确定要恢复备份吗？\n\n备份文件：{filename}\n\n当前数据将被覆盖！"):
                try:
                    success = self.backup_manager.restore_backup(backup_info['path'])
                    if success:
                        messagebox.showinfo("成功", "数据恢复成功！")
                        self.operation_logger.log_operation(
                            operation_type="恢复", module="系统管理",
                            details=f"快捷鍵恢复数据备份: {filename}"
                        )
                        self.show_main_menu()
                        top.destroy()
                    else:
                        messagebox.showerror("错误", "数据恢复失败！")
                except Exception as e:
                    messagebox.showerror("恢复失败", str(e))

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="恢复选中备份", command=do_restore,
                   style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=top.destroy,
                   style="Secondary.TButton").pack(side=tk.LEFT, padx=5)

    def show_main_menu(self):
        """返回主菜单"""
        self.create_main_menu()

    def show_create_sale_page(self):
        """新销售"""
        self.sales_management()

    def show_add_product_page(self):
        """新产品"""
        self.add_product_gui()

    def show_stock_in_page(self):
        """新进货"""
        self.stock_in_gui()

    def show_product_management_page(self):
        """商品管理页面"""
        self.product_management()

    def show_purchase_management_page(self):
        """进货管理页面"""
        self.stock_management()

    def show_sales_management_page(self):
        """销售管理页面"""
        self.sales_management()

    def show_statistics_page(self):
        """统计报表页面"""
        self.statistics_analysis()

    def show_settings_page(self):
        """系统设置页面"""
        self.system_management()

    def show_export_page(self):
        """数据导出页面"""
        from data_exporter import DataExporter
        exporter = DataExporter(self.system.excel_manager)
        self.clear_window()
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)

        self._create_page_header(main_container, "数据导出", "将数据导出为不同格式的文件")

        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)

        buttons = [
            ("导出商品数据", lambda: self._export_single("商品数据", "commodities", exporter), "📦"),
            ("导出销售数据", lambda: self._export_single("销售数据", "sales", exporter), "💰"),
            ("导出发货数据", lambda: self._export_single("发货数据", "stocks", exporter), "📥"),
            ("导出供应商数据", lambda: self._export_single("供应商数据", "suppliers", exporter), "🤝"),
            ("导出客户数据", lambda: self._export_single("客户数据", "customers", exporter), "👥"),
            ("导出全部数据", lambda: self._export_all(exporter), "📊"),
        ]
        self._create_button_grid(buttons_container, buttons, columns=3)
        self._create_back_button(main_container, self.create_main_menu)

    def _export_single(self, name, data_type, exporter):
        """导出单个数据模块"""
        format_map = {"excel": (".xlsx", "Excel文件"), "csv": (".csv", "CSV文件"), "json": (".json", "JSON文件")}
        default_fmt = self.config_manager.get_export_config().get('default_format', 'excel')
        ext, desc = format_map.get(default_fmt, (".xlsx", "Excel文件"))
        file_path = filedialog.asksaveasfilename(
            title=f"导出{name}",
            defaultextension=ext,
            filetypes=[(desc, f"*{ext}")]
        )
        if not file_path:
            return
        export_funcs = {
            "commodities": exporter.export_commodities,
            "sales": exporter.export_sales,
            "stocks": exporter.export_stocks,
            "suppliers": exporter.export_suppliers,
            "customers": exporter.export_customers,
        }
        try:
            func = export_funcs[data_type]
            success = func(export_path=file_path, format=default_fmt)
            if success:
                messagebox.showinfo("成功", f"{name}导出成功！\n保存位置：{file_path}")
            else:
                messagebox.showerror("错误", f"{name}导出失败！")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")

    def _export_all(self, exporter):
        """导出全部数据"""
        export_dir = filedialog.askdirectory(title="选择导出目录")
        if not export_dir:
            return
        try:
            results = exporter.export_all_data(export_dir)
            success_count = sum(1 for v in results.values() if v)
            if success_count > 0:
                messagebox.showinfo("成功", f"全部数据导出成功！\n导出目录：{export_dir}")
            else:
                messagebox.showerror("错误", "数据导出失败！")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")

    def _create_status_bar(self):
        if self._status_bar is not None:
            return
        self._status_bar = tk.Frame(self.root, bg=Styles.PRIMARY_COLOR, height=28)
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._status_bar.pack_propagate(False)

        self._status_label = tk.Label(
            self._status_bar,
            text="就绪 | Ctrl+Z 撤销 | Ctrl+Y 重做",
            font=("微软雅黑", 9),
            bg=Styles.PRIMARY_COLOR,
            fg="white"
        )
        self._status_label.pack(side=tk.LEFT, padx=10)

    def _ensure_status_bar(self):
        if self._status_bar is None or not self._status_bar.winfo_exists():
            self._status_bar = None
            self._create_status_bar()
        self._update_status_bar()

    def _update_status_bar(self):
        if not hasattr(self, '_status_label') or self._status_label is None:
            return
        if not self._status_label.winfo_exists():
            return

        parts = ["就绪"]
        if self.undo_manager.can_undo():
            undo_name = self.undo_manager.get_undo_name()
            parts.append(f"可撤销: {undo_name}")
        if self.undo_manager.can_redo():
            redo_name = self.undo_manager.get_redo_name()
            parts.append(f"可重做: {redo_name}")
        parts.append("Ctrl+Z 撤销 | Ctrl+Y 重做")
        self._status_label.config(text=" | ".join(parts))

    def _undo_action(self):
        if not self.undo_manager.can_undo():
            messagebox.showinfo("提示", "没有可以撤销的操作")
            return
        try:
            action_name = self.undo_manager.undo()
            if action_name:
                self._update_status_bar()
                messagebox.showinfo("撤销", f"已撤销: {action_name}")
        except Exception as e:
            messagebox.showerror("撤销失败", f"撤销操作失败: {e}")
            self._update_status_bar()

    def _redo_action(self):
        if not self.undo_manager.can_redo():
            messagebox.showinfo("提示", "没有可以重做的操作")
            return
        try:
            action_name = self.undo_manager.redo()
            if action_name:
                self._update_status_bar()
                messagebox.showinfo("重做", f"已重做: {action_name}")
        except Exception as e:
            messagebox.showerror("重做失败", f"重做操作失败: {e}")
            self._update_status_bar()


def main():
    setup_global_exception_handler()
    root = tk.Tk()
    app = TeaInventoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()