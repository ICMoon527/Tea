#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深入检查销售记录读取问题
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import pandas as pd

def deep_check_sales_issue():
    """深入检查销售记录读取问题"""
    print("深入检查销售记录读取问题")
    print("="*70)
    
    system = TeaInventorySystem()
    
    print("\n【1. 直接使用pandas读取Excel销售记录】")
    excel_file = "e:/工作/Code/Tea/tea_inventory.xlsx"
    sales_df_direct = pd.read_excel(excel_file, sheet_name="销售记录")
    print(f"直接读取的销售记录数: {len(sales_df_direct)}")
    print("直接读取的销售记录:")
    for idx, (_, row) in enumerate(sales_df_direct.iterrows(), 1):
        print(f"  {idx}. 编号: {row['销售编号']}, 商品: {row['商品名称']} ({row['商品编号']})")
    
    print(f"\n【2. 通过系统接口读取销售记录】")
    sales_df_system = system.excel_manager.get_all_sales()
    print(f"系统接口读取的销售记录数: {len(sales_df_system)}")
    print("系统接口读取的销售记录:")
    for idx, (_, row) in enumerate(sales_df_system.iterrows(), 1):
        print(f"  {idx}. 编号: {row['销售编号']}, 商品: {row['商品名称']} ({row['商品编号']})")
    
    print(f"\n【3. 比较差异】")
    direct_ids = set(str(row['销售编号']) for _, row in sales_df_direct.iterrows())
    system_ids = set(str(row['销售编号']) for _, row in sales_df_system.iterrows()) if not sales_df_system.empty else set()
    
    print(f"直接读取的ID: {direct_ids}")
    print(f"系统读取的ID: {system_ids}")
    print(f"直接读取有但系统没有的ID: {direct_ids - system_ids}")
    print(f"系统有但直接读取没有的ID: {system_ids - direct_ids}")
    
    print(f"\n【4. 检查ExcelManager的get_all_sales方法】")
    # 查看ExcelManager源码
    import inspect
    print(inspect.getsource(system.excel_manager.get_all_sales))
    
    print(f"\n【5. 检查具体缺失的记录】")
    target_id = 'S202602081855035823'
    direct_target = sales_df_direct[sales_df_direct['销售编号'] == target_id]
    if not direct_target.empty:
        print(f"直接读取中找到目标记录: {dict(direct_target.iloc[0])}")
    
    if not sales_df_system.empty:
        system_target = sales_df_system[sales_df_system['销售编号'] == target_id]
        if not system_target.empty:
            print(f"系统读取中找到目标记录: {dict(system_target.iloc[0])}")
        else:
            print(f"系统读取中未找到目标记录 {target_id}")

if __name__ == "__main__":
    deep_check_sales_issue()