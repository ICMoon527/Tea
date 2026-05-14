import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles
from validators import validate_required, validate_phone, highlight_entry_error, clear_entry_highlight
from logger import get_logger

_logger = get_logger()


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
        _logger.debug(f"供应商数据行数: {len(df)}")
        _logger.debug(f"供应商数据列数: {len(df.columns)}")
        _logger.debug(f"列名: {list(df.columns)}")
        _logger.debug(f"是否为空: {df.empty}")
        if not df.empty:
            _logger.debug("前5行数据:")
            _logger.debug(df.head())
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
        supplier_id_entry = tk.Entry(frame, textvariable=supplier_id_var, font=Styles.TEXT_FONT)
        supplier_id_entry.pack(fill=tk.X, pady=(2, 0))

        # 供应商名称
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="供应商名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        name_var = tk.StringVar()
        name_entry = tk.Entry(frame, textvariable=name_var, font=Styles.TEXT_FONT)
        name_entry.pack(fill=tk.X, pady=(2, 0))

        # 联系人
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="联系人", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        contact_var = tk.StringVar()
        contact_entry = tk.Entry(frame, textvariable=contact_var, font=Styles.TEXT_FONT)
        contact_entry.pack(fill=tk.X, pady=(2, 0))

        # 右列字段
        # 联系电话
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="联系电话", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(frame, textvariable=phone_var, font=Styles.TEXT_FONT)
        phone_entry.pack(fill=tk.X, pady=(2, 0))

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
                errors = []
                result = validate_required(name_var.get(), "供应商名称")
                if not result: errors.append(result.error_message); highlight_entry_error(name_entry)
                else: clear_entry_highlight(name_entry)
                result = validate_phone(phone_var.get(), "联系电话")
                if not result: errors.append(result.error_message); highlight_entry_error(phone_entry)
                else: clear_entry_highlight(phone_entry)

                if errors:
                    messagebox.showwarning("输入校验", "\n".join(errors))
                    return

                supplier_id_input = supplier_id_var.get().strip()
                name = name_var.get().strip()
                contact_person = contact_var.get().strip()
                phone = phone_var.get().strip()
                address = address_var.get().strip()
                remarks = remarks_var.get().strip()

                result = self.system.add_supplier_business(
                    supplier_id_input=supplier_id_input, name=name,
                    contact_person=contact_person, phone=phone,
                    address=address, remarks=remarks
                )

                if not result['success']:
                    messagebox.showerror("错误", result['message'])
                    return

                new_supplier_id = result['supplier_id']
                supplier_data = [new_supplier_id, name, contact_person, phone, address, 0.0, remarks]
                self.undo_manager.record_action(
                    f"添加供应商：{name}",
                    undo_func=lambda sid=new_supplier_id: self.system.excel_manager.delete_record("供应商", sid, "供应商编号"),
                    redo_func=lambda sd=supplier_data: self.system.excel_manager.append_to_sheet("供应商", sd)
                )
                self._update_status_bar()

                messagebox.showinfo("成功", f"供应商添加成功！\n供应商编号: {new_supplier_id}")
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
            entries = {}
            
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
                entry = tk.Entry(frame, textvariable=var, font=Styles.TEXT_FONT)
                entry.pack(fill=tk.X, pady=(2, 0))
                entries[key] = entry
            
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
                entry = tk.Entry(frame, textvariable=var, font=Styles.TEXT_FONT)
                entry.pack(fill=tk.X, pady=(2, 0))
                entries[key] = entry

            def save():
                errors = []
                result = validate_required(vars["供应商名称"].get(), "供应商名称")
                if not result: errors.append(result.error_message); highlight_entry_error(entries["供应商名称"])
                else: clear_entry_highlight(entries["供应商名称"])
                result = validate_phone(vars["联系电话"].get(), "联系电话")
                if not result: errors.append(result.error_message); highlight_entry_error(entries["联系电话"])
                else: clear_entry_highlight(entries["联系电话"])

                if errors:
                    messagebox.showwarning("输入校验", "\n".join(errors))
                    return

                updates = {}
                for key, var in vars.items():
                    value = var.get().strip()
                    updates[key] = value if value else ""

                if updates:
                    old_data = {
                        '供应商名称': supplier_row['供应商名称'],
                        '联系人': supplier_row['联系人'],
                        '联系电话': supplier_row['联系电话'],
                        '地址': supplier_row['地址'],
                        '备注': supplier_row.get('备注', '')
                    }
                    update_result = self.system.update_supplier_business(supplier_id, updates)
                    if update_result['success']:
                        self.undo_manager.record_action(
                            f"修改供应商：{supplier_row['供应商名称']}",
                            undo_func=lambda sid=supplier_id, old=dict(old_data): self.system.update_supplier_business(sid, old),
                            redo_func=lambda sid=supplier_id, upd=dict(updates): self.system.update_supplier_business(sid, upd)
                        )
                        self._update_status_bar()
                        messagebox.showinfo("成功", "供应商信息更新成功！")
                        edit_top.destroy()
                        top.destroy()
                    else:
                        messagebox.showerror("错误", update_result['message'])
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
            all_suppliers = self.system.excel_manager.get_all_suppliers()
            if all_suppliers.empty:
                messagebox.showerror("错误", "未找到供应商信息")
                return

            supplier_row = all_suppliers[all_suppliers['供应商编号'] == supplier_id]
            if supplier_row.empty:
                messagebox.showerror("错误", "未找到该供应商")
                return

            if messagebox.askyesno("确认", f"确定要删除供应商 '{supplier_row.iloc[0]['供应商名称']}' 吗？"):
                supplier_name = supplier_row.iloc[0]['供应商名称']
                saved_row = supplier_row.iloc[0].to_list()
                result = self.system.delete_supplier_business(supplier_id)
                if result['success']:
                    self.undo_manager.record_action(
                        f"删除供应商：{supplier_name}",
                        undo_func=lambda sd=list(saved_row): self.system.excel_manager.append_to_sheet("供应商", sd),
                        redo_func=lambda sid=supplier_id: self.system.delete_supplier_business(sid)
                    )
                    self._update_status_bar()
                    messagebox.showinfo("成功", "供应商删除成功！")
                    top.destroy()
                else:
                    messagebox.showerror("错误", result['message'])

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
