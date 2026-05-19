import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles
from validators import validate_required, validate_numeric, validate_integer, highlight_entry_error, clear_entry_highlight
from tea_commodity import TeaCommodity
from logger import get_logger

_logger = get_logger()


class ProductViewMixin:
    """GUI 视图混入类"""

    def product_management(self):
        """商品管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 页面标题
        self._create_page_header(main_container, "商品管理", "管理您的茶叶商品库存")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("查看所有商品", self.view_all_products, "📋"),
            ("添加商品", self.add_product_gui, "➕"),
            ("修改商品", self.update_product_gui, "✏️"),
            ("删除商品", self.delete_product_gui, "🗑️"),
            ("按编号查询", self.query_product_by_id_gui, "🔍"),
            ("按商品名查询", self.query_product_by_name_gui, "🔎")
        ]
        self._create_button_grid(buttons_container, buttons, columns=3)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def view_all_products(self):
        """查看所有商品"""
        df = self.system.excel_manager.get_all_commodities()
        self.show_dataframe_window(df, "商品列表")

    def add_product_gui(self):
        """添加商品GUI"""
        top = self._create_toplevel_with_size("add_product", "medium")
        top.title("添加商品")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=(15, 10))
        
        tk.Label(
            title_frame, 
            text="添加商品", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 创建表单容器 - 使用Canvas和滚动条
        form_container = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 创建Canvas用于滚动
        canvas = tk.Canvas(form_container, bg=Styles.BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        form_scroll_frame = tk.Frame(canvas, bg=Styles.BACKGROUND_COLOR)

        form_scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 创建两列表单
        left_col = tk.Frame(form_scroll_frame, bg=Styles.BACKGROUND_COLOR)
        right_col = tk.Frame(form_scroll_frame, bg=Styles.BACKGROUND_COLOR)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 左列字段
        fields_left = [
            ("商品编号 (留空自动生成)", "com_id", ""),
            ("茶类 *", "tea_category", ""),
            ("品种 *", "variety", ""),
            ("公司/品牌", "company", ""),
            ("产区", "origin", ""),
            ("商品名称 *", "name", ""),
            ("规格 *", "specification", ""),
            ("成本价(每斤) *", "cost_price", ""),
        ]

        vars_left = {}
        entries_left = {}
        for i, (label_text, key, default) in enumerate(fields_left):
            frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
            frame.pack(fill=tk.X, pady=3)
            tk.Label(frame, text=label_text, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
            var = tk.StringVar(value=default)
            vars_left[key] = var
            entry = tk.Entry(frame, textvariable=var, width=28, font=Styles.TEXT_FONT)
            entry.pack(fill=tk.X, pady=(2, 0))
            entries_left[key] = entry

        com_id_var = vars_left["com_id"]
        tea_category_var = vars_left["tea_category"]
        variety_var = vars_left["variety"]
        company_var = vars_left["company"]
        origin_var = vars_left["origin"]
        name_var = vars_left["name"]
        specification_var = vars_left["specification"]
        cost_price_var = vars_left["cost_price"]

        # 右列字段
        fields_right = [
            ("零售价(每斤) *", "retail_price", ""),
            ("初始库存(斤) *", "current_stock", ""),
            ("生产日期(YYYY-MM-DD)", "production_date", ""),
            ("保质期(月) *", "shelf_life", ""),
            ("品质特征", "quality_features", ""),
            ("年份", "year", ""),
            ("等级", "grade", ""),
            ("计量单位(斤/克)", "unit", "斤"),
        ]

        vars_right = {}
        entries_right = {}
        for i, (label_text, key, default) in enumerate(fields_right):
            frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
            frame.pack(fill=tk.X, pady=3)
            tk.Label(frame, text=label_text, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
            var = tk.StringVar(value=default)
            vars_right[key] = var
            entry = tk.Entry(frame, textvariable=var, width=28, font=Styles.TEXT_FONT)
            entry.pack(fill=tk.X, pady=(2, 0))
            entries_right[key] = entry

        retail_price_var = vars_right["retail_price"]
        current_stock_var = vars_right["current_stock"]
        production_date_var = vars_right["production_date"]
        shelf_life_var = vars_right["shelf_life"]
        quality_features_var = vars_right["quality_features"]
        year_var = vars_right["year"]
        grade_var = vars_right["grade"]
        unit_var = vars_right["unit"]

        # 按钮
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_MEDIUM)

        def submit():
            try:
                errors = []
                result = validate_required(tea_category_var.get(), "茶类")
                if not result: errors.append(result.error_message); highlight_entry_error(entries_left["tea_category"])
                else: clear_entry_highlight(entries_left["tea_category"])
                result = validate_required(variety_var.get(), "品种")
                if not result: errors.append(result.error_message); highlight_entry_error(entries_left["variety"])
                else: clear_entry_highlight(entries_left["variety"])
                result = validate_required(name_var.get(), "商品名称")
                if not result: errors.append(result.error_message); highlight_entry_error(entries_left["name"])
                else: clear_entry_highlight(entries_left["name"])
                result = validate_required(specification_var.get(), "规格")
                if not result: errors.append(result.error_message); highlight_entry_error(entries_left["specification"])
                else: clear_entry_highlight(entries_left["specification"])
                result = validate_numeric(cost_price_var.get(), "成本价", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(entries_left["cost_price"])
                else: clear_entry_highlight(entries_left["cost_price"])
                result = validate_numeric(retail_price_var.get(), "零售价", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(entries_right["retail_price"])
                else: clear_entry_highlight(entries_right["retail_price"])
                result = validate_numeric(current_stock_var.get(), "初始库存", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(entries_right["current_stock"])
                else: clear_entry_highlight(entries_right["current_stock"])
                result = validate_integer(shelf_life_var.get(), "保质期", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(entries_right["shelf_life"])
                else: clear_entry_highlight(entries_right["shelf_life"])

                if errors:
                    messagebox.showwarning("输入校验", "\n".join(errors))
                    return

                com_id_input = com_id_var.get().strip()
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

                result = self.system.add_commodity_business(
                    com_id_input=com_id_input, tea_category=tea_category,
                    variety=variety, company=company, origin=origin,
                    name=name, specification=specification,
                    cost_price=cost_price, retail_price=retail_price,
                    current_stock=current_stock, production_date=production_date,
                    shelf_life=shelf_life, quality_features=quality_features,
                    year=year, grade=grade, unit=unit
                )

                if not result['success']:
                    messagebox.showerror("错误", result['message'])
                    return

                new_com_id = result['com_id']
                commodity_data = TeaCommodity(
                    com_id=new_com_id, tea_category=tea_category,
                    variety=variety, company=company, origin=origin,
                    name=name, specification=specification,
                    cost_price=cost_price, retail_price=retail_price,
                    current_stock=current_stock, production_date=production_date,
                    shelf_life=shelf_life, quality_features=quality_features,
                    year=year, grade=grade, unit=unit
                ).to_list()

                self.undo_manager.record_action(
                    f"添加商品：{name}",
                    undo_func=lambda cid=new_com_id: self.system.excel_manager.delete_commodity(cid),
                    redo_func=lambda data=commodity_data: self.system.excel_manager.add_commodity(data)
                )
                self._update_status_bar()

                messagebox.showinfo("成功", f"商品添加成功！\n商品编号: {new_com_id}")
                top.destroy()
            except ValueError as e:
                _logger.exception("商品添加数据输入错误")
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
        top = self._create_toplevel_with_size("update_product", "medium")
        top.title("修改商品")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

        tk.Label(top, text="请选择要修改的商品", 
                 font=Styles.SUB_HEADER_FONT,
                 bg=Styles.BACKGROUND_COLOR,
                 fg=Styles.HEADER_COLOR).pack(pady=(15, 10))

        # 获取所有商品
        df = self.system.excel_manager.get_all_commodities()
        if df.empty:
            messagebox.showinfo("提示", "暂无商品数据")
            top.destroy()
            return

        # 创建商品列表
        list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        list_frame.pack(pady=(0, 10), padx=20, fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(list_frame, style="Treeview", show="headings")
        tree["columns"] = ("商品编号", "商品名称", "茶类", "品种", "当前库存", "零售价")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor=tk.CENTER)

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
            edit_top = self._create_toplevel_with_size("edit_product", "medium")
            edit_top.title("修改商品信息")
            edit_top.configure(bg=Styles.BACKGROUND_COLOR)
            edit_top.resizable(True, True)

            # 创建标题区域
            title_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            title_frame.pack(pady=(15, 10))
            
            tk.Label(
                title_frame, 
                text="修改商品信息", 
                font=Styles.SUB_HEADER_FONT,
                bg=Styles.BACKGROUND_COLOR,
                fg=Styles.HEADER_COLOR
            ).pack()

            # 创建表单容器 - 使用Canvas和滚动条
            form_container = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            form_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # 创建Canvas用于滚动
            canvas = tk.Canvas(form_container, bg=Styles.BACKGROUND_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
            form_scroll_frame = tk.Frame(canvas, bg=Styles.BACKGROUND_COLOR)

            form_scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=form_scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # 创建两列表单
            left_col = tk.Frame(form_scroll_frame, bg=Styles.BACKGROUND_COLOR)
            right_col = tk.Frame(form_scroll_frame, bg=Styles.BACKGROUND_COLOR)
            left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

            # 创建变量
            vars = {}
            entries = {}
            fields_left = [
                ("商品编号", "商品编号", commodity['商品编号']),
                ("茶类", "茶类", commodity['茶类']),
                ("品种", "品种", commodity['品种']),
                ("公司", "公司", commodity['公司']),
                ("产区", "产区", commodity['产区']),
                ("商品名称", "商品名称", commodity['商品名称']),
                ("规格", "规格", commodity['规格']),
                ("成本价", "成本价", commodity['成本价']),
            ]

            for label, key, value in fields_left:
                frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
                frame.pack(fill=tk.X, pady=3)
                tk.Label(frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
                var = tk.StringVar(value=str(value) if pd.notna(value) else "")
                vars[key] = var
                entry = tk.Entry(frame, textvariable=var, width=28, font=Styles.TEXT_FONT)
                entry.pack(fill=tk.X, pady=(2, 0))
                entries[key] = entry

            fields_right = [
                ("零售价", "零售价", commodity['零售价']),
                ("当前库存", "当前库存", commodity['当前库存']),
                ("生产日期", "生产日期", commodity['生产日期']),
                ("保质期(月)", "保质期(月)", commodity['保质期(月)']),
                ("品质特征", "品质特征", commodity['品质特征']),
                ("年份", "年份", commodity['年份']),
                ("等级", "等级", commodity['等级']),
                ("单位", "单位", commodity['单位']),
            ]

            for label, key, value in fields_right:
                frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
                frame.pack(fill=tk.X, pady=3)
                tk.Label(frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
                var = tk.StringVar(value=str(value) if pd.notna(value) else "")
                vars[key] = var
                entry = tk.Entry(frame, textvariable=var, width=28, font=Styles.TEXT_FONT)
                entry.pack(fill=tk.X, pady=(2, 0))
                entries[key] = entry

            def save():
                errors = []
                result = validate_required(vars["商品名称"].get(), "商品名称")
                if not result: errors.append(result.error_message); highlight_entry_error(entries["商品名称"])
                else: clear_entry_highlight(entries["商品名称"])
                for key in ['成本价', '零售价', '当前库存']:
                    val = vars[key].get().strip()
                    if val:
                        result = validate_numeric(val, key, min_val=0)
                        if not result: errors.append(result.error_message); highlight_entry_error(entries[key])
                        else: clear_entry_highlight(entries[key])
                for key in ['保质期(月)']:
                    val = vars[key].get().strip()
                    if val:
                        result = validate_integer(val, key, min_val=0)
                        if not result: errors.append(result.error_message); highlight_entry_error(entries[key])
                        else: clear_entry_highlight(entries[key])

                if errors:
                    messagebox.showwarning("输入校验", "\n".join(errors))
                    return

                updates = {}
                for key, var in vars.items():
                    value = var.get().strip()
                    if value:
                        if key in ['成本价', '零售价', '当前库存']:
                            updates[key] = float(value)
                        elif key in ['保质期(月)', '年份']:
                            updates[key] = int(float(value))
                        else:
                            updates[key] = value

                if updates:
                    old_data = dict(commodity)
                    success = self.system.excel_manager.update_commodity(com_id, updates)
                    if success.get('success'):
                        self.undo_manager.record_action(
                            f"修改商品：{commodity['商品名称']}",
                            undo_func=lambda cid=com_id, old=old_data: self.system.excel_manager.update_commodity(cid, old),
                            redo_func=lambda cid=com_id, upd=updates: self.system.excel_manager.update_commodity(cid, upd)
                        )
                        self._update_status_bar()
                        messagebox.showinfo("成功", "商品信息更新成功！")
                        edit_top.destroy()
                        top.destroy()
                    else:
                        messagebox.showerror("错误", "更新失败！")
                else:
                    messagebox.showinfo("提示", "未做任何修改。")

            btn_frame = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=10)
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
        btn_frame.pack(pady=10)

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
        top = self._create_toplevel_with_size("delete_product", "small")
        top.title("删除商品")
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
                commodity_columns = ["商品编号", "茶类", "品种", "公司", "产区", "商品名称",
                                     "规格", "成本价", "零售价", "生产日期", "保质期(月)",
                                     "当前库存", "品质特征", "年份", "等级", "单位"]
                saved_data = [commodity.get(col, "") for col in commodity_columns]
                product_name = commodity['商品名称']
                success = self.system.excel_manager.delete_commodity(com_id)
                if success.get('success'):
                    self.undo_manager.record_action(
                        f"删除商品：{product_name}",
                        undo_func=lambda data=saved_data: self.system.excel_manager.add_commodity(data),
                        redo_func=lambda cid=com_id: self.system.excel_manager.delete_commodity(cid)
                    )
                    self._update_status_bar()
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
        top = self._create_toplevel_with_size("query_product_by_id", "small")
        top.title("按编号查询商品")
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
            info_top = self._create_toplevel_with_size("product_info", "medium")
            info_top.title("商品信息")
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
        top = self._create_toplevel_with_size("query_product_by_name", "large")
        top.title("按商品名查询")
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
            
            info_top = self._create_toplevel_with_size("product_detail", "medium")
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
