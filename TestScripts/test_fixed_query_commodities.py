#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修复后的查询所有商品功能
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem

def test_query_all_commodities():
    """测试查询所有商品功能"""
    print("测试修复后的查询所有商品功能")
    print("="*50)
    
    system = TeaInventorySystem()
    
    # 获取所有商品信息而不打印表格，直接检查数据
    df = system.excel_manager.get_all_commodities()
    print(f"原始DataFrame行数: {len(df)}")
    
    if len(df) > 0:
        print(f"第一行商品编号: {df.iloc[0]['商品编号'] if '商品编号' in df.columns else 'N/A'}")
        print(f"第一行商品名称: {df.iloc[0]['商品名称'] if '商品名称' in df.columns else 'N/A'}")
    
    # 执行查询所有商品功能
    print(f"\n执行查询所有商品功能:")
    system.query_all_commodities()

def main():
    test_query_all_commodities()

if __name__ == "__main__":
    main()