
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tea_inventory_system import TeaInventorySystem
from backup_manager import BackupManager
from operation_logger import OperationLogger
from cloud_sync import CloudSyncManager
import pandas as pd
from prettytable import PrettyTable
from datetime import datetime

# 全局样式配置
class Styles:
    """GUI样式配置"""
    # 颜色方案
    PRIMARY_COLOR = "#4A90E2"  # 主色调：蓝色
    SECONDARY_COLOR = "#50E3C2"  # 辅助色：青色
    BACKGROUND_COLOR = "#F5F7FA"  # 背景色：浅灰色
    TEXT_COLOR = "#333333"  # 文本色：深灰色
    HEADER_COLOR = "#2C3E50"  # 标题色：深蓝色
    BUTTON_HOVER_COLOR = "#357ABD"  # 按钮悬停色
    ERROR_COLOR = "#E74C3C"  # 错误色：红色
    SUCCESS_COLOR = "#27AE60"  # 成功色：绿色
    
    # 字体配置
    HEADER_FONT = ("微软雅黑", 24, "bold")
    SUB_HEADER_FONT = ("微软雅黑", 18, "bold")
    BUTTON_FONT = ("微软雅黑", 12)
    LABEL_FONT = ("微软雅黑", 10)
    TEXT_FONT = ("微软雅黑", 9)
    
    # 间距配置
    PADY_LARGE = 30
    PADY_MEDIUM = 20
    PADY_SMALL = 10
    PADX_LARGE = 40
    PADX_MEDIUM = 20
    PADX_SMALL = 10
    
    # 控件尺寸
    BUTTON_WIDTH = 20
    BUTTON_HEIGHT = 2
    ENTRY_WIDTH = 30
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    DIALOG_WIDTH = 600
    DIALOG_HEIGHT = 400


class TeaInventoryGUI:
    """茶叶进销存管理系统图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("茶叶进销存管理系统——狗拿耗子")
        self.root.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")
        self.root.configure(bg=Styles.BACKGROUND_COLOR)
        self.system = TeaInventorySystem()
        
        # 初始化备份管理器、日志记录器和云同步管理器
        self.backup_manager = BackupManager()
        self.operation_logger = OperationLogger()
        self.cloud_sync_manager = CloudSyncManager()

        # 创建全局样式
        self.style = ttk.Style()
        self._configure_styles()

        self.create_main_menu()

    def _configure_styles(self):
        """配置ttk控件样式"""
        # 配置按钮样式
        self.style.configure("TButton", 
                            font=Styles.BUTTON_FONT,
                            padding=(10, 5))
        self.style.map("TButton", 
                      background=[("active", Styles.BUTTON_HOVER_COLOR)],
                      foreground=[("active", "white")])
        
        # 配置标签样式
        self.style.configure("TLabel", 
                            font=Styles.LABEL_FONT,
                            background=Styles.BACKGROUND_COLOR,
                            foreground=Styles.TEXT_COLOR)
        
        # 配置输入框样式
        self.style.configure("TEntry", 
                            font=Styles.TEXT_FONT,
                            padding=(5, 3))
        
        # 配置树状表格样式
        self.style.configure("Treeview", 
                            font=Styles.TEXT_FONT,
                            background="white",
                            foreground=Styles.TEXT_COLOR,
                            rowheight=25)
        self.style.configure("Treeview.Heading", 
                            font=Styles.LABEL_FONT,
                            background=Styles.PRIMARY_COLOR,
                            foreground="black")
        self.style.map("Treeview", 
                      background=[("selected", Styles.SECONDARY_COLOR)],
                      foreground=[("selected", "white")])

    def create_main_menu(self):
        """创建主菜单"""
        self.clear_window()

        # 创建主标题
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_LARGE)
        
        title_label = tk.Label(
            title_frame, 
            text="茶叶进销存管理系统——狗拿耗子", 
            font=Styles.HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        )
        title_label.pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)
        
        buttons = [
            ("商品管理", self.product_management),
            ("销售功能", self.sales_management),
            ("进货管理", self.stock_management),
            ("供应商管理", self.supplier_management),
            ("客户管理", self.customer_management),
            ("销售记录管理", self.sales_record_management),
            ("统计分析", self.statistics_analysis),
            ("系统管理", self.system_management)
        ]

        # 按2x4网格排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

        # 添加版权信息
        footer_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        footer_frame.pack(side=tk.BOTTOM, pady=Styles.PADY_MEDIUM)
        
        footer_label = tk.Label(
            footer_frame, 
            text="© 2026 茶叶进销存管理系统——狗拿耗子", 
            font=Styles.TEXT_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg="#666666"
        )
        footer_label.pack()

    def clear_window(self):
        """清空窗口"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def product_management(self):
        """商品管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="商品管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("查看所有商品", self.view_all_products),
            ("添加商品", self.add_product_gui),
            ("修改商品", self.update_product_gui),
            ("删除商品", self.delete_product_gui),
            ("按编号查询", self.query_product_by_id_gui),
            ("按商品名查询", self.query_product_by_name_gui)
        ]

        # 按2行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)
        
        # 创建返回主菜单按钮 - 居中靠下
        footer_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        footer_frame.pack(side=tk.BOTTOM, pady=Styles.PADY_LARGE, fill=tk.X)
        
        back_btn = tk.Button(
            footer_frame, 
            text="返回主菜单", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=self.create_main_menu,
            bg=Styles.ERROR_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        # 添加悬停效果
        back_btn.bind("<Enter>", lambda e, b=back_btn: b.config(bg="#C0392B"))
        back_btn.bind("<Leave>", lambda e, b=back_btn: b.config(bg=Styles.ERROR_COLOR))
        
        back_btn.pack()
        # 确保按钮在底部框架中居中
        footer_frame.pack_propagate(False)
        footer_frame.configure(height=100)

    def view_all_products(self):
        """查看所有商品"""
        df = self.system.excel_manager.get_all_commodities()
        self.show_dataframe_window(df, "商品列表")

    def add_product_gui(self):
        """添加商品GUI"""
        top = tk.Toplevel(self.root)
        top.title("添加商品")
        top.geometry("900x750")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="添加商品", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建表单
        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM)

        # 商品编号
        tk.Label(form_frame, text="商品编号 (留空自动生成)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=5)
        com_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=com_id_var, width=30, font=Styles.TEXT_FONT).grid(row=0, column=1, pady=5)

        # 茶类
        tk.Label(form_frame, text="茶类 *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=1, column=0, sticky='w', pady=5)
        tea_category_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=tea_category_var, width=30, font=Styles.TEXT_FONT).grid(row=1, column=1, pady=5)

        # 品种
        tk.Label(form_frame, text="品种 *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=2, column=0, sticky='w', pady=5)
        variety_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=variety_var, width=30, font=Styles.TEXT_FONT).grid(row=2, column=1, pady=5)

        # 公司/品牌
        tk.Label(form_frame, text="公司/品牌", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=3, column=0, sticky='w', pady=5)
        company_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=company_var, width=30, font=Styles.TEXT_FONT).grid(row=3, column=1, pady=5)

        # 产区
        tk.Label(form_frame, text="产区", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=4, column=0, sticky='w', pady=5)
        origin_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=origin_var, width=30, font=Styles.TEXT_FONT).grid(row=4, column=1, pady=5)

        # 商品名称
        tk.Label(form_frame, text="商品名称 *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=5, column=0, sticky='w', pady=5)
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, width=30, font=Styles.TEXT_FONT).grid(row=5, column=1, pady=5)

        # 规格
        tk.Label(form_frame, text="规格 *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=6, column=0, sticky='w', pady=5)
        specification_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=specification_var, width=30, font=Styles.TEXT_FONT).grid(row=6, column=1, pady=5)

        # 成本价
        tk.Label(form_frame, text="成本价(每斤) *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=7, column=0, sticky='w', pady=5)
        cost_price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=cost_price_var, width=30, font=Styles.TEXT_FONT).grid(row=7, column=1, pady=5)

        # 零售价
        tk.Label(form_frame, text="零售价(每斤) *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=8, column=0, sticky='w', pady=5)
        retail_price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=retail_price_var, width=30, font=Styles.TEXT_FONT).grid(row=8, column=1, pady=5)

        # 初始库存
        tk.Label(form_frame, text="初始库存(斤) *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=9, column=0, sticky='w', pady=5)
        current_stock_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=current_stock_var, width=30, font=Styles.TEXT_FONT).grid(row=9, column=1, pady=5)

        # 生产日期
        tk.Label(form_frame, text="生产日期(YYYY-MM-DD)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=10, column=0, sticky='w', pady=5)
        production_date_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=production_date_var, width=30, font=Styles.TEXT_FONT).grid(row=10, column=1, pady=5)

        # 保质期
        tk.Label(form_frame, text="保质期(月) *", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=11, column=0, sticky='w', pady=5)
        shelf_life_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=shelf_life_var, width=30, font=Styles.TEXT_FONT).grid(row=11, column=1, pady=5)

        # 品质特征
        tk.Label(form_frame, text="品质特征", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=12, column=0, sticky='w', pady=5)
        quality_features_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=quality_features_var, width=30, font=Styles.TEXT_FONT).grid(row=12, column=1, pady=5)

        # 年份
        tk.Label(form_frame, text="年份", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=13, column=0, sticky='w', pady=5)
        year_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=year_var, width=30, font=Styles.TEXT_FONT).grid(row=13, column=1, pady=5)

        # 等级
        tk.Label(form_frame, text="等级", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=14, column=0, sticky='w', pady=5)
        grade_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=grade_var, width=30, font=Styles.TEXT_FONT).grid(row=14, column=1, pady=5)

        # 计量单位
        tk.Label(form_frame, text="计量单位(斤/克) (默认: 斤)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=15, column=0, sticky='w', pady=5)
        unit_var = tk.StringVar(value="斤")
        tk.Entry(form_frame, textvariable=unit_var, width=30, font=Styles.TEXT_FONT).grid(row=15, column=1, pady=5)

        # 按钮
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        def submit():
            try:
                # 验证必填字段
                if not tea_category_var.get().strip():
                    messagebox.showerror("错误", "请输入茶类")
                    return
                if not variety_var.get().strip():
                    messagebox.showerror("错误", "请输入品种")
                    return
                if not name_var.get().strip():
                    messagebox.showerror("错误", "请输入商品名称")
                    return
                if not specification_var.get().strip():
                    messagebox.showerror("错误", "请输入规格")
                    return
                if not cost_price_var.get().strip():
                    messagebox.showerror("错误", "请输入成本价")
                    return
                if not retail_price_var.get().strip():
                    messagebox.showerror("错误", "请输入零售价")
                    return
                if not current_stock_var.get().strip():
                    messagebox.showerror("错误", "请输入初始库存")
                    return
                if not shelf_life_var.get().strip():
                    messagebox.showerror("错误", "请输入保质期")
                    return

                com_id_input = com_id_var.get().strip()
                if com_id_input:
                    com_id = com_id_input
                    existing = self.system.excel_manager.get_commodity_by_id(com_id)
                    if existing is not None:
                        messagebox.showerror("错误", "该商品编号已存在！")
                        return
                else:
                    com_id = self.system.excel_manager.generate_id("C", "商品信息", "商品编号")

                tea_category = tea_category_var.get().strip()
                variety = variety_var.get().strip()
                company = company_var.get().strip()
                origin = origin_var.get().strip()
                name = name_var.get().strip()
                specification = specification_var.get().strip()

                cost_price = float(cost_price_var.get())
                retail_price = float(retail_price_var.get())
                current_stock = float(current_stock_var.get())
                shelf_life = int(shelf_life_var.get())

                production_date = production_date_var.get().strip()
                quality_features = quality_features_var.get().strip()
                year = year_var.get().strip()
                grade = grade_var.get().strip()
                unit = unit_var.get().strip() or "斤"

                from tea_commodity import TeaCommodity
                commodity = TeaCommodity(
                    com_id=com_id, tea_category=tea_category, variety=variety,
                    company=company, origin=origin, name=name,
                    specification=specification, cost_price=cost_price,
                    retail_price=retail_price, production_date=production_date,
                    shelf_life=shelf_life, current_stock=current_stock,
                    quality_features=quality_features, year=year, grade=grade, unit=unit
                )

                self.system.excel_manager.add_commodity(commodity.to_list())
                messagebox.showinfo("成功", f"商品添加成功！\n商品编号: {com_id}")
                top.destroy()
            except ValueError as e:
                messagebox.showerror("错误", f"数据输入错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        btn_confirm = tk.Button(btn_frame, text="确认添加", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=submit,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def update_product_gui(self):
        """修改商品GUI - 从列表选择"""
        top = tk.Toplevel(self.root)
        top.title("修改商品")
        top.geometry("1000x700")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        tk.Label(top, text="请选择要修改的商品", 
                 font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR,
                 fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_MEDIUM)

        # 获取所有商品
        df = self.system.excel_manager.get_all_commodities()
        if df.empty:
            messagebox.showinfo("提示", "暂无商品数据")
            top.destroy()
            return

        # 创建商品列表
        list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        list_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(list_frame, style="Treeview", show="headings")
        tree["columns"] = ("商品编号", "商品名称", "茶类", "品种", "当前库存", "零售价")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)

        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 填充商品列表
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=(
                row['商品编号'],
                row['商品名称'],
                row['茶类'],
                row['品种'],
                row['当前库存'],
                row['零售价']
            ))

        def edit_selected():
            """编辑选中的商品"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个商品")
                return

            item = tree.item(selected[0])
            com_id = item['values'][0]

            commodity = self.system.excel_manager.get_commodity_by_id(com_id)
            if commodity is None:
                messagebox.showerror("错误", "未找到该商品")
                return

            # 创建修改窗口
            edit_top = tk.Toplevel(top)
            edit_top.title("修改商品信息")
            edit_top.geometry("900x750")
            edit_top.configure(bg=Styles.BACKGROUND_COLOR)

            # 创建标题区域
            title_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            title_frame.pack(pady=Styles.PADY_MEDIUM)
            
            tk.Label(
                title_frame, 
                text="修改商品信息", 
                font=Styles.SUB_HEADER_FONT,
                bg=Styles.BACKGROUND_COLOR,
                fg=Styles.HEADER_COLOR
            ).pack()

            form_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            form_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM)

            # 创建变量
            vars = {}
            fields = [
                ("茶类", "茶类", commodity['茶类']),
                ("品种", "品种", commodity['品种']),
                ("公司", "公司", commodity['公司']),
                ("产区", "产区", commodity['产区']),
                ("商品名称", "商品名称", commodity['商品名称']),
                ("规格", "规格", commodity['规格']),
                ("成本价", "成本价", commodity['成本价']),
                ("零售价", "零售价", commodity['零售价']),
                ("当前库存", "当前库存", commodity['当前库存']),
                ("生产日期", "生产日期", commodity['生产日期']),
                ("保质期(月)", "保质期(月)", commodity['保质期(月)']),
                ("品质特征", "品质特征", commodity['品质特征']),
                ("年份", "年份", commodity['年份']),
                ("等级", "等级", commodity['等级']),
                ("单位", "单位", commodity['单位'])
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
                    if value:
                        if key in ['成本价', '零售价', '当前库存']:
                            updates[key] = float(value)
                        elif key in ['保质期(月)', '年份']:
                            updates[key] = int(value)
                        else:
                            updates[key] = value

                if updates:
                    success = self.system.excel_manager.update_commodity(com_id, updates)
                    if success:
                        messagebox.showinfo("成功", "商品信息更新成功！")
                        edit_top.destroy()
                        top.destroy()
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

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        tk.Button(btn_frame, text="修改选中商品", 
                 font=Styles.BUTTON_FONT,
                 width=15,
                 command=edit_selected,
                 bg=Styles.PRIMARY_COLOR,
                 fg="white",
                 relief=tk.FLAT,
                 padx=10,
                 pady=5).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="关闭", 
                 font=Styles.BUTTON_FONT,
                 width=15,
                 command=top.destroy,
                 bg=Styles.ERROR_COLOR,
                 fg="white",
                 relief=tk.FLAT,
                 padx=10,
                 pady=5).pack(side=tk.LEFT, padx=5)

        # 双击商品也可以编辑
        tree.bind('<Double-1>', lambda e: edit_selected())

    def delete_product_gui(self):
        """删除商品GUI"""
        top = tk.Toplevel(self.root)
        top.title("删除商品")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="删除商品", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM)

        tk.Label(form_frame, text="请输入商品编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        com_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=com_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def delete():
            com_id = com_id_var.get().strip()
            commodity = self.system.excel_manager.get_commodity_by_id(com_id)
            if commodity is None:
                messagebox.showerror("错误", "未找到该商品")
                return

            if messagebox.askyesno("确认", f"确定要删除商品 '{commodity['商品名称']}' 吗？"):
                success = self.system.excel_manager.delete_commodity(com_id)
                if success:
                    messagebox.showinfo("成功", "商品删除成功！")
                    top.destroy()
                else:
                    messagebox.showerror("错误", "删除失败！")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_delete = tk.Button(btn_frame, text="删除", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=delete,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_delete.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.PRIMARY_COLOR))

    def query_product_by_id_gui(self):
        """按编号查询商品GUI"""
        top = tk.Toplevel(self.root)
        top.title("按编号查询商品")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="按编号查询商品", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM)

        tk.Label(form_frame, text="请输入商品编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        com_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=com_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def query():
            com_id = com_id_var.get().strip()
            commodity = self.system.excel_manager.get_commodity_by_id(com_id)
            if commodity is None:
                messagebox.showerror("错误", "未找到该商品")
                return

            # 显示商品信息
            info_top = tk.Toplevel(top)
            info_top.title("商品信息")
            info_top.geometry("700x500")
            info_top.configure(bg=Styles.BACKGROUND_COLOR)

            # 创建标题区域
            info_title_frame = tk.Frame(info_top, bg=Styles.BACKGROUND_COLOR)
            info_title_frame.pack(pady=Styles.PADY_MEDIUM)
            
            tk.Label(
                info_title_frame, 
                text="商品详情", 
                font=Styles.SUB_HEADER_FONT,
                bg=Styles.BACKGROUND_COLOR,
                fg=Styles.HEADER_COLOR
            ).pack()

            frame = tk.Frame(info_top, bg=Styles.BACKGROUND_COLOR)
            frame.pack(pady=Styles.PADY_LARGE, padx=Styles.PADX_LARGE)

            for key, value in commodity.items():
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

            btn_close = tk.Button(info_top, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=info_top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack(pady=Styles.PADY_MEDIUM)

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_query = tk.Button(btn_frame, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=query,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_query.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_query.bind("<Enter>", lambda e, b=btn_query: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_query.bind("<Leave>", lambda e, b=btn_query: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def query_product_by_name_gui(self):
        """按商品名模糊查询商品GUI"""
        top = tk.Toplevel(self.root)
        top.title("按商品名查询")
        top.geometry("900x700")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        tk.Label(top, text="请输入商品名称（支持模糊搜索）", 
                 font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR,
                 fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_MEDIUM)
        
        search_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        search_frame.pack(pady=Styles.PADY_SMALL)
        
        name_var = tk.StringVar()
        entry = tk.Entry(search_frame, textvariable=name_var, 
                        font=Styles.TEXT_FONT, width=40)
        entry.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        results_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        results_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM, fill=tk.BOTH, expand=True)
        
        results_label = tk.Label(results_frame, text="搜索结果", 
                                 font=Styles.LABEL_FONT,
                                 bg=Styles.BACKGROUND_COLOR,
                                 fg=Styles.HEADER_COLOR)
        results_label.pack(pady=Styles.PADY_SMALL, anchor=tk.W)
        
        tree = ttk.Treeview(results_frame, style="Treeview", show="headings")
        tree["columns"] = ("商品编号", "商品名称", "茶类", "品种", "当前库存", "零售价")
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def search():
            """执行搜索"""
            keyword = name_var.get().strip()
            if not keyword:
                messagebox.showwarning("提示", "请输入搜索关键词")
                return
            
            df = self.system.excel_manager.get_all_commodities()
            if df.empty:
                messagebox.showinfo("提示", "暂无商品数据")
                return
            
            mask = df['商品名称'].str.contains(keyword, case=False, na=False)
            results = df[mask]
            
            for item in tree.get_children():
                tree.delete(item)
            
            if results.empty:
                messagebox.showinfo("提示", f"未找到包含 '{keyword}' 的商品")
                return
            
            for _, row in results.iterrows():
                tree.insert("", tk.END, values=(
                    row['商品编号'],
                    row['商品名称'],
                    row['茶类'],
                    row['品种'],
                    row['当前库存'],
                    row['零售价']
                ))
        
        def show_detail():
            """显示选中商品的详细信息"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个商品")
                return
            
            item = tree.item(selected[0])
            com_id = item['values'][0]
            
            commodity = self.system.excel_manager.get_commodity_by_id(com_id)
            if commodity is None:
                messagebox.showerror("错误", "未找到该商品")
                return
            
            info_top = tk.Toplevel(top)
            info_top.title("商品详情")
            info_top.geometry("700x500")
            info_top.configure(bg=Styles.BACKGROUND_COLOR)
            
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
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Button(btn_frame, text="搜索", 
                 font=Styles.BUTTON_FONT,
                 width=12,
                 command=search,
                 bg=Styles.PRIMARY_COLOR,
                 fg="white",
                 relief=tk.FLAT,
                 padx=10,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="查看详情", 
                 font=Styles.BUTTON_FONT,
                 width=12,
                 command=show_detail,
                 bg=Styles.SECONDARY_COLOR,
                 fg="white",
                 relief=tk.FLAT,
                 padx=10,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="关闭", 
                 font=Styles.BUTTON_FONT,
                 width=12,
                 command=top.destroy,
                 bg=Styles.ERROR_COLOR,
                 fg="white",
                 relief=tk.FLAT,
                 padx=10,
                 pady=5).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: search())
        
        # 绑定双击事件，双击查看商品详情
        tree.bind('<Double-1>', lambda e: show_detail())

    def sales_management(self):
        """销售管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="销售管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("添加商品到购物车", self.add_to_cart_gui),
            ("查看购物车", self.view_cart_gui),
            ("清空购物车", self.clear_cart_gui),
            ("结账", self.checkout_gui),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按2行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def add_to_cart_gui(self):
        """添加商品到购物车GUI"""
        top = tk.Toplevel(self.root)
        top.title("添加商品到购物车")
        top.geometry("800x650")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="添加商品到购物车", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 显示可销售的商品
        all_commodities = self.system.excel_manager.get_all_commodities()
        if not all_commodities.empty:
            # 筛选有库存的商品
            available_commodities = all_commodities[all_commodities['当前库存'].astype(float) > 0]
            if not available_commodities.empty:
                # tk.Label(top, text="可销售的商品列表", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
                
                # 创建商品列表框
                list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                list_frame.pack(pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
                
                listbox = tk.Listbox(list_frame, width=80, height=15, font=Styles.TEXT_FONT)
                listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                listbox.config(yscrollcommand=scrollbar.set)
                
                # 填充商品列表
                for idx, (_, row) in enumerate(available_commodities.iterrows()):
                    stock_jin = float(row['当前库存'])
                    stock_ke = stock_jin * 500
                    item_text = f"{idx+1}. {row['商品名称']} (编号: {row['商品编号']}) - 库存: {stock_jin}斤 ({stock_ke}克) - 零售价: {row['零售价']}元/斤"
                    listbox.insert(tk.END, item_text)
                
                # 双击商品填充商品序号到输入框
                def double_click_fill(event):
                    """双击商品填充商品序号到输入框"""
                    try:
                        # 获取双击的索引
                        index = listbox.curselection()
                        if not index:
                            return
                        idx = index[0]
                        
                        if 0 <= idx < len(available_commodities):
                            # 填充商品序号（从1开始）
                            choice_var.set(str(idx + 1))
                            # 聚焦到数量输入框
                            quantity_entry.focus_set()
                    except Exception as e:
                        pass
                
                # 选择商品
                input_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                input_frame.pack(pady=Styles.PADY_MEDIUM)
                
                # 水平排列输入框
                input_row_frame = tk.Frame(input_frame, bg=Styles.BACKGROUND_COLOR)
                input_row_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
                
                # 商品序号
                serial_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                serial_frame.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                tk.Label(serial_frame, text="商品序号: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack()
                choice_var = tk.StringVar()
                tk.Entry(serial_frame, textvariable=choice_var, width=10, font=Styles.TEXT_FONT).pack()
                
                # 购买数量
                quantity_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                quantity_frame.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                tk.Label(quantity_frame, text="购买数量: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack()
                quantity_var = tk.StringVar()
                quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, width=20, font=Styles.TEXT_FONT)
                quantity_entry.pack()
                
                # 购买单位
                unit_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                unit_frame.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                tk.Label(unit_frame, text="单位 (1-斤, 2-克): ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack()
                unit_var = tk.StringVar(value="2")
                tk.Entry(unit_frame, textvariable=unit_var, width=10, font=Styles.TEXT_FONT).pack()
                
                # 绑定双击事件
                listbox.bind('<Double-1>', double_click_fill)
                
                def add_to_cart():
                    try:
                        choice = int(choice_var.get()) - 1
                        if 0 <= choice < len(available_commodities):
                            selected_commodity = available_commodities.iloc[choice]
                            com_id = selected_commodity['商品编号']
                            com_name = selected_commodity['商品名称']
                            retail_price = float(selected_commodity['零售价'])
                            current_stock = float(selected_commodity['当前库存'])
                            
                            quantity = float(quantity_var.get())
                            unit_choice = unit_var.get()
                            unit = "斤" if unit_choice == "1" else "克"
                            
                            # 检查库存
                            if unit == "斤":
                                if quantity > current_stock:
                                    messagebox.showerror("错误", "库存不足！")
                                    return
                            else:
                                if quantity > current_stock * 500:
                                    messagebox.showerror("错误", "库存不足！")
                                    return
                            
                            # 添加到购物车
                            cart_item = {
                                '商品编号': com_id,
                                '商品名称': com_name,
                                '单价(每斤)': retail_price,
                                '购买数量': quantity,
                                '购买单位': unit,
                                '小计': (quantity / 500) * retail_price if unit == "克" else quantity * retail_price
                            }
                            
                            # 检查是否已存在
                            existing = False
                            for item in self.system.shopping_cart:
                                if item['商品编号'] == com_id:
                                    item['购买数量'] = quantity
                                    item['购买单位'] = unit
                                    item['小计'] = (quantity / 500) * retail_price if unit == "克" else quantity * retail_price
                                    existing = True
                                    break
                            
                            if not existing:
                                self.system.shopping_cart.append(cart_item)
                            
                            messagebox.showinfo("成功", f"已添加到购物车！\n商品: {com_name}\n数量: {quantity} {unit}")
                            top.destroy()
                        else:
                            messagebox.showerror("错误", "无效的选择")
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数字")
                
                btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                btn_frame.pack(pady=Styles.PADY_MEDIUM)
                
                btn_add = tk.Button(btn_frame, text="添加到购物车", font=Styles.BUTTON_FONT,
                          width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=add_to_cart,
                          bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                btn_add.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                btn_add.bind("<Enter>", lambda e, b=btn_add: b.config(bg=Styles.BUTTON_HOVER_COLOR))
                btn_add.bind("<Leave>", lambda e, b=btn_add: b.config(bg=Styles.PRIMARY_COLOR))
                
                # 添加取消按钮到同一框架
                btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                          width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                          bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
                btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg="#C0392B"))
                btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.ERROR_COLOR))
            else:
                tk.Label(top, text="暂无可销售的商品", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
                
                # 为无商品情况添加取消按钮
                btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                btn_frame.pack(pady=Styles.PADY_MEDIUM)
                btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                          width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                          bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                btn_cancel.pack()
                btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg="#C0392B"))
                btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.ERROR_COLOR))
        else:
            tk.Label(top, text="暂无商品信息", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
            
            # 为无商品信息情况添加取消按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_cancel.pack()
            btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg="#C0392B"))
            btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.ERROR_COLOR))

    def view_cart_gui(self):
        """查看购物车GUI"""
        top = tk.Toplevel(self.root)
        top.title("购物车")
        top.geometry("800x600")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="购物车", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        if not self.system.shopping_cart:
            tk.Label(top, text="购物车为空", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
        else:
            tk.Label(top, text="购物车商品", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
            
            frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            frame.pack(pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
            
            tree = ttk.Treeview(frame, style="Treeview")
            tree["columns"] = ["商品编号", "商品名称", "单价(每斤)", "数量", "单位", "小计"]
            tree["show"] = "headings"
            
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.CENTER)
            
            total = 0
            for item in self.system.shopping_cart:
                tree.insert("", tk.END, values=[
                    item['商品编号'],
                    item['商品名称'],
                    item['单价(每斤)'],
                    item['购买数量'],
                    item['购买单位'],
                    item['小计']
                ])
                total += item['小计']
            
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            tk.Label(top, text=f"总计: {total:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_MEDIUM)
            
            # 双击修改商品数量
            def double_click_modify(event):
                """双击修改商品数量"""
                selected = tree.selection()
                if not selected:
                    return
                
                item = tree.item(selected[0])
                values = item['values']
                com_id = values[0]
                current_quantity = values[3]
                unit = values[4]
                
                # 查找对应的购物车项目
                for cart_item in self.system.shopping_cart:
                    if cart_item['商品编号'] == com_id:
                        # 弹出输入框修改数量
                        new_quantity = simpledialog.askfloat(
                            "修改数量", 
                            f"请输入新的购买数量 ({unit}):",
                            initialvalue=current_quantity,
                            minvalue=0.1
                        )
                        
                        if new_quantity is not None:
                            # 更新购物车
                            cart_item['购买数量'] = new_quantity
                            cart_item['小计'] = (new_quantity / 500) * cart_item['单价(每斤)'] if unit == "克" else new_quantity * cart_item['单价(每斤)']
                            
                            # 重新显示购物车
                            top.destroy()
                            self.view_cart_gui()
                        break
            
            # 绑定双击事件
            tree.bind('<Double-1>', double_click_modify)
            
            # 删除选中商品
            def delete_selected():
                """删除选中的商品"""
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("提示", "请先选择要删除的商品")
                    return
                
                item = tree.item(selected[0])
                values = item['values']
                com_id = values[0]
                com_name = values[1]
                
                if messagebox.askyesno("确认", f"确定要删除商品 '{com_name}' 吗？"):
                    # 从购物车中删除
                    for i, cart_item in enumerate(self.system.shopping_cart):
                        if cart_item['商品编号'] == com_id:
                            self.system.shopping_cart.pop(i)
                            break
                    
                    # 重新显示购物车
                    top.destroy()
                    self.view_cart_gui()
            
            # 添加按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            
            btn_delete = tk.Button(btn_frame, text="删除选中商品", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=delete_selected,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_delete.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            
            # 添加关闭按钮到同一框架
            btn_close = tk.Button(btn_frame, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            tk.Label(top, text="购物车为空", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_LARGE)
            # 购物车为空时的关闭按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            btn_close = tk.Button(btn_frame, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack()

    def clear_cart_gui(self):
        """清空购物车GUI"""
        if not self.system.shopping_cart:
            messagebox.showinfo("提示", "购物车已经为空")
            return
        
        if messagebox.askyesno("确认", "确定要清空购物车吗？"):
            self.system.shopping_cart.clear()
            messagebox.showinfo("成功", "购物车已清空")

    def checkout_gui(self):
        """结账GUI"""
        if not self.system.shopping_cart:
            messagebox.showerror("错误", "购物车为空，无法结账")
            return
        
        top = tk.Toplevel(self.root)
        top.title("结账")
        top.geometry("600x750")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="结账", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 显示购物车内容
        total_amount = sum(item['小计'] for item in self.system.shopping_cart)
        # tk.Label(top, text="购物车商品", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        
        frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        frame.pack(pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(frame, style="Treeview")
        tree["columns"] = ["商品名称", "数量", "单位", "小计"]
        tree["show"] = "headings"
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        for item in self.system.shopping_cart:
            tree.insert("", tk.END, values=[
                item['商品名称'],
                item['购买数量'],
                item['购买单位'],
                item['小计']
            ])
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Label(top, text=f"应付总额: {total_amount:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_MEDIUM)
        
        input_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        input_frame.pack(pady=Styles.PADY_MEDIUM)
        
        # 客户名称
        tk.Label(input_frame, text="客户名称: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        customer_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=customer_var, width=30, font=Styles.TEXT_FONT).pack(pady=Styles.PADY_SMALL)
        
        # 实收金额
        tk.Label(input_frame, text="实收金额: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        received_var = tk.StringVar(value=str(total_amount))
        tk.Entry(input_frame, textvariable=received_var, width=30, font=Styles.TEXT_FONT).pack(pady=Styles.PADY_SMALL)
        
        def process_checkout():
            customer_name = customer_var.get().strip()
            if not customer_name:
                messagebox.showerror("错误", "请输入客户名称")
                return
            
            try:
                received_amount = float(received_var.get())
                if received_amount < 0:
                    messagebox.showerror("错误", "实收金额不能为负数")
                    return
                
                if received_amount < total_amount:
                    if not messagebox.askyesno("确认", f"实收金额 {received_amount:.2f} 元低于应收金额 {total_amount:.2f} 元，是否继续？"):
                        return
                    discount_ratio = received_amount / total_amount
                else:
                    discount_ratio = 1.0
                
                # 处理销售记录 - 统一以"斤"为单位
                for item in self.system.shopping_cart:
                    sale_id = self.system.excel_manager.generate_id("S", "销售记录", "销售编号")
                    # 将数量转换为斤
                    quantity_in_jin = item['购买数量'] / 500 if item['购买单位'] == "克" else item['购买数量']
                    item_received_amount = item['小计'] * discount_ratio
                    
                    from sale_record import SaleRecord
                    sale_record = SaleRecord(
                        sale_id=sale_id,
                        com_id=item['商品编号'],
                        com_name=item['商品名称'],
                        quantity=quantity_in_jin,  # 统一以斤为单位记录
                        unit_price=item['单价(每斤)'],
                        total_amount=item['小计'],
                        received_amount=item_received_amount,
                        customer_name=customer_name,
                        sale_unit="斤"  # 统一销售单位为斤
                    )
                    self.system.excel_manager.add_sale(sale_record.to_list())
                
                # 注意：add_sale方法中已经会自动更新客户信息，不需要重复调用
                messagebox.showinfo("成功", f"结账成功！\n应付: {total_amount:.2f} 元\n实收: {received_amount:.2f} 元\n折扣: {discount_ratio:.2f}")
                
                # 清空购物车
                self.system.shopping_cart.clear()
                top.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额")
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        
        btn_confirm = tk.Button(btn_frame, text="确认结账", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=process_checkout,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def stock_management(self):
        """进货管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="进货管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("进货入库", self.stock_in_gui),
            ("查看进货记录", self.view_all_stocks),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按1行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def stock_in_gui(self):
        """进货入库GUI"""
        top = tk.Toplevel(self.root)
        top.title("进货入库")
        top.geometry("800x600")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="进货入库", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 显示历史进货记录
        df_stocks = self.system.excel_manager.get_all_stocks()
        if not df_stocks.empty:
            tk.Label(top, text="历史进货记录", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
            
            list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            list_frame.pack(pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
            
            listbox = tk.Listbox(list_frame, width=80, height=10, font=Styles.TEXT_FONT)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            
            for idx, (_, row) in enumerate(df_stocks.iterrows(), 1):
                item_text = f"{idx}. {row['商品名称']} (编号: {row['商品编号']}) - 数量: {row['进货数量']} {row['进货单位']} - 供应商: {row['供应商']}"
                listbox.insert(tk.END, item_text)

        # 输入表单
        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM)

        # 商品编号
        tk.Label(form_frame, text="商品编号 (留空选择历史记录)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=5)
        com_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=com_id_var, width=30, font=Styles.TEXT_FONT).grid(row=0, column=1, pady=5)

        # 进货单价
        tk.Label(form_frame, text="进货单价(每斤)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=1, column=0, sticky='w', pady=5)
        unit_price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=unit_price_var, width=30, font=Styles.TEXT_FONT).grid(row=1, column=1, pady=5)

        # 进货数量
        tk.Label(form_frame, text="进货数量", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=2, column=0, sticky='w', pady=5)
        quantity_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=quantity_var, width=30, font=Styles.TEXT_FONT).grid(row=2, column=1, pady=5)

        # 进货单位
        tk.Label(form_frame, text="进货单位 (斤/克)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=3, column=0, sticky='w', pady=5)
        unit_var = tk.StringVar(value="斤")
        tk.Entry(form_frame, textvariable=unit_var, width=30, font=Styles.TEXT_FONT).grid(row=3, column=1, pady=5)

        # 供应商
        tk.Label(form_frame, text="供应商", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=4, column=0, sticky='w', pady=5)
        supplier_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=supplier_var, width=30, font=Styles.TEXT_FONT).grid(row=4, column=1, pady=5)

        # 进货日期
        tk.Label(form_frame, text="进货日期 (YYYY-MM-DD)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=5, column=0, sticky='w', pady=5)
        stock_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(form_frame, textvariable=stock_date_var, width=30, font=Styles.TEXT_FONT).grid(row=5, column=1, pady=5)

        # 备注
        tk.Label(form_frame, text="备注", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=6, column=0, sticky='w', pady=5)
        remarks_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=remarks_var, width=30, font=Styles.TEXT_FONT).grid(row=6, column=1, pady=5)

        def submit():
            try:
                com_id = com_id_var.get().strip()
                
                if not com_id and not df_stocks.empty:
                    # 从历史记录选择
                    selection = listbox.curselection()
                    if selection:
                        idx = selection[0]
                        selected_product = df_stocks.iloc[idx]
                        com_id = selected_product['商品编号']
                    else:
                        messagebox.showerror("错误", "请输入商品编号或选择历史记录")
                        return
                
                commodity = self.system.excel_manager.get_commodity_by_id(com_id)
                if commodity is None:
                    messagebox.showerror("错误", "商品不存在，请先添加商品")
                    return
                
                unit_price = float(unit_price_var.get())
                quantity = float(quantity_var.get())
                unit = unit_var.get().strip() or "斤"
                supplier = supplier_var.get().strip()
                stock_date = stock_date_var.get().strip() or datetime.now().strftime("%Y-%m-%d")
                remarks = remarks_var.get().strip()
                
                # 自动生成进货编号
                stock_id = self.system.excel_manager.generate_id("I", "进货记录", "进货编号")
                from stock_record import StockRecord
                stock_record = StockRecord(
                    stock_id=stock_id,
                    com_id=com_id,
                    com_name=commodity['商品名称'],
                    quantity=quantity,
                    unit_price=unit_price,
                    supplier=supplier,
                    stock_date=stock_date,
                    remarks=remarks,
                    stock_unit=unit
                )
                
                self.system.excel_manager.add_stock(stock_record.to_list())
                
                # 更新供应商信息
                self.system.excel_manager.update_supplier_after_stock(supplier, quantity * unit_price, stock_date)
                
                messagebox.showinfo("成功", f"进货入库成功！\n进货编号: {stock_id}")
                top.destroy()
            except ValueError as e:
                messagebox.showerror("错误", f"数据输入错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"进货失败: {e}")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        btn_confirm = tk.Button(btn_frame, text="确认进货", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=submit,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def view_all_stocks(self):
        """查看所有进货记录"""
        df = self.system.excel_manager.get_all_stocks()
        self.show_dataframe_window(df, "进货记录列表")

    def supplier_management(self):
        """供应商管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="供应商管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("查看所有供应商", self.view_all_suppliers),
            ("添加供应商", self.add_supplier_gui),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按1行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def view_all_suppliers(self):
        df = self.system.excel_manager.get_all_suppliers()
        # 添加调试信息
        print(f"供应商数据行数: {len(df)}")
        print(f"供应商数据列数: {len(df.columns)}")
        print(f"列名: {list(df.columns)}")
        print(f"是否为空: {df.empty}")
        if not df.empty:
            print("前5行数据:")
            print(df.head())
        # 显示供应商数据的基本信息
        self.show_dataframe_window(df, "供应商列表")

    def add_supplier_gui(self):
        """添加供应商GUI"""
        top = tk.Toplevel(self.root)
        top.title("添加供应商")
        top.geometry("600x400")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="添加供应商", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM)

        # 供应商编号
        tk.Label(form_frame, text="供应商编号 (留空自动生成)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=5)
        supplier_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=supplier_id_var, width=30, font=Styles.TEXT_FONT).grid(row=0, column=1, pady=5)

        # 供应商名称
        tk.Label(form_frame, text="供应商名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=1, column=0, sticky='w', pady=5)
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, width=30, font=Styles.TEXT_FONT).grid(row=1, column=1, pady=5)

        # 联系人
        tk.Label(form_frame, text="联系人", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=2, column=0, sticky='w', pady=5)
        contact_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=contact_var, width=30, font=Styles.TEXT_FONT).grid(row=2, column=1, pady=5)

        # 联系电话
        tk.Label(form_frame, text="联系电话", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=3, column=0, sticky='w', pady=5)
        phone_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=phone_var, width=30, font=Styles.TEXT_FONT).grid(row=3, column=1, pady=5)

        # 地址
        tk.Label(form_frame, text="地址", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=4, column=0, sticky='w', pady=5)
        address_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=address_var, width=30, font=Styles.TEXT_FONT).grid(row=4, column=1, pady=5)

        # 备注
        tk.Label(form_frame, text="备注", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=5, column=0, sticky='w', pady=5)
        remarks_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=remarks_var, width=30, font=Styles.TEXT_FONT).grid(row=5, column=1, pady=5)

        def submit():
            try:
                supplier_id_input = supplier_id_var.get().strip()
                if supplier_id_input:
                    supplier_id = supplier_id_input
                    df = self.system.excel_manager.get_all_suppliers()
                    if not df.empty:
                        existing = df[df['供应商编号'] == supplier_id]
                        if not existing.empty:
                            messagebox.showerror("错误", "该供应商编号已存在！")
                            return
                else:
                    supplier_id = self.system.excel_manager.generate_id("SP", "供应商", "供应商编号")

                name = name_var.get().strip()
                contact_person = contact_var.get().strip()
                phone = phone_var.get().strip()
                address = address_var.get().strip()
                remarks = remarks_var.get().strip()

                from supplier import Supplier
                supplier = Supplier(
                    supplier_id=supplier_id,
                    name=name,
                    contact_person=contact_person,
                    phone=phone,
                    address=address,
                    remarks=remarks
                )

                self.system.excel_manager.add_supplier(supplier.to_list())
                messagebox.showinfo("成功", f"供应商添加成功！\n供应商编号: {supplier_id}")
                top.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        btn_confirm = tk.Button(btn_frame, text="确认添加", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=submit,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def update_supplier_gui(self):
        """修改供应商GUI"""
        top = tk.Toplevel(self.root)
        top.title("修改供应商")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="修改供应商", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入供应商编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        supplier_id_var = tk.StringVar()
        tk.Entry(top, textvariable=supplier_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def search():
            supplier_id = supplier_id_var.get().strip()
            df = self.system.excel_manager.get_all_suppliers()
            if df.empty:
                messagebox.showerror("错误", "未找到供应商信息")
                return

            supplier = df[df['供应商编号'] == supplier_id]
            if supplier.empty:
                messagebox.showerror("错误", "未找到该供应商")
                return

            supplier_row = supplier.iloc[0]

            # 创建修改窗口
            edit_top = tk.Toplevel(top)
            edit_top.title("修改供应商信息")
            edit_top.geometry("600x400")
            edit_top.configure(bg=Styles.BACKGROUND_COLOR)

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

        btn_frame_top = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame_top.pack(pady=Styles.PADY_MEDIUM)
        btn_search = tk.Button(btn_frame_top, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=search,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_search.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_search.bind("<Enter>", lambda e, b=btn_search: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_search.bind("<Leave>", lambda e, b=btn_search: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel_top = tk.Button(btn_frame_top, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel_top.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def delete_supplier_gui(self):
        """删除供应商GUI"""
        top = tk.Toplevel(self.root)
        top.title("删除供应商")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="删除供应商", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入供应商编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        supplier_id_var = tk.StringVar()
        tk.Entry(top, textvariable=supplier_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def delete():
            supplier_id = supplier_id_var.get().strip()
            df = self.system.excel_manager.get_all_suppliers()
            if df.empty:
                messagebox.showerror("错误", "未找到供应商信息")
                return

            supplier = df[df['供应商编号'] == supplier_id]
            if supplier.empty:
                messagebox.showerror("错误", "未找到该供应商")
                return

            supplier_row = supplier.iloc[0]
            if messagebox.askyesno("确认", f"确定要删除供应商 '{supplier_row['供应商名称']}' 吗？"):
                # 删除供应商
                new_df = df[df['供应商编号'] != supplier_id]
                self.system.excel_manager.write_sheet("供应商", new_df)
                messagebox.showinfo("成功", "供应商删除成功！")
                top.destroy()

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        btn_delete = tk.Button(btn_frame, text="删除", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=delete,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_delete.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.PRIMARY_COLOR))

    def customer_management(self):
        """客户管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="客户管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("查看所有客户", self.view_all_customers),
            ("添加客户", self.add_customer_gui),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按1行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def view_all_customers(self):
        df = self.system.excel_manager.get_all_customers()
        self.show_dataframe_window(df, "客户列表")

    def add_customer_gui(self):
        """添加客户GUI"""
        top = tk.Toplevel(self.root)
        top.title("添加客户")
        top.geometry("600x400")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="添加客户", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        form_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_frame.pack(pady=Styles.PADY_MEDIUM, padx=Styles.PADX_MEDIUM)

        # 客户编号
        tk.Label(form_frame, text="客户编号 (留空自动生成)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=5)
        customer_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=customer_id_var, width=30, font=Styles.TEXT_FONT).grid(row=0, column=1, pady=5)

        # 客户名称
        tk.Label(form_frame, text="客户名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=1, column=0, sticky='w', pady=5)
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, width=30, font=Styles.TEXT_FONT).grid(row=1, column=1, pady=5)

        # 联系电话
        tk.Label(form_frame, text="联系电话", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=2, column=0, sticky='w', pady=5)
        phone_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=phone_var, width=30, font=Styles.TEXT_FONT).grid(row=2, column=1, pady=5)

        # 地址
        tk.Label(form_frame, text="地址", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=3, column=0, sticky='w', pady=5)
        address_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=address_var, width=30, font=Styles.TEXT_FONT).grid(row=3, column=1, pady=5)

        # 累计消费
        tk.Label(form_frame, text="累计消费", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=4, column=0, sticky='w', pady=5)
        total_purchases_var = tk.StringVar(value="0")
        tk.Entry(form_frame, textvariable=total_purchases_var, width=30, font=Styles.TEXT_FONT).grid(row=4, column=1, pady=5)

        def submit():
            try:
                customer_id_input = customer_id_var.get().strip()
                if customer_id_input:
                    customer_id = customer_id_input
                    df = self.system.excel_manager.get_all_customers()
                    if not df.empty:
                        existing = df[df['客户编号'] == customer_id]
                        if not existing.empty:
                            messagebox.showerror("错误", "该客户编号已存在！")
                            return
                else:
                    customer_id = self.system.excel_manager.generate_id("CU", "客户", "客户编号")

                name = name_var.get().strip()
                phone = phone_var.get().strip()
                address = address_var.get().strip()
                total_purchases = float(total_purchases_var.get())

                from customer import Customer
                customer = Customer(
                    customer_id=customer_id,
                    name=name,
                    phone=phone,
                    address=address,
                    total_purchases=total_purchases
                )

                # 自动计算客户等级
                customer.update_customer_level()

                self.system.excel_manager.add_customer(customer.to_list())
                messagebox.showinfo("成功", f"客户添加成功！\n客户编号: {customer_id}\n客户等级: {customer.customer_level}")
                top.destroy()
            except ValueError as e:
                messagebox.showerror("错误", f"数据输入错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {e}")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        btn_confirm = tk.Button(btn_frame, text="确认添加", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=submit,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def update_customer_gui(self):
        """修改客户GUI"""
        top = tk.Toplevel(self.root)
        top.title("修改客户")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="修改客户", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入客户编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        customer_id_var = tk.StringVar()
        tk.Entry(top, textvariable=customer_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def search():
            customer_id = customer_id_var.get().strip()
            df = self.system.excel_manager.get_all_customers()
            if df.empty:
                messagebox.showerror("错误", "未找到客户信息")
                return

            customer = df[df['客户编号'] == customer_id]
            if customer.empty:
                messagebox.showerror("错误", "未找到该客户")
                return

            customer_row = customer.iloc[0]

            # 创建修改窗口
            edit_top = tk.Toplevel(top)
            edit_top.title("修改客户信息")
            edit_top.geometry("600x400")
            edit_top.configure(bg=Styles.BACKGROUND_COLOR)

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
                ("地址", "地址", customer_row['地址']),
                ("累计消费", "累计消费", customer_row['累计消费'])
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
                    if value:
                        if key == '累计消费':
                            updates[key] = float(value)
                        else:
                            updates[key] = value

                if updates:
                    # 获取所有客户数据
                    all_customers = self.system.excel_manager.get_all_customers()
                    # 找到要修改的客户
                    idx = all_customers[all_customers['客户编号'] == customer_id].index
                    if len(idx) > 0:
                        # 更新数据
                        for key, value in updates.items():
                            all_customers.at[idx[0], key] = value
                        
                        # 重新计算客户等级
                        total_purchases = updates.get('累计消费', customer_row['累计消费'])
                        if total_purchases >= 5000:
                            customer_level = "VIP客户"
                        elif total_purchases >= 2000:
                            customer_level = "高级客户"
                        elif total_purchases >= 1000:
                            customer_level = "中级客户"
                        else:
                            customer_level = "普通客户"
                        all_customers.at[idx[0], '客户等级'] = customer_level
                        
                        # 写回Excel
                        self.system.excel_manager.write_sheet("客户", all_customers)
                        messagebox.showinfo("成功", "客户信息更新成功！")
                        edit_top.destroy()
                        top.destroy()
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

        btn_frame_top = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame_top.pack(pady=Styles.PADY_MEDIUM)
        btn_search = tk.Button(btn_frame_top, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=search,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_search.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_search.bind("<Enter>", lambda e, b=btn_search: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_search.bind("<Leave>", lambda e, b=btn_search: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel_top = tk.Button(btn_frame_top, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel_top.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def delete_customer_gui(self):
        """删除客户GUI"""
        top = tk.Toplevel(self.root)
        top.title("删除客户")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="删除客户", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入客户编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        customer_id_var = tk.StringVar()
        tk.Entry(top, textvariable=customer_id_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def delete():
            customer_id = customer_id_var.get().strip()
            df = self.system.excel_manager.get_all_customers()
            if df.empty:
                messagebox.showerror("错误", "未找到客户信息")
                return

            customer = df[df['客户编号'] == customer_id]
            if customer.empty:
                messagebox.showerror("错误", "未找到该客户")
                return

            customer_row = customer.iloc[0]
            if messagebox.askyesno("确认", f"确定要删除客户 '{customer_row['客户名称']}' 吗？"):
                # 删除客户
                new_df = df[df['客户编号'] != customer_id]
                self.system.excel_manager.write_sheet("客户", new_df)
                messagebox.showinfo("成功", "客户删除成功！")
                top.destroy()

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        btn_delete = tk.Button(btn_frame, text="删除", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=delete,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_delete.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_cancel.bind("<Enter>", lambda e, b=btn_cancel: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_cancel.bind("<Leave>", lambda e, b=btn_cancel: b.config(bg=Styles.PRIMARY_COLOR))

    def view_all_customers(self):
        df = self.system.excel_manager.get_all_customers()
        self.show_dataframe_window(df, "客户列表")

    def sales_record_management(self):
        """销售记录管理界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="销售记录管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("查看所有销售记录", self.view_all_sales),
            ("按客户查询", self.query_sales_by_customer_gui),
            ("按商品查询", self.query_sales_by_product_gui),
            ("按日期查询", self.query_sales_by_date_gui),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按2行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def view_all_sales(self):
        df = self.system.excel_manager.get_all_sales()
        self.show_dataframe_window(df, "销售记录列表")

    def query_sales_by_customer_gui(self):
        """按客户查询销售记录GUI"""
        top = tk.Toplevel(self.root)
        top.title("按客户查询销售记录")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="按客户查询销售记录", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入客户名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        customer_var = tk.StringVar()
        tk.Entry(top, textvariable=customer_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def query():
            customer_name = customer_var.get().strip()
            if not customer_name:
                messagebox.showerror("错误", "请输入客户名称")
                return

            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            filtered_df = df[df['客户名称'] == customer_name]
            if filtered_df.empty:
                messagebox.showinfo("提示", f"未找到客户 '{customer_name}' 的销售记录")
                return

            self.show_dataframe_window(filtered_df, f"{customer_name} 的销售记录")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        btn_query = tk.Button(btn_frame, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=query,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_query.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_query.bind("<Enter>", lambda e, b=btn_query: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_query.bind("<Leave>", lambda e, b=btn_query: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def query_sales_by_product_gui(self):
        """按商品查询销售记录GUI"""
        top = tk.Toplevel(self.root)
        top.title("按商品查询销售记录")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="按商品查询销售记录", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="请输入商品编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        product_var = tk.StringVar()
        tk.Entry(top, textvariable=product_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def query():
            product_id = product_var.get().strip()
            if not product_id:
                messagebox.showerror("错误", "请输入商品编号")
                return

            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            filtered_df = df[df['商品编号'] == product_id]
            if filtered_df.empty:
                messagebox.showinfo("提示", f"未找到商品编号 '{product_id}' 的销售记录")
                return

            self.show_dataframe_window(filtered_df, f"商品编号 {product_id} 的销售记录")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        btn_query = tk.Button(btn_frame, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=query,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_query.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_query.bind("<Enter>", lambda e, b=btn_query: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_query.bind("<Leave>", lambda e, b=btn_query: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def query_sales_by_date_gui(self):
        """按日期查询销售记录GUI"""
        top = tk.Toplevel(self.root)
        top.title("按日期查询销售记录")
        top.geometry("400x400")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="按日期查询销售记录", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="开始日期 (YYYY-MM-DD)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        start_date_var = tk.StringVar()
        tk.Entry(top, textvariable=start_date_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        tk.Label(top, text="结束日期 (YYYY-MM-DD)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_SMALL)
        end_date_var = tk.StringVar()
        tk.Entry(top, textvariable=end_date_var, font=Styles.TEXT_FONT, width=30).pack(pady=Styles.PADY_SMALL)

        def query():
            start_date = start_date_var.get().strip()
            end_date = end_date_var.get().strip()

            if not start_date or not end_date:
                messagebox.showerror("错误", "请输入开始和结束日期")
                return

            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            # 确保销售日期列是日期类型
            df['销售日期'] = pd.to_datetime(df['销售日期'], errors='coerce')

            # 过滤日期范围
            filtered_df = df[(df['销售日期'] >= start_date) & (df['销售日期'] <= end_date)]
            if filtered_df.empty:
                messagebox.showinfo("提示", f"{start_date} 到 {end_date} 期间未找到销售记录")
                return

            self.show_dataframe_window(filtered_df, f"{start_date} 到 {end_date} 的销售记录")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)
        btn_query = tk.Button(btn_frame, text="查询", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=query,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_query.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        btn_query.bind("<Enter>", lambda e, b=btn_query: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_query.bind("<Leave>", lambda e, b=btn_query: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)

    def statistics_analysis(self):
        """统计分析界面"""
        self.clear_window()
        
        # 创建标题区域
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="统计分析", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建按钮区域
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM, fill=tk.X)
        
        # 创建按钮网格
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(padx=Styles.PADX_LARGE)

        buttons = [
            ("销售统计", self.sales_statistics_gui),
            ("热销商品排行", self.top_selling_products_gui),
            ("盈利分析", self.profit_analysis_gui),
            ("数据可视化", self.data_visualization_gui),
            ("返回主菜单", self.create_main_menu)
        ]

        # 按2行3列排列按钮
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            # 添加悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

    def sales_statistics_gui(self):
        """销售统计GUI"""
        top = tk.Toplevel(self.root)
        top.title("销售统计")
        top.geometry("800x600")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="销售统计", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 销售统计维度选择
        tk.Label(top, text="选择统计维度", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_MEDIUM)

        button_grid = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(pady=Styles.PADY_MEDIUM)

        buttons = [
            ("按茶类统计", lambda: self.statistics_by_dimension("茶类")),
            ("按品种统计", lambda: self.statistics_by_dimension("品种")),
            ("按商品统计", lambda: self.statistics_by_dimension("商品")),
            ("按时间统计", self.statistics_by_time_gui)
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(button_grid, text=text, font=Styles.BUTTON_FONT,
                            width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=command,
                            bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))

        btn_close = tk.Button(top, text="关闭", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_close.pack(pady=Styles.PADY_LARGE)

    def statistics_by_dimension(self, dimension):
        """按维度统计"""
        try:
            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            # 获取商品信息
            commodity_df = self.system.excel_manager.get_all_commodities()
            if commodity_df.empty:
                messagebox.showinfo("提示", "暂无商品信息，无法进行详细统计")
                return

            # 合并数据
            merged_df = pd.merge(df, commodity_df[["商品编号", "茶类", "品种", "成本价"]], 
                               on="商品编号", how="left")

            # 计算销售数量（转换为斤）- 使用向量化操作
            unit_is_gram = merged_df.get('销售单位', '斤') == '克'
            merged_df['销售数量(斤)'] = merged_df['销售数量']
            merged_df.loc[unit_is_gram, '销售数量(斤)'] = merged_df.loc[unit_is_gram, '销售数量'] / 500
            merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
            merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']

            if dimension == "茶类":
                if '茶类' in merged_df.columns:
                    stats = merged_df.groupby('茶类').agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum',
                        '利润': 'sum'
                    }).round(2)
                    stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
                    # 将索引转换为列
                    stats = stats.reset_index()
                    self.show_dataframe_window(stats, "按茶类统计")
                else:
                    messagebox.showinfo("提示", "暂无茶类信息")
            elif dimension == "品种":
                if '品种' in merged_df.columns:
                    stats = merged_df.groupby('品种').agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum',
                        '利润': 'sum'
                    }).round(2)
                    stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
                    # 将索引转换为列
                    stats = stats.reset_index()
                    self.show_dataframe_window(stats, "按品种统计")
                else:
                    messagebox.showinfo("提示", "暂无品种信息")
            elif dimension == "商品":
                if '商品名称' in merged_df.columns:
                    stats = merged_df.groupby(['商品编号', '商品名称']).agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum',
                        '利润': 'sum'
                    }).round(2)
                    stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
                    # 将索引转换为列
                    stats = stats.reset_index()
                    self.show_dataframe_window(stats, "按商品统计")
                else:
                    messagebox.showinfo("提示", "暂无商品名称信息")
        except Exception as e:
            messagebox.showerror("错误", f"统计失败: {e}")

    def statistics_by_time_gui(self):
        """按时间统计GUI"""
        top = tk.Toplevel(self.root)
        top.title("按时间统计")
        top.geometry("900x400")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_MEDIUM)
        
        tk.Label(
            title_frame, 
            text="按时间统计", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        tk.Label(top, text="选择时间维度", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.PADY_MEDIUM)

        button_grid = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack(pady=Styles.PADY_SMALL)

        buttons = [
            ("按日统计", lambda: self.statistics_by_time("日")),
            ("按周统计", lambda: self.statistics_by_time("周")),
            ("按月统计", lambda: self.statistics_by_time("月"))
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_grid, text=text, font=Styles.BUTTON_FONT,
                            width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=command,
                            bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn.grid(row=0, column=i, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))

        btn_close = tk.Button(top, text="关闭", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_close.pack(pady=Styles.PADY_LARGE)

    def statistics_by_time(self, time_unit):
        """按时间单位统计"""
        try:
            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            # 转换销售日期为日期类型
            df['销售日期'] = pd.to_datetime(df['销售日期'], errors='coerce')

            # 计算销售数量（转换为斤）
            def calculate_quantity(row):
                quantity = row['销售数量']
                unit = row.get('销售单位', '斤')
                return quantity / 500 if unit == '克' else quantity

            df['销售数量(斤)'] = df.apply(calculate_quantity, axis=1)

            # 获取商品信息计算成本
            commodity_df = self.system.excel_manager.get_all_commodities()
            if not commodity_df.empty:
                merged_df = pd.merge(df, commodity_df[["商品编号", "成本价"]], 
                                   on="商品编号", how="left")
                merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
                merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']
            else:
                merged_df = df
                merged_df['销售成本'] = 0
                merged_df['利润'] = merged_df['实收金额']

            # 按时间分组
            if time_unit == "日":
                grouped = merged_df.groupby(merged_df['销售日期'].dt.date)
            elif time_unit == "周":
                grouped = merged_df.groupby(merged_df['销售日期'].dt.to_period('W'))
            elif time_unit == "月":
                grouped = merged_df.groupby(merged_df['销售日期'].dt.to_period('M'))

            stats = grouped.agg({
                '销售数量(斤)': 'sum',
                '实收金额': 'sum',
                '销售成本': 'sum',
                '利润': 'sum'
            }).round(2)
            stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
            # 将索引转换为列
            stats = stats.reset_index()
            # 重命名时间列
            stats = stats.rename(columns={'index': f'{time_unit}期'})

            self.show_dataframe_window(stats, f"按{time_unit}统计")
        except Exception as e:
            messagebox.showerror("错误", f"统计失败: {e}")

    def top_selling_products_gui(self):
        """热销商品排行GUI"""
        try:
            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            # 计算销售数量（转换为斤）
            def calculate_quantity(row):
                quantity = row['销售数量']
                unit = row.get('销售单位', '斤')
                return quantity / 500 if unit == '克' else quantity

            df['销售数量(斤)'] = df.apply(calculate_quantity, axis=1)

            # 按商品分组
            stats = df.groupby(['商品编号', '商品名称']).agg({
                '销售数量(斤)': 'sum',
                '实收金额': 'sum'
            }).round(2)

            # 按销售数量排序
            stats = stats.sort_values(by='销售数量(斤)', ascending=False).head(10)
            # 将索引转换为列
            stats = stats.reset_index()

            self.show_dataframe_window(stats, "热销商品排行")
        except Exception as e:
            messagebox.showerror("错误", f"统计失败: {e}")

    def profit_analysis_gui(self):
        """盈利分析GUI"""
        try:
            df = self.system.excel_manager.get_all_sales()
            if df.empty:
                messagebox.showinfo("提示", "暂无销售记录")
                return

            # 获取商品信息
            commodity_df = self.system.excel_manager.get_all_commodities()
            if commodity_df.empty:
                messagebox.showinfo("提示", "暂无商品信息，无法进行盈利分析")
                return

            # 合并数据
            merged_df = pd.merge(df, commodity_df[["商品编号", "成本价"]], 
                               on="商品编号", how="left")

            # 计算销售数量（转换为斤）- 使用向量化操作
            unit_is_gram = merged_df.get('销售单位', '斤') == '克'
            merged_df['销售数量(斤)'] = merged_df['销售数量']
            merged_df.loc[unit_is_gram, '销售数量(斤)'] = merged_df.loc[unit_is_gram, '销售数量'] / 500
            merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
            merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']

            # 计算总体盈利情况
            total_income = merged_df['实收金额'].sum()
            total_cost = merged_df['销售成本'].sum()
            total_profit = merged_df['利润'].sum()
            profit_margin = (total_profit / total_income * 100) if total_income > 0 else 0

            # 显示盈利分析结果
            result_window = tk.Toplevel(self.root)
            result_window.title("盈利分析")
            result_window.geometry("600x400")
            result_window.configure(bg=Styles.BACKGROUND_COLOR)

            # 创建标题区域
            result_title_frame = tk.Frame(result_window, bg=Styles.BACKGROUND_COLOR)
            result_title_frame.pack(pady=Styles.PADY_MEDIUM)
            
            tk.Label(
                result_title_frame, 
                text="盈利分析结果", 
                font=Styles.SUB_HEADER_FONT,
                bg=Styles.BACKGROUND_COLOR,
                fg=Styles.HEADER_COLOR
            ).pack()

            frame = tk.Frame(result_window, bg=Styles.BACKGROUND_COLOR)
            frame.pack(pady=Styles.PADY_MEDIUM)

            tk.Label(frame, text=f"总销售收入: {total_income:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=5)
            tk.Label(frame, text=f"总销售成本: {total_cost:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=5)
            tk.Label(frame, text=f"总利润: {total_profit:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=5)
            tk.Label(frame, text=f"利润率: {profit_margin:.2f}%", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=5)

            # 显示按商品的盈利情况
            product_profit = merged_df.groupby(['商品编号', '商品名称']).agg({
                '销售数量(斤)': 'sum',
                '实收金额': 'sum',
                '销售成本': 'sum',
                '利润': 'sum'
            }).round(2)
            product_profit['利润率(%)'] = (product_profit['利润'] / product_profit['实收金额'] * 100).round(2)
            product_profit = product_profit.sort_values(by='利润', ascending=False)
            # 将索引转换为列
            product_profit = product_profit.reset_index()

            btn_frame = tk.Frame(result_window, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.PADY_MEDIUM)
            btn_product_detail = tk.Button(btn_frame, text="查看商品盈利详情", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=lambda: self.show_dataframe_window(product_profit, "商品盈利详情"),
                      bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_product_detail.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
            btn_product_detail.bind("<Enter>", lambda e, b=btn_product_detail: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn_product_detail.bind("<Leave>", lambda e, b=btn_product_detail: b.config(bg=Styles.PRIMARY_COLOR))
            
            btn_close = tk.Button(btn_frame, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=result_window.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack(side=tk.LEFT, padx=Styles.PADX_SMALL)
        except Exception as e:
            messagebox.showerror("错误", f"分析失败: {e}")

    def data_visualization_gui(self):
        """数据可视化GUI"""
        top = tk.Toplevel(self.root)
        top.title("数据可视化")
        top.geometry("800x600")
        top.configure(bg=Styles.BACKGROUND_COLOR)

        tk.Label(top, text="选择可视化类型", font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_LARGE)

        frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        frame.pack(pady=Styles.PADY_MEDIUM)
        
        button_grid = tk.Frame(frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack()

        buttons = [
            ("销售趋势图", self.show_sales_trend_options),
            ("商品销量饼图", lambda: self.system.data_viz.plot_product_sales_pie()),
            ("利润趋势图", self.show_profit_trend_options),
            ("茶类销售对比图", lambda: self.system.data_viz.plot_tea_category_sales())
        ]

        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(button_grid, text=text, font=Styles.BUTTON_FONT,
                            width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                            command=command, bg=Styles.PRIMARY_COLOR, fg="white",
                            relief=tk.FLAT, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            btn.grid(row=row, column=col, padx=Styles.PADX_SMALL, pady=Styles.PADY_SMALL)

        tk.Button(top, text="关闭", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT,
                  command=top.destroy, bg=Styles.ERROR_COLOR, fg="white",
                  relief=tk.FLAT, padx=10, pady=5).pack(pady=Styles.PADY_LARGE)
    
    def show_sales_trend_options(self):
        """显示销售趋势图选项"""
        top = tk.Toplevel(self.root)
        top.title("销售趋势图 - 选择时间周期")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        tk.Label(top, text="选择时间周期", font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_LARGE)
        
        frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        frame.pack(pady=Styles.PADY_MEDIUM)
        
        buttons = [
            ("按日", lambda: self.plot_with_close(top, 'day')),
            ("按周", lambda: self.plot_with_close(top, 'week')),
            ("按月", lambda: self.plot_with_close(top, 'month'))
        ]
        
        for text, command in buttons:
            btn = tk.Button(frame, text=text, font=Styles.BUTTON_FONT,
                            width=15, height=2, command=command,
                            bg=Styles.PRIMARY_COLOR, fg="white",
                            relief=tk.FLAT, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            btn.pack(pady=Styles.PADY_SMALL)
        
        tk.Button(top, text="取消", font=Styles.BUTTON_FONT,
                  width=15, height=2, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white",
                  relief=tk.FLAT, padx=10, pady=5).pack(pady=Styles.PADY_MEDIUM)
    
    def show_profit_trend_options(self):
        """显示利润趋势图选项"""
        top = tk.Toplevel(self.root)
        top.title("利润趋势图 - 选择时间周期")
        top.geometry("400x300")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        tk.Label(top, text="选择时间周期", font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.PADY_LARGE)
        
        frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        frame.pack(pady=Styles.PADY_MEDIUM)
        
        buttons = [
            ("按日", lambda: self.plot_profit_with_close(top, 'day')),
            ("按周", lambda: self.plot_profit_with_close(top, 'week')),
            ("按月", lambda: self.plot_profit_with_close(top, 'month'))
        ]
        
        for text, command in buttons:
            btn = tk.Button(frame, text=text, font=Styles.BUTTON_FONT,
                            width=15, height=2, command=command,
                            bg=Styles.PRIMARY_COLOR, fg="white",
                            relief=tk.FLAT, padx=10, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            btn.pack(pady=Styles.PADY_SMALL)
        
        tk.Button(top, text="取消", font=Styles.BUTTON_FONT,
                  width=15, height=2, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white",
                  relief=tk.FLAT, padx=10, pady=5).pack(pady=Styles.PADY_MEDIUM)
    
    def plot_with_close(self, window, period):
        """绘制图表并关闭窗口"""
        window.destroy()
        self.system.data_viz.plot_sales_trend(period)
    
    def plot_profit_with_close(self, window, period):
        """绘制利润图表并关闭窗口"""
        window.destroy()
        self.system.data_viz.plot_profit_trend(period)

    def show_dataframe_window(self, df, title):
        """显示DataFrame的窗口（带分页功能）"""
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")
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
                if commodity:
                    info_top = tk.Toplevel(top)
                    info_top.title("商品详情")
                    info_top.geometry("700x500")
                    info_top.configure(bg=Styles.BACKGROUND_COLOR)
                    
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
                        edit_top = tk.Toplevel(top)
                        edit_top.title("修改供应商信息")
                        edit_top.geometry("600x400")
                        edit_top.configure(bg=Styles.BACKGROUND_COLOR)
                        
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
                        edit_top = tk.Toplevel(top)
                        edit_top.title("修改客户信息")
                        edit_top.geometry("600x500")
                        edit_top.configure(bg=Styles.BACKGROUND_COLOR)
                        
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

    def system_management(self):
        """系统管理界面"""
        self.clear_window()
        
        title_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_LARGE)
        
        tk.Label(
            title_frame, 
            text="系统管理", 
            font=Styles.HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()
        
        buttons_frame = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        buttons_frame.pack(pady=Styles.PADY_MEDIUM)
        
        button_grid = tk.Frame(buttons_frame, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack()
        
        buttons = [
            ("数据备份管理", self.backup_management),
            ("云端同步管理", self.cloud_sync_management),
            ("操作日志查询", self.log_management),
            ("返回主菜单", self.create_main_menu),
            ("退出系统", self.root.quit)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                button_grid, 
                text=text, 
                font=Styles.BUTTON_FONT,
                width=Styles.BUTTON_WIDTH,
                height=Styles.BUTTON_HEIGHT,
                command=command,
                bg=Styles.PRIMARY_COLOR,
                fg="white",
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Styles.BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Styles.PRIMARY_COLOR))
            btn.grid(row=i, column=0, pady=Styles.PADY_SMALL)
    
    def backup_management(self):
        """数据备份管理界面"""
        top = tk.Toplevel(self.root)
        top.title("数据备份管理")
        top.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="数据备份管理", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_SMALL)
        
        def create_backup():
            """创建备份"""
            description = simpledialog.askstring("备份描述", "请输入备份描述（可选）：", parent=top)
            try:
                backup_path = self.backup_manager.create_backup(description or "")
                messagebox.showinfo("成功", f"备份创建成功！\n备份文件：{backup_path}")
                self.operation_logger.log_operation(
                    operation_type="备份",
                    module="系统管理",
                    details=f"创建数据备份: {backup_path}"
                )
                refresh_list()
            except Exception as e:
                messagebox.showerror("错误", f"备份创建失败：{e}")
        
        def refresh_list():
            """刷新备份列表"""
            for item in tree.get_children():
                tree.delete(item)
            
            backups = self.backup_manager.list_backups()
            for backup in backups:
                tree.insert("", tk.END, values=(
                    backup['filename'],
                    backup['size_formatted'],
                    backup['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                ))
        
        def restore_backup():
            """恢复备份"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个备份文件！")
                return
            
            item = tree.item(selected[0])
            filename = item['values'][0]
            
            backups = self.backup_manager.list_backups()
            backup_info = next((b for b in backups if b['filename'] == filename), None)
            
            if not backup_info:
                messagebox.showerror("错误", "备份文件不存在！")
                return
            
            confirm = messagebox.askyesno(
                "确认恢复",
                f"确定要恢复备份吗？\n\n备份文件：{filename}\n\n注意：当前数据将被覆盖！"
            )
            
            if confirm:
                try:
                    success = self.backup_manager.restore_backup(backup_info['path'])
                    if success:
                        messagebox.showinfo("成功", "数据恢复成功！")
                        self.operation_logger.log_operation(
                            operation_type="恢复",
                            module="系统管理",
                            details=f"恢复数据备份: {filename}"
                        )
                    else:
                        messagebox.showerror("错误", "数据恢复失败！")
                except Exception as e:
                    messagebox.showerror("错误", f"恢复失败：{e}")
        
        def delete_backup():
            """删除备份"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("提示", "请先选择一个备份文件！")
                return
            
            item = tree.item(selected[0])
            filename = item['values'][0]
            
            confirm = messagebox.askyesno(
                "确认删除",
                f"确定要删除备份吗？\n\n备份文件：{filename}"
            )
            
            if confirm:
                backups = self.backup_manager.list_backups()
                backup_info = next((b for b in backups if b['filename'] == filename), None)
                
                if backup_info:
                    try:
                        success = self.backup_manager.delete_backup(backup_info['path'])
                        if success:
                            messagebox.showinfo("成功", "备份删除成功！")
                            refresh_list()
                        else:
                            messagebox.showerror("错误", "备份删除失败！")
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败：{e}")
        
        tk.Button(
            btn_frame, 
            text="创建备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=create_backup,
            bg=Styles.SUCCESS_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="恢复备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=restore_backup,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="删除备份", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=delete_backup,
            bg=Styles.ERROR_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="刷新列表", 
            font=Styles.BUTTON_FONT,
            width=15,
            command=refresh_list,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(table_frame, style="Treeview", columns=("filename", "size", "time"), show="headings")
        tree.heading("filename", text="备份文件")
        tree.heading("size", text="文件大小")
        tree.heading("time", text="创建时间")
        tree.column("filename", width=300, anchor=tk.W)
        tree.column("size", width=100, anchor=tk.CENTER)
        tree.column("time", width=180, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        refresh_list()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)
    
    def log_management(self):
        """操作日志管理界面"""
        top = tk.Toplevel(self.root)
        top.title("操作日志查询")
        top.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="操作日志查询", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        filter_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        filter_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        tk.Label(filter_frame, text="操作类型:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(filter_frame, textvariable=type_var, state="readonly", width=15)
        type_combo['values'] = ["全部", "新增", "修改", "删除", "查询", "导入", "导出", "备份", "恢复", "其他"]
        type_combo.current(0)
        type_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="模块:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        module_var = tk.StringVar()
        module_combo = ttk.Combobox(filter_frame, textvariable=module_var, state="readonly", width=15)
        module_combo['values'] = ["全部"]
        module_combo.current(0)
        module_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="记录数:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        limit_var = tk.StringVar(value="100")
        limit_entry = tk.Entry(filter_frame, textvariable=limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=5)
        
        def refresh_logs():
            """刷新日志列表"""
            for item in tree.get_children():
                tree.delete(item)
            
            op_type = type_var.get()
            module = module_var.get()
            limit = int(limit_var.get()) if limit_var.get().isdigit() else 100
            
            op_type_param = None if op_type == "全部" else op_type
            module_param = None if module == "全部" else module
            
            logs = self.operation_logger.get_logs(
                operation_type=op_type_param,
                module=module_param,
                limit=limit
            )
            
            for _, row in logs.iterrows():
                tree.insert("", tk.END, values=(
                    row['日志编号'],
                    row['操作时间'],
                    row['操作类型'],
                    row['操作模块'],
                    row['操作详情'],
                    row['操作人']
                ))
        
        tk.Button(
            filter_frame, 
            text="查询", 
            font=Styles.BUTTON_FONT,
            command=refresh_logs,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=2
        ).pack(side=tk.LEFT, padx=10)
        
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(table_frame, style="Treeview", 
                            columns=("id", "time", "type", "module", "detail", "operator"), 
                            show="headings")
        tree.heading("id", text="日志编号")
        tree.heading("time", text="操作时间")
        tree.heading("type", text="操作类型")
        tree.heading("module", text="操作模块")
        tree.heading("detail", text="操作详情")
        tree.heading("operator", text="操作人")
        tree.column("id", width=150, anchor=tk.W)
        tree.column("time", width=150, anchor=tk.CENTER)
        tree.column("type", width=80, anchor=tk.CENTER)
        tree.column("module", width=120, anchor=tk.W)
        tree.column("detail", width=300, anchor=tk.W)
        tree.column("operator", width=100, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        refresh_logs()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)
    
    def cloud_sync_management(self):
        """云端同步管理界面 - SFTP 版本"""
        top = tk.Toplevel(self.root)
        top.title("云端同步管理 - SFTP")
        top.geometry(f"{Styles.WINDOW_WIDTH}x{Styles.WINDOW_HEIGHT}")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=Styles.PADY_SMALL, fill=tk.X)
        
        tk.Label(
            title_frame, 
            text="云端同步管理 - SFTP", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack(padx=Styles.PADX_MEDIUM, anchor=tk.W)
        
        # 状态信息区域
        status_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        status_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        status_label = tk.Label(
            status_frame, 
            text="同步状态: 未启用",
            font=Styles.LABEL_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_COLOR
        )
        status_label.pack(anchor=tk.W)
        
        # 服务器配置区域
        config_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR, relief=tk.SOLID, bd=1)
        config_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        tk.Label(
            config_frame,
            text="服务器配置",
            font=("微软雅黑", 12, "bold"),
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)
        
        # 主机地址
        tk.Label(config_frame, text="主机地址:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        host_var = tk.StringVar(value="27.tcp.cpolar.top")
        host_entry = tk.Entry(config_frame, textvariable=host_var, width=25, font=Styles.TEXT_FONT)
        host_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 端口
        tk.Label(config_frame, text="端口:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=1, column=2, padx=10, pady=5, sticky=tk.E)
        port_var = tk.StringVar(value="11007")
        port_entry = tk.Entry(config_frame, textvariable=port_var, width=10, font=Styles.TEXT_FONT)
        port_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        
        # 用户名
        tk.Label(config_frame, text="用户名:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        username_var = tk.StringVar(value="ljw")
        username_entry = tk.Entry(config_frame, textvariable=username_var, width=25, font=Styles.TEXT_FONT)
        username_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 密码
        tk.Label(config_frame, text="密码:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=2, column=2, padx=10, pady=5, sticky=tk.E)
        password_var = tk.StringVar(value="Lang0527")
        password_entry = tk.Entry(config_frame, textvariable=password_var, width=25, font=Styles.TEXT_FONT, show="*")
        password_entry.grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)
        
        # 远程路径
        tk.Label(config_frame, text="远程路径:", bg=Styles.BACKGROUND_COLOR, font=Styles.LABEL_FONT).grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        remote_path_var = tk.StringVar(value="/mnt/sda/ljw/Code/Tea/")
        remote_path_entry = tk.Entry(config_frame, textvariable=remote_path_var, width=50, font=Styles.TEXT_FONT)
        remote_path_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)
        
        def update_status():
            """更新状态显示"""
            sync_status = self.cloud_sync_manager.get_sync_status()
            if sync_status['enabled']:
                status_text = f"同步状态: 已启用 | 服务器: {sync_status['host']}:{sync_status['port']} | 用户: {sync_status['username']}"
                if sync_status['last_sync_time']:
                    status_text += f" | 最后同步: {sync_status['last_sync_time'][:19]}"
                status_label.config(text=status_text, fg=Styles.SUCCESS_COLOR)
            elif not sync_status['paramiko_available']:
                status_label.config(text="同步状态: paramiko 库未安装，请运行: pip install paramiko", fg=Styles.ERROR_COLOR)
            else:
                status_label.config(text="同步状态: 未启用", fg=Styles.ERROR_COLOR)
        
        def load_existing_config():
            """加载现有配置"""
            sync_status = self.cloud_sync_manager.get_sync_status()
            if sync_status['host']:
                host_var.set(sync_status['host'])
            if sync_status['port']:
                port_var.set(str(sync_status['port']))
            if sync_status['username']:
                username_var.set(sync_status['username'])
            remote_path_var.set(sync_status['remote_path'])
        
        def save_server_config():
            """保存服务器配置"""
            try:
                host = host_var.get().strip()
                port = int(port_var.get().strip())
                username = username_var.get().strip()
                password = password_var.get().strip()
                remote_path = remote_path_var.get().strip()
                
                if not host or not username:
                    messagebox.showwarning("提示", "主机地址和用户名不能为空！")
                    return
                
                success = self.cloud_sync_manager.set_server_config(host, port, username, password, remote_path)
                if success:
                    messagebox.showinfo("成功", "服务器配置已保存！")
                    self.operation_logger.log_operation(
                        operation_type="设置",
                        module="云端同步",
                        details=f"配置 SFTP 服务器: {host}:{port}"
                    )
                    update_status()
                    refresh_cloud_list()
                else:
                    messagebox.showerror("错误", "保存配置失败！")
            except ValueError:
                messagebox.showerror("错误", "端口必须是数字！")
        
        def test_connection():
            """测试服务器连接"""
            result = self.cloud_sync_manager.test_connection()
            if result['success']:
                messagebox.showinfo("成功", result['message'])
            else:
                messagebox.showerror("错误", result['message'])
        
        def upload_to_cloud():
            """上传数据到云端"""
            if not self.cloud_sync_manager.is_enabled():
                messagebox.showwarning("提示", "请先配置并保存服务器连接！")
                return
            
            data_files = ["tea_inventory.xlsx", "config.json", "operation_logs.xlsx", "cloud_sync_config.json"]
            result = self.cloud_sync_manager.upload_to_cloud(data_files)
            
            if result['success']:
                uploaded_str = ", ".join(result.get('uploaded_files', []))
                messagebox.showinfo("成功", f"{result['message']}\n上传文件: {uploaded_str}")
                self.operation_logger.log_operation(
                    operation_type="上传",
                    module="云端同步",
                    details=f"上传数据到 SFTP 服务器，版本: {result['version']}"
                )
                update_status()
                refresh_cloud_list()
            else:
                messagebox.showerror("错误", result['message'])
        
        def download_from_cloud():
            """从云端下载数据"""
            if not self.cloud_sync_manager.is_enabled():
                messagebox.showwarning("提示", "请先配置并保存服务器连接！")
                return
            
            confirm = messagebox.askyesno(
                "确认下载",
                "确定要从云端下载数据吗？\n\n本地文件会被备份后覆盖！"
            )
            
            if not confirm:
                return
            
            result = self.cloud_sync_manager.download_from_cloud(".")
            
            if result['success']:
                restored_str = ", ".join(result.get('restored_files', []))
                messagebox.showinfo("成功", f"{result['message']}\n恢复文件: {restored_str}")
                self.operation_logger.log_operation(
                    operation_type="下载",
                    module="云端同步",
                    details=f"从 SFTP 服务器恢复数据"
                )
                update_status()
                refresh_cloud_list()
            else:
                messagebox.showerror("错误", result['message'])
        
        def refresh_cloud_list():
            """刷新云端文件列表"""
            for item in tree_cloud.get_children():
                tree_cloud.delete(item)
            
            packages = self.cloud_sync_manager.list_cloud_packages()
            for pkg in packages:
                tree_cloud.insert("", tk.END, values=(
                    pkg.get('filename', ''),
                    pkg.get('size_formatted', ''),
                    pkg.get('modified_time_str', '')
                ))
        
        # 配置操作按钮
        config_btn_frame = tk.Frame(config_frame, bg=Styles.BACKGROUND_COLOR)
        config_btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        tk.Button(
            config_btn_frame, 
            text="保存配置", 
            font=Styles.BUTTON_FONT,
            width=12,
            command=save_server_config,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            config_btn_frame, 
            text="测试连接", 
            font=Styles.BUTTON_FONT,
            width=12,
            command=test_connection,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # 操作按钮区域
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_SMALL)
        
        tk.Button(
            btn_frame, 
            text="上传到云端", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=upload_to_cloud,
            bg=Styles.SUCCESS_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="从云端下载", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=download_from_cloud,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, 
            text="刷新列表", 
            font=Styles.BUTTON_FONT,
            width=18,
            command=refresh_cloud_list,
            bg=Styles.SECONDARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        # 使用说明
        help_frame = tk.Frame(top, bg="#E8F4FD", relief=tk.SOLID, bd=1)
        help_frame.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM, fill=tk.X)
        
        help_text = """使用说明：
1. 本系统通过 SFTP 协议直接连接远程服务器进行数据同步
2. 请在上方填写服务器信息（已预填您提供的配置）
3. 点击\"保存配置\"保存服务器连接信息
4. 点击\"测试连接\"验证服务器连接是否正常
5. 点击\"上传到云端\"将本地数据上传到服务器
6. 点击\"从云端下载\"从服务器下载最新数据到本地
7. 点击\"刷新列表\"查看服务器上的数据文件"""
        
        tk.Label(
            help_frame,
            text=help_text,
            font=Styles.TEXT_FONT,
            bg="#E8F4FD",
            fg="#333333",
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
        
        # 云端文件列表
        table_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        table_frame.pack(padx=Styles.PADX_MEDIUM, pady=Styles.PADY_SMALL, fill=tk.BOTH, expand=True)
        
        tree_cloud = ttk.Treeview(
            table_frame, 
            style="Treeview", 
            columns=("filename", "size", "time"), 
            show="headings"
        )
        tree_cloud.heading("filename", text="文件名")
        tree_cloud.heading("size", text="文件大小")
        tree_cloud.heading("time", text="修改时间")
        tree_cloud.column("filename", width=300, anchor=tk.W)
        tree_cloud.column("size", width=120, anchor=tk.CENTER)
        tree_cloud.column("time", width=180, anchor=tk.CENTER)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree_cloud.yview)
        tree_cloud.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_cloud.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 加载现有配置并初始化
        load_existing_config()
        update_status()
        refresh_cloud_list()
        
        tk.Button(
            top, 
            text="关闭", 
            font=Styles.BUTTON_FONT,
            width=Styles.BUTTON_WIDTH,
            height=Styles.BUTTON_HEIGHT,
            command=top.destroy,
            bg=Styles.PRIMARY_COLOR,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(pady=Styles.PADY_MEDIUM)


def main():
    root = tk.Tk()
    app = TeaInventoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

