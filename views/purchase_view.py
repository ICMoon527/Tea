import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles
from validators import validate_required, validate_numeric, highlight_entry_error, clear_entry_highlight
from logger import get_logger

_logger = get_logger()


class PurchaseViewMixin:
    """GUI 视图混入类"""

    def stock_management(self):
        """进货管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "进货管理", "管理商品入库和库存记录")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("进货入库", self.stock_in_gui, "📥"),
            ("查看进货记录", self.view_all_stocks, "📋")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def stock_in_gui(self):
        """进货入库GUI"""
        top = self._create_toplevel_with_size("stock_in", "medium")
        top.title("进货入库")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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

        # 输入表单 - 两列布局
        form_container = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        form_container.pack(pady=Styles.PADY_SMALL, padx=Styles.PADX_MEDIUM)
        
        left_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        right_col = tk.Frame(form_container, bg=Styles.BACKGROUND_COLOR)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 左列字段
        # 商品编号
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="商品编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        com_id_var = tk.StringVar()
        entry_frame = tk.Frame(frame, bg=Styles.BACKGROUND_COLOR)
        entry_frame.pack(fill=tk.X)
        com_id_entry = tk.Entry(entry_frame, textvariable=com_id_var, font=Styles.TEXT_FONT)
        com_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(2, 0))
        btn_select_product = tk.Button(entry_frame, text="选择...", font=Styles.TEXT_FONT,
                                      width=8, command=lambda: self._select_product_dialog(com_id_var),
                                      bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=5, pady=2)
        btn_select_product.pack(side=tk.LEFT, padx=(5, 0))
        btn_select_product.bind("<Enter>", lambda e, b=btn_select_product: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_select_product.bind("<Leave>", lambda e, b=btn_select_product: b.config(bg=Styles.PRIMARY_COLOR))

        # 进货单价
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="进货单价(每斤)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        unit_price_var = tk.StringVar()
        unit_price_entry = tk.Entry(frame, textvariable=unit_price_var, font=Styles.TEXT_FONT)
        unit_price_entry.pack(fill=tk.X, pady=(2, 0))

        # 进货数量
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="进货数量", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(frame, textvariable=quantity_var, font=Styles.TEXT_FONT)
        quantity_entry.pack(fill=tk.X, pady=(2, 0))

        # 进货单位
        frame = tk.Frame(left_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="进货单位 (斤/克)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        unit_var = tk.StringVar(value="斤")
        tk.Entry(frame, textvariable=unit_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 右列字段
        # 供应商
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="供应商", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        supplier_var = tk.StringVar()
        entry_frame = tk.Frame(frame, bg=Styles.BACKGROUND_COLOR)
        entry_frame.pack(fill=tk.X)
        tk.Entry(entry_frame, textvariable=supplier_var, font=Styles.TEXT_FONT).pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(2, 0))
        btn_select_supplier = tk.Button(entry_frame, text="选择...", font=Styles.TEXT_FONT,
                                        width=8, command=lambda: self._select_supplier_dialog(supplier_var),
                                        bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=5, pady=2)
        btn_select_supplier.pack(side=tk.LEFT, padx=(5, 0))
        btn_select_supplier.bind("<Enter>", lambda e, b=btn_select_supplier: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_select_supplier.bind("<Leave>", lambda e, b=btn_select_supplier: b.config(bg=Styles.PRIMARY_COLOR))

        # 进货日期
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="进货日期 (YYYY-MM-DD)", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        stock_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(frame, textvariable=stock_date_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        # 备注
        frame = tk.Frame(right_col, bg=Styles.BACKGROUND_COLOR)
        frame.pack(fill=tk.X, pady=4)
        tk.Label(frame, text="备注", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR, anchor="w").pack(fill=tk.X)
        remarks_var = tk.StringVar()
        tk.Entry(frame, textvariable=remarks_var, font=Styles.TEXT_FONT).pack(fill=tk.X, pady=(2, 0))

        def submit():
            try:
                errors = []
                result = validate_required(com_id_var.get(), "商品编号")
                if not result: errors.append(result.error_message); highlight_entry_error(com_id_entry)
                else: clear_entry_highlight(com_id_entry)
                result = validate_numeric(unit_price_var.get(), "进货单价", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(unit_price_entry)
                else: clear_entry_highlight(unit_price_entry)
                result = validate_numeric(quantity_var.get(), "进货数量", min_val=0)
                if not result: errors.append(result.error_message); highlight_entry_error(quantity_entry)
                else: clear_entry_highlight(quantity_entry)

                if errors:
                    messagebox.showwarning("输入校验", "\n".join(errors))
                    return

                com_id = com_id_var.get().strip()
                unit_price = float(unit_price_var.get())
                quantity = float(quantity_var.get())
                unit = unit_var.get().strip() or "斤"
                supplier = supplier_var.get().strip()
                stock_date = stock_date_var.get().strip() or datetime.now().strftime("%Y-%m-%d")
                remarks = remarks_var.get().strip()

                commodity_before = self.system.excel_manager.get_commodity_by_id(com_id)
                stock_before = float(commodity_before['当前库存']) if commodity_before is not None else 0
                cost_before = float(commodity_before['成本价']) if commodity_before is not None and pd.notna(commodity_before['成本价']) else 0

                result = self.system.create_stock_record_business(
                    com_id=com_id, unit_price=unit_price, quantity=quantity,
                    unit=unit, supplier=supplier, stock_date=stock_date, remarks=remarks
                )

                if not result['success']:
                    messagebox.showerror("错误", result['message'])
                    return

                stock_id = result['stock_id']
                commodity_name = commodity_before['商品名称'] if commodity_before is not None else com_id
                stock_data = [stock_id, com_id, commodity_name, quantity, unit_price,
                              supplier, stock_date, remarks, unit]
                self.undo_manager.record_action(
                    f"进货入库：{commodity_name} {quantity}{unit}",
                    undo_func=lambda sid=stock_id, cid=com_id, sb=stock_before, cb=cost_before:
                        self._undo_stock_in(sid, cid, sb, cb),
                    redo_func=lambda sd=stock_data: self._redo_stock_in(sd)
                )
                self._update_status_bar()

                messagebox.showinfo("成功", f"进货入库成功！\n进货编号: {stock_id}")
                top.destroy()
            except ValueError as e:
                _logger.exception("进货数据输入错误")
                messagebox.showerror("错误", f"数据输入错误: {e}")
            except Exception as e:
                messagebox.showerror("错误", f"进货失败: {e}")

        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.PADY_LARGE)

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

    def _undo_stock_in(self, stock_id, com_id, stock_before, cost_before):
        self.system.excel_manager.delete_record("进货记录", stock_id, "进货编号")
        self.system.excel_manager.update_commodity(com_id, {
            '当前库存': stock_before,
            '成本价': cost_before
        })

    def _redo_stock_in(self, stock_data):
        self.system.excel_manager.add_stock(list(stock_data))
