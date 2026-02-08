#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
详细对比系统和直接读取的数据
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import pandas as pd

def compare_data():
    print("对比系统读取和直接读取的数据")
    print("="*60)
    
    system = TeaInventorySystem()
    
    # 直接读取
    df_direct = pd.read_excel("e:/工作/Code/Tea/tea_inventory.xlsx", sheet_name="销售记录")
    print(f"直接读取销售记录数: {len(df_direct)}")
    print("直接读取的记录:")
    for i, row in df_direct.iterrows():
        print(f"  {i+1}. {row['销售编号']} - {row['商品名称']}")
    
    # 系统读取
    df_system = system.excel_manager.get_all_sales()
    print(f"\n系统读取销售记录数: {len(df_system)}")
    print("系统读取的记录:")
    for i, row in df_system.iterrows():
        print(f"  {i+1}. {row['销售编号']} - {row['商品名称']}")
    
    print(f"\n差异分析:")
    direct_ids = set(df_direct['销售编号'])
    system_ids = set(df_system['销售编号']) if not df_system.empty else set()
    
    print(f"直接有但系统没有: {direct_ids - system_ids}")
    print(f"系统有但直接没有: {system_ids - direct_ids}")
    
    # 检查系统读取时的处理
    print(f"\n系统读取时跳过了标题行吗？")
    if len(df_system) > 1:
        first_row = df_system.iloc[0]
        print(f"系统读取的第一行: {first_row['销售编号']} - {first_row['商品名称']}")
    
    # 检查是否有过滤条件
    print(f"\n检查系统代码中是否有过滤...")
    # 重现系统中的逻辑
    df_from_system = df_system.copy()
    if not df_from_system.empty and len(df_from_system) > 1:
        df_from_system = df_from_system.iloc[1:]  # 系统代码中会跳过第一行
        print(f"系统跳过第一行后剩余: {len(df_from_system)} 条")
        for i, row in df_from_system.iterrows():
            print(f"  {i+1}. {row['销售编号']} - {row['商品名称']}")

if __name__ == "__main__":
    compare_data()