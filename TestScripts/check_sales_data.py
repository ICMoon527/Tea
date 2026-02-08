#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查茶叶进销存系统中的销售记录数据
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from excel_manager import ExcelManager
import pandas as pd

def check_sales_data():
    """检查销售记录数据"""
    print("茶叶进销存系统 - 数据完整性检查")
    print("="*50)
    
    excel_manager = ExcelManager()
    
    # 检查销售记录表
    print("\n【销售记录表检查】")
    sales_df = excel_manager.get_all_sales()
    print(f"销售记录表总行数: {len(sales_df)}")
    
    if not sales_df.empty:
        print(f"销售记录表列名: {list(sales_df.columns)}")
        if len(sales_df) > 1:
            sales_df_content = sales_df.iloc[1:]  # 移除标题行
            print(f"实际销售记录数量: {len(sales_df_content)}")
            
            if not sales_df_content.empty:
                print("\n销售记录详情:")
                for idx, row in sales_df_content.iterrows():
                    print(f"  记录 {idx}: 销售编号={row['销售编号']}, "
                          f"商品编号={row['商品编号']}, 商品名称={row['商品名称']}, "
                          f"销售数量={row['销售数量']}, 销售单位={row['销售单位'] if '销售单位' in row.index else '未知'}")
            else:
                print("  没有实际的销售记录")
        else:
            print("  只有标题行，没有实际的销售记录")
    else:
        print("  销售记录表为空")
    
    # 检查商品信息表
    print("\n【商品信息表检查】")
    commodity_df = excel_manager.get_all_commodities()
    print(f"商品信息表总行数: {len(commodity_df)}")
    
    if not commodity_df.empty and len(commodity_df) > 1:
        commodity_df_content = commodity_df.iloc[1:]  # 移除标题行
        print(f"实际商品数量: {len(commodity_df_content)}")
        
        print("\n商品库存状态:")
        for idx, row in commodity_df_content.iterrows():
            print(f"  商品 {idx}: 编号={row['商品编号']}, 名称={row['商品名称']}, "
                  f"当前库存={row['当前库存']}")
    else:
        print("  没有商品信息")
    
    # 检查系统统计功能
    print("\n【系统统计功能检查】")
    try:
        from tea_inventory_system import TeaInventorySystem
        system = TeaInventorySystem()
        
        # 测试获取销售记录
        sys_sales_df = system.excel_manager.get_all_sales()
        print(f"系统获取的销售记录总行数: {len(sys_sales_df)}")
        
        if len(sys_sales_df) > 1:
            sys_sales_content = sys_sales_df.iloc[1:]  # 移除标题行
            print(f"系统获取的实际销售记录数量: {len(sys_sales_content)}")
        else:
            print("  系统获取的销售记录为空")
            
    except Exception as e:
        print(f"  系统统计功能检查出错: {e}")

def test_sales_query_methods():
    """测试不同的销售记录查询方法"""
    print("\n" + "="*50)
    print("【销售记录查询方法测试】")
    
    from tea_inventory_system import TeaInventorySystem
    system = TeaInventorySystem()
    
    # 方法1: 直接从ExcelManager获取
    print("\n方法1 - ExcelManager.get_all_sales():")
    raw_sales = system.excel_manager.get_all_sales()
    print(f"  总行数: {len(raw_sales)}")
    if len(raw_sales) > 1:
        content = raw_sales.iloc[1:]
        print(f"  实际数据行: {len(content)}")
        for idx, row in content.iterrows():
            print(f"    {idx}: {row.get('商品名称', 'N/A')} - {row.get('销售数量', 'N/A')}")
    
    # 方法2: 通过系统方法
    print("\n方法2 - 系统内部调用:")
    try:
        # 模拟系统统计方法中的处理
        df = system.excel_manager.get_all_sales()
        print(f"  获取的总行数: {len(df)}")
        if df.empty or len(df) <= 1:
            print("  数据为空或只有标题行")
        else:
            df_content = df.iloc[1:]  # 移除标题行
            print(f"  实际数据行: {len(df_content)}")
            if not df_content.empty:
                for idx, row in df_content.iterrows():
                    print(f"    {idx}: {row.get('商品名称', 'N/A')} - {row.get('销售数量', 'N/A')}")
    except Exception as e:
        print(f"  处理出错: {e}")

def main():
    check_sales_data()
    test_sales_query_methods()
    print(f"\n{'='*50}")
    print("✅ 数据检查完成！")

if __name__ == "__main__":
    main()