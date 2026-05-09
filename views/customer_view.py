import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles


class CustomerViewMixin:
    """GUI 视图混入类"""

    def customer_management(self):
        """客户管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "客户管理", "管理您的客户信息")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("查看所有客户", self.view_all_customers, "📋"),
            ("添加客户", self.add_customer_gui, "➕"),
            ("修改客户", self.update_customer_gui, "✏️"),
            ("删除客户", self.delete_customer_gui, "🗑️")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def view_all_customers(self):
        df = self.system.excel_manager.get_all_customers()
        if not df.empty:
            try:
                # 获取销售数据和商品成本价
                sales_df = self.system.excel_manager.get_all_sales()
                commodity_df = self.system.excel_manager.get_all_commodities()
                
                if not sales_df.empty and not commodity_df.empty:
                    # 合并销售数据和成本价
                    merged_sales = pd.merge(sales_df, commodity_df[["商品编号", "成本价"]], 
                                          on="商品编号", how="left")
                    
                    # 计算每笔销售的利润
                    unit_is_gram = merged_sales.get('销售单位', '斤') == '克'
                    merged_sales['销售数量(斤)'] = merged_sales['销售数量']
                    merged_sales.loc[unit_is_gram, '销售数量(斤)'] = merged_sales.loc[unit_is_gram, '销售数量'] / 500
                    merged_sales['销售成本'] = merged_sales['销售数量(斤)'] * merged_sales['成本价']
                    merged_sales['利润'] = merged_sales['实收金额'] - merged_sales['销售成本']
                    
                    # 按客户分组计算累计利润
                    customer_profit = merged_sales.groupby('客户名称')['利润'].sum().reset_index()
                    customer_profit.columns = ['客户名称', '累计利润']
                    
                    # 合并到客户数据中
                    df = pd.merge(df, customer_profit, on='客户名称', how='left')
                    df['累计利润'] = df['累计利润'].fillna(0).round(2)
                    
                    # 调整列的顺序，将累计利润放在累计消费后面
                    cols = list(df.columns)
                    if '累计消费' in cols and '累计利润' in cols:
                        pos = cols.index('累计消费')
                        cols.insert(pos + 1, cols.pop(cols.index('累计利润')))
                        df = df[cols]
            except Exception as e:
                print(f"计算客户累计利润时出错: {e}")
        self.show_dataframe_window(df, "客户列表")

    def add_customer_gui(self):
        """添加客户GUI"""
        top = self._create_toplevel_with_size("add_customer", "medium")
        top.title("添加客户")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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

        # 表单容器 - 两列布局
        form_container = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_container.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM)
        
        left_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        right_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 左列字段
        # 客户编号
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="客户编号 (留空自动生成)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        customer_id_var = tk.StringVar()
        tk.Entry(frame, textvariable=customer_id_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 客户名称
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="客户名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        name_var = tk.StringVar()
        tk.Entry(frame, textvariable=name_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 联系电话
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="联系电话", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        phone_var = tk.StringVar()
        tk.Entry(frame, textvariable=phone_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 右列字段
        # 地址
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="地址", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        address_var = tk.StringVar()
        tk.Entry(frame, textvariable=address_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 累计消费
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="累计消费", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        total_purchases_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=total_purchases_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

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
        top = self._create_toplevel_with_size("update_customer", "medium")
        top.title("修改客户")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
            edit_top = self._create_toplevel_with_size("edit_customer", "medium", parent=top)
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

            # 表单容器 - 两列布局
            form_container = tk.Frame(edit_top, bg=Styles.BACKGROUND_COLOR)
            form_container.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM)
            
            left_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
            right_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
            left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

            # 创建变量
            vars = {}
            
            # 左列字段
            fields_left = [
                ("客户名称", "客户名称", customer_row['客户名称']),
                ("联系电话", "联系电话", customer_row['联系电话'])
            ]
            
            for label, key, value in fields_left:
                frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
                frame.pack(fill=tk.X, pady=4)
                tk.Label(frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
                var = tk.StringVar(value=str(value) if pd.notna(value) else "")
                vars[key] = var
                tk.Entry(frame, textvariable=var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))
            
            # 右列字段
            fields_right = [
                ("地址", "地址", customer_row['地址']),
                ("累计消费", "累计消费", customer_row['累计消费'])
            ]
            
            for label, key, value in fields_right:
                frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
                frame.pack(fill=tk.X, pady=4)
                tk.Label(frame, text=label, font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
                var = tk.StringVar(value=str(value) if pd.notna(value) else "")
                vars[key] = var
                tk.Entry(frame, textvariable=var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

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
        top = self._create_toplevel_with_size("delete_customer", "small")
        top.title("删除客户")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
