import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles


class SupplierViewMixin:
    """GUI 视图混入类"""

    def supplier_management(self):
        """供应商管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "供应商管理", "管理您的供应商信息")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("查看所有供应商", self.view_all_suppliers, "📋"),
            ("添加供应商", self.add_supplier_gui, "➕"),
            ("修改供应商", self.update_supplier_gui, "✏️"),
            ("删除供应商", self.delete_supplier_gui, "🗑️")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

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
        top = self._create_toplevel_with_size("add_supplier", "medium")
        top.title("添加供应商")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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

        # 表单容器 - 两列布局
        form_container = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_container.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM)
        
        left_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        right_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 左列字段
        # 供应商编号
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="供应商编号 (留空自动生成)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        supplier_id_var = tk.StringVar()
        tk.Entry(frame, textvariable=supplier_id_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 供应商名称
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="供应商名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        name_var = tk.StringVar()
        tk.Entry(frame, textvariable=name_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 联系人
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="联系人", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        contact_var = tk.StringVar()
        tk.Entry(frame, textvariable=contact_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 右列字段
        # 联系电话
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="联系电话", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        phone_var = tk.StringVar()
        tk.Entry(frame, textvariable=phone_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 地址
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="地址", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        address_var = tk.StringVar()
        tk.Entry(frame, textvariable=address_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 备注
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="备注", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        remarks_var = tk.StringVar()
        tk.Entry(frame, textvariable=remarks_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

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
        top = self._create_toplevel_with_size("update_supplier", "medium")
        top.title("修改供应商")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
            edit_top = self._create_toplevel_with_size("edit_supplier", "medium", parent=top)
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
                ("供应商名称", "供应商名称", supplier_row['供应商名称']),
                ("联系人", "联系人", supplier_row['联系人'])
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
                ("联系电话", "联系电话", supplier_row['联系电话']),
                ("地址", "地址", supplier_row['地址']),
                ("备注", "备注", supplier_row['备注'])
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
        top = self._create_toplevel_with_size("delete_supplier", "small")
        top.title("删除供应商")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
