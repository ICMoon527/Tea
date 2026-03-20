
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
import pandas as pd
from datetime import datetime
from utils import convert_to_jin
import numpy as np


matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.dpi'] = 150
matplotlib.rcParams['savefig.dpi'] = 150
matplotlib.rcParams['savefig.bbox'] = 'tight'
matplotlib.rcParams['savefig.pad_inches'] = 0.1


class DataVisualization:
    """数据可视化类 - SCI论文标准"""

    def __init__(self, excel_manager):
        self.excel_manager = excel_manager
        
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'tertiary': '#F18F01',
            'success': '#4CAF50',
            'info': '#2196F3',
            'warning': '#FF9800',
            'danger': '#F44336'
        }
        
        self.markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
        
        self.line_styles = ['-', '--', '-.', ':']

    def _apply_scientific_style(self, ax, title=None, xlabel=None, ylabel=None, 
                                 grid=True, legend_loc='best'):
        """应用SCI论文风格
        
        Args:
            ax: matplotlib轴对象
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            grid: 是否显示网格
            legend_loc: 图例位置
        """
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12, fontweight='medium')
        
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12, fontweight='medium')
        
        for tick in ax.get_xticklabels():
            tick.set_fontsize(10)
        
        for tick in ax.get_yticklabels():
            tick.set_fontsize(10)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.2)
        ax.spines['bottom'].set_linewidth(1.2)
        
        if grid:
            ax.grid(True, linestyle='--', alpha=0.6, color='gray', linewidth=0.8)
        
        if ax.get_legend_handles_labels()[0]:
            ax.legend(fontsize=10, loc=legend_loc, frameon=True, 
                     framealpha=0.9, edgecolor='lightgray')

    def plot_sales_trend(self, period='day'):
        """绘制销售趋势图 - SCI论文标准

        Args:
            period: 'day'按日, 'week'按周, 'month'按月
        """
        df = self.excel_manager.get_all_sales()
        if df.empty:
            print("暂无销售记录")
            return

        df['销售日期'] = pd.to_datetime(df['销售日期'])

        if period == 'day':
            df['period'] = df['销售日期'].dt.date
            period_label = '日'
        elif period == 'week':
            df['period'] = df['销售日期'].dt.to_period('W')
            period_label = '周'
        elif period == 'month':
            df['period'] = df['销售日期'].dt.to_period('M')
            period_label = '月'
        else:
            print("无效的时间周期")
            return

        sales_by_period = df.groupby('period')['实收金额'].sum()

        fig, ax = plt.subplots(figsize=(6.5, 3.9))
        
        x = np.arange(len(sales_by_period))
        line1, = ax.plot(x, sales_by_period.values, marker=self.markers[0], 
                        linestyle=self.line_styles[0], linewidth=2.5, 
                        markersize=8, color=self.colors['primary'], 
                        label='销售额')
        
        if len(x) >= 2:
            try:
                z = np.polyfit(x, sales_by_period.values, 1)
                p = np.poly1d(z)
                line2, = ax.plot(x, p(x), linestyle=self.line_styles[1], 
                                linewidth=1.5, color=self.colors['secondary'], 
                                label='趋势线')
            except:
                pass
        
        ax.set_xticks(x)
        ax.set_xticklabels([str(p) for p in sales_by_period.index], rotation=45, ha='right')
        
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        self._apply_scientific_style(
            ax,
            title=f'销售趋势图（按{period_label}）',
            xlabel='时间',
            ylabel='销售额（元）',
            grid=True,
            legend_loc='upper left'
        )
        
        plt.tight_layout()
        plt.show()

    def plot_product_sales_pie(self):
        """绘制商品销量饼图 - SCI论文标准"""
        df = self.excel_manager.get_all_sales()
        if df.empty:
            print("暂无销售记录")
            return

        def get_qty_jin(row):
            return convert_to_jin(row['销售数量'], row.get('销售单位', '克'))

        df['销量(斤)'] = df.apply(get_qty_jin, axis=1)

        sales_by_product = df.groupby('商品名称')['销量(斤)'].sum()
        sales_by_product = sales_by_product.sort_values(ascending=False)

        top_10 = sales_by_product.head(10)
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_10)))

        fig, ax = plt.subplots(figsize=(6.5, 5.2))
        
        wedges, texts, autotexts = ax.pie(
            top_10.values,
            labels=top_10.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
            textprops={'fontsize': 10},
            pctdistance=0.85
        )
        
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title('商品销量占比（前10名）', fontsize=14, fontweight='bold', pad=20)
        
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def plot_product_profit_pie(self):
        """绘制商品利润饼图 - SCI论文标准"""
        df_sales = self.excel_manager.get_all_sales()
        df_products = self.excel_manager.get_all_commodities()

        if df_sales.empty or df_products.empty:
            print("数据不足")
            return

        if '是否作废' in df_sales.columns:
            df_sales = df_sales[df_sales['是否作废'] != True]

        if df_sales.empty:
            print("暂无有效销售记录")
            return

        merged = pd.merge(df_sales, df_products[['商品编号', '成本价']], on='商品编号', how='left')

        def calculate_profit(row):
            qty_jin = convert_to_jin(row['销售数量'], row.get('销售单位', '克'))
            cost = qty_jin * row['成本价']
            return row['实收金额'] - cost

        merged['利润'] = merged.apply(calculate_profit, axis=1)

        profit_by_product = merged.groupby('商品名称')['利润'].sum()
        profit_by_product = profit_by_product.sort_values(ascending=False)

        top_10 = profit_by_product.head(10)
        
        colors = plt.cm.Paired(np.linspace(0, 1, len(top_10)))

        fig, ax = plt.subplots(figsize=(6.5, 5.2))
        
        wedges, texts, autotexts = ax.pie(
            top_10.values,
            labels=top_10.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
            textprops={'fontsize': 10},
            pctdistance=0.85
        )
        
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title('商品利润占比（前10名）', fontsize=14, fontweight='bold', pad=20)
        
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def plot_profit_trend(self, period='month'):
        """绘制利润趋势图 - SCI论文标准"""
        df_sales = self.excel_manager.get_all_sales()
        df_products = self.excel_manager.get_all_commodities()

        if df_sales.empty or df_products.empty:
            print("数据不足")
            return

        df_sales['销售日期'] = pd.to_datetime(df_sales['销售日期'])

        merged = pd.merge(df_sales, df_products[['商品编号', '成本价']], on='商品编号', how='left')

        def calculate_profit(row):
            qty_jin = convert_to_jin(row['销售数量'], row.get('销售单位', '克'))
            cost = qty_jin * row['成本价']
            return row['实收金额'] - cost

        merged['利润'] = merged.apply(calculate_profit, axis=1)

        if period == 'day':
            merged['period'] = merged['销售日期'].dt.date
            period_label = '日'
        elif period == 'week':
            merged['period'] = merged['销售日期'].dt.to_period('W')
            period_label = '周'
        elif period == 'month':
            merged['period'] = merged['销售日期'].dt.to_period('M')
            period_label = '月'
        else:
            print("无效的时间周期")
            return

        profit_by_period = merged.groupby('period')['利润'].sum()
        revenue_by_period = merged.groupby('period')['实收金额'].sum()

        fig, ax = plt.subplots(figsize=(6.5, 3.9))
        
        x = np.arange(len(profit_by_period))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, profit_by_period.values, width, 
                      label='利润', color=self.colors['primary'], 
                      edgecolor='darkblue', linewidth=1.2, alpha=0.8)
        
        bars2 = ax.bar(x + width/2, revenue_by_period.values, width, 
                      label='销售额', color=self.colors['tertiary'], 
                      edgecolor='darkorange', linewidth=1.2, alpha=0.8)
        
        ax.set_xticks(x)
        ax.set_xticklabels([str(p) for p in profit_by_period.index], rotation=45, ha='right')
        
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height):,}',
                       ha='center', va='bottom', fontsize=8)
        
        self._apply_scientific_style(
            ax,
            title=f'利润趋势图（按{period_label}）',
            xlabel='时间',
            ylabel='金额（元）',
            grid=True,
            legend_loc='upper left'
        )
        
        plt.tight_layout()
        plt.show()

    def plot_tea_category_sales(self):
        """绘制茶类销售对比图 - SCI论文标准"""
        df_sales = self.excel_manager.get_all_sales()
        df_products = self.excel_manager.get_all_commodities()

        if df_sales.empty or df_products.empty:
            print("数据不足")
            return

        merged = pd.merge(df_sales, df_products[['商品编号', '茶类']], on='商品编号', how='left')

        def get_qty_jin(row):
            return convert_to_jin(row['销售数量'], row.get('销售单位', '克'))

        merged['销量(斤)'] = merged.apply(get_qty_jin, axis=1)

        sales_by_category = merged.groupby('茶类').agg({
            '销量(斤)': 'sum',
            '实收金额': 'sum'
        })

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.1, 3.9))
        
        colors1 = plt.cm.Blues(np.linspace(0.4, 0.9, len(sales_by_category)))
        bars1 = ax1.bar(sales_by_category.index, sales_by_category['销量(斤)'], 
                       color=colors1, edgecolor='navy', linewidth=1.2)
        ax1.set_title('各茶类销量对比', fontsize=12, fontweight='bold', pad=15)
        ax1.set_ylabel('销量（斤）', fontsize=11)
        ax1.tick_params(axis='x', rotation=45)
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)
        
        colors2 = plt.cm.Reds(np.linspace(0.4, 0.9, len(sales_by_category)))
        bars2 = ax2.bar(sales_by_category.index, sales_by_category['实收金额'], 
                       color=colors2, edgecolor='darkred', linewidth=1.2)
        ax2.set_title('各茶类销售额对比', fontsize=12, fontweight='bold', pad=15)
        ax2.set_ylabel('销售额（元）', fontsize=11)
        ax2.tick_params(axis='x', rotation=45)
        
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=9)
        
        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(1.2)
            ax.spines['bottom'].set_linewidth(1.2)
            ax.grid(True, linestyle='--', alpha=0.6, color='gray', linewidth=0.8, axis='y')
            for tick in ax.get_xticklabels():
                tick.set_fontsize(10)
            for tick in ax.get_yticklabels():
                tick.set_fontsize(10)
        
        plt.tight_layout()
        plt.show()

    def show_chart_menu(self):
        """图表菜单"""
        while True:
            print("\n=== 数据可视化 ===")
            print("1. 销售趋势图")
            print("2. 商品销量饼图")
            print("3. 利润趋势图")
            print("4. 茶类销售对比图")
            print("0. 返回上级菜单")

            choice = input("请选择: ").strip()

            if choice == '1':
                print("\n请选择时间周期:")
                print("1. 按日")
                print("2. 按周")
                print("3. 按月")
                p_choice = input("请选择: ").strip()
                period_map = {'1': 'day', '2': 'week', '3': 'month'}
                if p_choice in period_map:
                    self.plot_sales_trend(period_map[p_choice])
            elif choice == '2':
                self.plot_product_sales_pie()
            elif choice == '3':
                print("\n请选择时间周期:")
                print("1. 按日")
                print("2. 按周")
                print("3. 按月")
                p_choice = input("请选择: ").strip()
                period_map = {'1': 'day', '2': 'week', '3': 'month'}
                if p_choice in period_map:
                    self.plot_profit_trend(period_map[p_choice])
            elif choice == '4':
                self.plot_tea_category_sales()
            elif choice == '0':
                break
            else:
                print("无效选择")
