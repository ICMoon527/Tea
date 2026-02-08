#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
茶叶进销存系统新功能演示脚本
展示了两个主要改进：
1. 自动生成不重复编号
2. 显示历史品种列表
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from excel_manager import ExcelManager
import pandas as pd

def demonstrate_auto_id_generation():
    """演示自动生成编号功能"""
    print("茶叶进销存系统 - 新功能演示")
    print("="*60)
    print("\n【功能改进一】 自动生成不重复的随机编号")
    print("-" * 40)
    
    excel_manager = ExcelManager()
    
    print("现在的系统支持以下自动编号：")
    print("• 商品编号 (以'C'开头): ", excel_manager.generate_id("C", "商品信息", "商品编号"))
    print("• 销售编号 (以'S'开头): ", excel_manager.generate_id("S", "销售记录", "销售编号"))
    print("• 进货编号 (以'I'开头): ", excel_manager.generate_id("I", "进货记录", "进货编号"))
    print("• 供应商编号 (以'SP'开头): ", excel_manager.generate_id("SP", "供应商", "供应商编号"))
    
    print("\n💡 使用说明：")
    print("  - 用户在添加商品/销售/进货/供应商时，可选择留空编号字段")
    print("  - 系统将自动生成唯一的随机编号，确保不会重复")
    print("  - 编号包含时间戳和随机数，保证全局唯一性")

def demonstrate_product_lists():
    """演示历史品种列表功能"""
    print("\n\n【功能改进二】 显示历史品种列表")
    print("-" * 40)
    
    excel_manager = ExcelManager()
    
    # 演示可销售商品列表（仅显示有库存的商品）
    print("1. 销售时显示可销售商品列表：")
    all_commodities = excel_manager.get_all_commodities()
    if not all_commodities.empty and len(all_commodities) > 1:
        all_commodities = all_commodities.iloc[1:]  # 移除标题行
        available_commodities = all_commodities[all_commodities['当前库存'].astype(float) > 0]
        print(f"   系统中有 {len(available_commodities)} 种有库存的商品可供销售：")
        for idx, (index, row) in enumerate(available_commodities.iterrows(), 1):
            stock_jin = float(row['当前库存'])
            stock_ke = stock_jin * 500
            print(f"   {idx}. {row['商品名称']} (编号: {row['商品编号']}) - 库存: {stock_jin}斤")
    
    # 演示历史进货品种列表
    print("\n2. 进货时显示历史进货品种列表：")
    df_stocks = excel_manager.get_all_stocks()
    if not df_stocks.empty and len(df_stocks) > 1:
        df_stocks = df_stocks.iloc[1:]  # 移除标题行
        if not df_stocks.empty:
            unique_products = df_stocks[['商品编号', '商品名称']].drop_duplicates()
            print(f"   系统记录了 {len(unique_products)} 种历史进货品种：")
            for idx, row in unique_products.iterrows():
                print(f"   {idx+1}. {row['商品名称']} (编号: {row['商品编号']})")
    
    print("\n💡 使用说明：")
    print("  - 销售时：系统自动过滤出有库存的商品，用户可直接选择序号")
    print("  - 进货时：系统显示历史进货过的品种，用户可快速选择")
    print("  - 用户仍可手动输入编号，灵活性与便捷性兼备")

def main():
    demonstrate_auto_id_generation()
    demonstrate_product_lists()
    
    print("\n" + "="*60)
    print("✅ 系统改进完成！新功能亮点：")
    print("   ✓ 无需记忆复杂编号规则，系统自动分配")
    print("   ✓ 避免手动输入错误，提高准确性")
    print("   ✓ 提供历史记录参考，提升工作效率")
    print("   ✓ 保留手动输入选项，满足特殊需求")

if __name__ == "__main__":
    main()