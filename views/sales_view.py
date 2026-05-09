import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles


class SalesViewMixin:
    """GUI 视图混入类"""

    def sales_management(self):
        """销售管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "销售管理", "处理客户订单和销售流程")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("添加商品到购物车", self.add_to_cart_gui, "🛒"),
            ("查看购物车", self.view_cart_gui, "📋"),
            ("清空购物车", self.clear_cart_gui, "🗑️"),
            ("结账", self.checkout_gui, "💳")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def add_to_cart_gui(self):
        """添加商品到购物车GUI"""
        top = self._create_toplevel_with_size("add_to_cart", "large")
        top.title("添加商品到购物车")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=(Styles.SPACING_MD, Styles.SPACING_SM))
        
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
                # 创建商品列表框
                list_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                list_frame.pack(pady=(Styles.SPACING_XS, Styles.SPACING_XS), fill=tk.BOTH, expand=True, padx=Styles.SPACING_LG)
                
                listbox = tk.Listbox(list_frame, width=100, height=18, font=Styles.TEXT_FONT)
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
                input_frame.pack(pady=Styles.SPACING_SM)
                
                # 水平排列输入框
                input_row_frame = tk.Frame(input_frame, bg=Styles.BACKGROUND_COLOR)
                input_row_frame.pack(pady=Styles.SPACING_XS, fill=tk.X)
                
                # 商品序号
                serial_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                serial_frame.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
                tk.Label(serial_frame, text="商品序号: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack()
                choice_var = tk.StringVar()
                tk.Entry(serial_frame, textvariable=choice_var, width=10, font=Styles.TEXT_FONT).pack()
                
                # 购买数量
                quantity_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                quantity_frame.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
                tk.Label(quantity_frame, text="购买数量: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack()
                quantity_var = tk.StringVar()
                quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var, width=20, font=Styles.TEXT_FONT)
                quantity_entry.pack()
                
                # 购买单位
                unit_frame = tk.Frame(input_row_frame, bg=Styles.BACKGROUND_COLOR)
                unit_frame.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
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
                            
                            # 添加到购物车 - 使用 ShoppingCart 的方法
                            result = self.system.shopping_cart.add_item(com_id, quantity, unit)
                            if not result['success']:
                                messagebox.showerror("错误", result['message'])
                                return
                            
                            messagebox.showinfo("成功", f"已添加到购物车！\n商品: {com_name}\n数量: {quantity} {unit}")
                            top.destroy()
                        else:
                            messagebox.showerror("错误", "无效的选择")
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数字")
                
                btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
                btn_frame.pack(pady=Styles.SPACING_MD)
                
                btn_add = tk.Button(btn_frame, text="添加到购物车", font=Styles.BUTTON_FONT,
                          width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=add_to_cart,
                          bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                btn_add.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
                btn_add.bind("<Enter>", lambda e, b=btn_add: b.config(bg=Styles.BUTTON_HOVER_COLOR))
                btn_add.bind("<Leave>", lambda e, b=btn_add: b.config(bg=Styles.PRIMARY_COLOR))
                
                # 添加取消按钮到同一框架
                btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                          width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                          bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
                btn_cancel.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
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
        top = self._create_toplevel_with_size("view_cart", "large")
        top.title("购物车")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=(Styles.SPACING_MD, Styles.SPACING_XS))
        
        tk.Label(
            title_frame, 
            text="购物车", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        if self.system.shopping_cart.is_empty():
            tk.Label(top, text="购物车为空", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XL)
            # 购物车为空时的关闭按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.SPACING_MD)
            btn_close = tk.Button(btn_frame, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack()
        else:
            tk.Label(top, text="购物车商品", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XS)
            
            frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            frame.pack(pady=Styles.SPACING_XS, fill=tk.BOTH, expand=True, padx=Styles.SPACING_LG)
            
            tree = ttk.Treeview(frame, style="Treeview")
            tree["columns"] = ["商品编号", "商品名称", "单价(每斤)", "成本价(每斤)", "数量", "单位", "成本小计", "小计"]
            tree["show"] = "headings"
            
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=110, anchor=tk.CENTER)
            
            total = 0
            total_cost = 0
            for item in self.system.shopping_cart.get_items():
                tree.insert("", tk.END, values=[
                    item['商品编号'],
                    item['商品名称'],
                    f"{item['单价(每斤)']:.2f}",
                    f"{item.get('成本价(每斤)', 0.0):.2f}",
                    item['购买数量'],
                    item['购买单位'],
                    f"{item.get('成本小计', 0.0):.2f}",
                    f"{item['小计']:.2f}"
                ])
                total += item['小计']
                total_cost += item.get('成本小计', 0.0)
            
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 显示总计信息
            info_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            info_frame.pack(pady=Styles.SPACING_SM)
            
            tk.Label(info_frame, text=f"总成本: {total_cost:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XS)
            tk.Label(info_frame, text=f"总计: {total:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.SPACING_XS)
            
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
                
                # 弹出输入框修改数量
                new_quantity = simpledialog.askfloat(
                    "修改数量", 
                    f"请输入新的购买数量 ({unit}):",
                    initialvalue=current_quantity,
                    minvalue=0.1
                )
                
                if new_quantity is not None:
                    # 使用 ShoppingCart 的方法更新数量
                    result = self.system.shopping_cart.update_item_quantity(com_id, new_quantity, unit)
                    if result['success']:
                        # 重新显示购物车
                        top.destroy()
                        self.view_cart_gui()
                    else:
                        messagebox.showerror("错误", result['message'])
            
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
                    # 使用 ShoppingCart 的方法删除
                    self.system.shopping_cart.remove_item(com_id)
                    
                    # 重新显示购物车
                    top.destroy()
                    self.view_cart_gui()
            
            # 添加按钮
            btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
            btn_frame.pack(pady=Styles.SPACING_MD)
            
            btn_delete = tk.Button(btn_frame, text="删除选中商品", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=delete_selected,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_delete.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
            
            # 添加关闭按钮到同一框架
            btn_close = tk.Button(btn_frame, text="关闭", font=Styles.BUTTON_FONT,
                      width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                      bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
            btn_close.pack(side=tk.LEFT, padx=Styles.SPACING_SM)

    def clear_cart_gui(self):
        """清空购物车GUI"""
        if self.system.shopping_cart.is_empty():
            messagebox.showinfo("提示", "购物车已经为空")
            return
        
        if messagebox.askyesno("确认", "确定要清空购物车吗？"):
            self.system.shopping_cart.clear()
            messagebox.showinfo("成功", "购物车已清空")

    def checkout_gui(self):
        """结账GUI"""
        if self.system.shopping_cart.is_empty():
            messagebox.showerror("错误", "购物车为空，无法结账")
            return
        
        top = self._create_toplevel_with_size("checkout", "large")
        top.title("结账")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

        # 创建标题区域
        title_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        title_frame.pack(pady=(Styles.SPACING_MD, Styles.SPACING_XS))
        
        tk.Label(
            title_frame, 
            text="结账", 
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.HEADER_COLOR
        ).pack()

        # 显示购物车内容
        cart_items = self.system.shopping_cart.get_items()
        total_amount = sum(item['小计'] for item in cart_items)
        total_cost = sum(item.get('成本小计', 0.0) for item in cart_items)
        expected_profit = total_amount - total_cost
        
        frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        frame.pack(pady=Styles.SPACING_XS, fill=tk.BOTH, expand=True, padx=Styles.SPACING_LG)
        
        tree = ttk.Treeview(frame, style="Treeview")
        tree["columns"] = ["商品名称", "数量", "单位", "成本小计", "小计"]
        tree["show"] = "headings"
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor=tk.CENTER)
        
        for item in cart_items:
            tree.insert("", tk.END, values=[
                item['商品名称'],
                item['购买数量'],
                item['购买单位'],
                f"{item.get('成本小计', 0.0):.2f}",
                f"{item['小计']:.2f}"
            ])
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 显示成本信息
        info_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        info_frame.pack(pady=Styles.SPACING_SM)
        
        tk.Label(info_frame, text=f"总成本: {total_cost:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XS)
        tk.Label(info_frame, text=f"预期利润: {expected_profit:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.SUCCESS_COLOR).pack(pady=Styles.SPACING_XS)
        tk.Label(info_frame, text=f"应付总额: {total_amount:.2f} 元", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.HEADER_COLOR).pack(pady=Styles.SPACING_XS)
        
        input_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        input_frame.pack(pady=Styles.SPACING_SM)
        
        # 客户名称
        tk.Label(input_frame, text="客户名称: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XS)
        customer_frame = tk.Frame(input_frame, bg=Styles.BACKGROUND_COLOR)
        customer_frame.pack(pady=Styles.SPACING_XS)
        customer_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=customer_var, width=30, font=Styles.TEXT_FONT).pack(side=tk.LEFT, padx=(0, 5))
        btn_select_customer = tk.Button(customer_frame, text="选择...", font=Styles.TEXT_FONT,
                                      width=8, command=lambda: self._select_customer_dialog(customer_var),
                                      bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=5, pady=2)
        btn_select_customer.pack(side=tk.LEFT)
        btn_select_customer.bind("<Enter>", lambda e, b=btn_select_customer: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_select_customer.bind("<Leave>", lambda e, b=btn_select_customer: b.config(bg=Styles.PRIMARY_COLOR))
        
        # 实收金额
        tk.Label(input_frame, text="实收金额: ", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).pack(pady=Styles.SPACING_XS)
        received_var = tk.StringVar(value=str(total_amount))
        tk.Entry(input_frame, textvariable=received_var, width=30, font=Styles.TEXT_FONT).pack(pady=Styles.SPACING_XS)
        
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
                
                # 无论实收金额是高还是低，都按比例分配给每个商品
                discount_ratio = received_amount / total_amount if total_amount > 0 else 1.0
                
                # 处理销售记录 - 统一以"斤"为单位
                for item in self.system.shopping_cart.get_items():
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
                if received_amount < total_amount:
                    message = f"结账成功！\n应付: {total_amount:.2f} 元\n实收: {received_amount:.2f} 元\n折扣: {total_amount - received_amount:.2f} 元"
                elif received_amount > total_amount:
                    message = f"结账成功！\n应付: {total_amount:.2f} 元\n实收: {received_amount:.2f} 元\n溢价: {received_amount - total_amount:.2f} 元"
                else:
                    message = f"结账成功！\n应付: {total_amount:.2f} 元\n实收: {received_amount:.2f} 元"
                messagebox.showinfo("成功", message)
                
                # 清空购物车
                self.system.shopping_cart.clear()
                top.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额")
        
        btn_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        btn_frame.pack(pady=Styles.SPACING_MD)
        
        btn_confirm = tk.Button(btn_frame, text="确认结账", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=process_checkout,
                  bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_confirm.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
        btn_confirm.bind("<Enter>", lambda e, b=btn_confirm: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_confirm.bind("<Leave>", lambda e, b=btn_confirm: b.config(bg=Styles.PRIMARY_COLOR))
        
        btn_cancel = tk.Button(btn_frame, text="取消", font=Styles.BUTTON_FONT,
                  width=Styles.BUTTON_WIDTH, height=Styles.BUTTON_HEIGHT, command=top.destroy,
                  bg=Styles.ERROR_COLOR, fg="white", relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=Styles.SPACING_SM)
