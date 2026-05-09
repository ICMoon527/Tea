import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import os
from styles import Styles


class StatsViewMixin:
    """GUI 视图混入类"""

    def sales_record_management(self):
        """销售记录管理界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "销售记录管理", "查看和查询历史销售记录")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("查看所有销售记录", self.view_all_sales, "📋"),
            ("按客户查询", self.query_sales_by_customer_gui, "👥"),
            ("按商品查询", self.query_sales_by_product_gui, "📦"),
            ("按日期查询", self.query_sales_by_date_gui, "📅")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def view_all_sales(self):
        df = self.system.excel_manager.get_all_sales()
        self.show_dataframe_window(df, "销售记录列表")

    def query_sales_by_customer_gui(self):
        """按客户查询销售记录GUI"""
        top = self._create_toplevel_with_size("query_sales_by_customer", "medium")
        top.title("按客户查询销售记录")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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

        # 客户名称输入区域
        input_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        input_frame.pack(pady=Styles.PADY_LARGE)
        
        tk.Label(input_frame, text="客户名称", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=8)
        customer_var = tk.StringVar()
        customer_entry = tk.Entry(input_frame, textvariable=customer_var, font=Styles.TEXT_FONT, width=25)
        customer_entry.grid(row=0, column=1, pady=8, padx=5)
        
        btn_select_customer = tk.Button(input_frame, text="选择...", font=Styles.BUTTON_FONT,
                                        width=10, command=lambda: self._select_customer_dialog(customer_var),
                                        bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=5, pady=3)
        btn_select_customer.grid(row=0, column=2, pady=8)
        btn_select_customer.bind("<Enter>", lambda e, b=btn_select_customer: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_select_customer.bind("<Leave>", lambda e, b=btn_select_customer: b.config(bg=Styles.PRIMARY_COLOR))

        def query():
            customer_name = customer_var.get().strip()
            if not customer_name:
                messagebox.showerror("错误", "请选择或输入客户名称")
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
        top = self._create_toplevel_with_size("query_sales_by_product", "medium")
        top.title("按商品查询销售记录")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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

        # 商品编号输入区域
        input_frame = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        input_frame.pack(pady=Styles.PADY_LARGE)
        
        tk.Label(input_frame, text="商品编号", font=Styles.LABEL_FONT, bg=Styles.BACKGROUND_COLOR, fg=Styles.TEXT_COLOR).grid(row=0, column=0, sticky='w', pady=8)
        product_var = tk.StringVar()
        product_entry = tk.Entry(input_frame, textvariable=product_var, font=Styles.TEXT_FONT, width=25)
        product_entry.grid(row=0, column=1, pady=8, padx=5)
        
        btn_select_product = tk.Button(input_frame, text="选择...", font=Styles.BUTTON_FONT,
                                       width=10, command=lambda: self._select_product_dialog(product_var),
                                       bg=Styles.PRIMARY_COLOR, fg="white", relief=tk.FLAT, padx=5, pady=3)
        btn_select_product.grid(row=0, column=2, pady=8)
        btn_select_product.bind("<Enter>", lambda e, b=btn_select_product: b.config(bg=Styles.BUTTON_HOVER_COLOR))
        btn_select_product.bind("<Leave>", lambda e, b=btn_select_product: b.config(bg=Styles.PRIMARY_COLOR))

        def query():
            product_id = product_var.get().strip()
            if not product_id:
                messagebox.showerror("错误", "请选择或输入商品编号")
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
        top = self._create_toplevel_with_size("query_sales_by_date", "small")
        top.title("按日期查询销售记录")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
        """统计分析界面 - 现代化设计"""
        self.clear_window()
        
        # 主容器
        main_container = tk.Frame(self.root, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL)
        
        # 页面标题
        self._create_page_header(main_container, "统计分析", "数据分析和可视化报表")
        
        # 按钮区域容器
        buttons_container = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        buttons_container.pack(fill=tk.BOTH, expand=True)
        
        # 按钮网格
        buttons = [
            ("销售统计", self.sales_statistics_gui, "📈"),
            ("热销商品排行", self.top_selling_products_gui, "🏆"),
            ("盈利分析", self.profit_analysis_gui, "💰"),
            ("数据可视化", self.data_visualization_gui, "📊")
        ]
        self._create_button_grid(buttons_container, buttons, columns=2)
        
        # 返回按钮
        self._create_back_button(main_container, self.create_main_menu)

    def sales_statistics_gui(self):
        """销售统计GUI"""
        top = self._create_toplevel_with_size("sales_statistics", "medium")
        top.title("销售统计")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
        top = self._create_toplevel_with_size("statistics_by_time", "medium")
        top.title("按时间统计")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)

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
            result_window = self._create_toplevel_with_size("profit_analysis", "medium")
            result_window.title("盈利分析")
            result_window.configure(bg=Styles.BACKGROUND_COLOR)
            result_window.resizable(True, True)

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
        """数据可视化GUI - 现代化设计"""
        top = self._create_toplevel_with_size("data_visualization", "medium")
        top.title("数据可视化")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
        # 主容器
        main_container = tk.Frame(top, bg=Styles.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=Styles.SPACING_XL, pady=Styles.SPACING_XL)
        
        # 标题
        tk.Label(
            main_container,
            text="选择可视化类型",
            font=Styles.SUB_HEADER_FONT,
            bg=Styles.BACKGROUND_COLOR,
            fg=Styles.TEXT_PRIMARY
        ).pack(pady=(0, Styles.SPACING_LG))
        
        # 按钮网格
        button_grid = tk.Frame(main_container, bg=Styles.BACKGROUND_COLOR)
        button_grid.pack()
        
        buttons = [
            ("📈 销售趋势图", self.show_sales_trend_options),
            ("🥧 商品销量饼图", lambda: self.system.data_viz.plot_product_sales_pie()),
            ("💰 商品利润饼图", lambda: self.system.data_viz.plot_product_profit_pie()),
            ("📊 利润趋势图", self.show_profit_trend_options),
            ("🍵 茶类销售对比图", lambda: self.system.data_viz.plot_tea_category_sales())
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            btn = ttk.Button(
                button_grid,
                text=text,
                command=command,
                style="Modern.TButton"
            )
            btn.grid(row=row, column=col, padx=Styles.SPACING_SM, pady=Styles.SPACING_SM, sticky="ew")
            button_grid.grid_columnconfigure(col, weight=1)
        
        # 关闭按钮
        ttk.Button(
            main_container,
            text="关闭",
            command=top.destroy,
            style="Danger.TButton"
        ).pack(pady=(Styles.SPACING_XL, 0))

    def show_sales_trend_options(self):
        """显示销售趋势图选项"""
        top = self._create_toplevel_with_size("sales_trend_options", "small")
        top.title("销售趋势图 - 选择时间周期")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
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
        top = self._create_toplevel_with_size("profit_trend_options", "small")
        top.title("利润趋势图 - 选择时间周期")
        top.configure(bg=Styles.BACKGROUND_COLOR)
        top.resizable(True, True)
        
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
