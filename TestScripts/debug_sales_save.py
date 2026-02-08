#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试销售记录保存问题
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from excel_manager import ExcelManager
from sale_record import SaleRecord
import pandas as pd

def debug_add_sale():
    """调试add_sale方法"""
    print("销售记录保存调试")
    print("="*40)
    
    excel_manager = ExcelManager()
    
    # 检查销售记录表的初始状态
    print("\n1. 初始销售记录表状态:")
    initial_df = excel_manager.get_all_sales()
    print(f"   行数: {len(initial_df)}")
    if len(initial_df) > 1:
        content = initial_df.iloc[1:]
        print(f"   数据行数: {len(content)}")
    
    # 创建一个测试销售记录
    print("\n2. 创建测试销售记录:")
    test_sale = SaleRecord(
        sale_id=excel_manager.generate_id("S", "销售记录", "销售编号"),
        com_id="T002",
        com_name="明前西湖龙井",
        quantity=0.5,
        unit_price=800.0,
        total_amount=400.0,
        received_amount=400.0,
        customer_name="测试客户",
        sale_unit="斤"
    )
    
    sale_data = test_sale.to_list()
    print(f"   销售数据: {sale_data}")
    
    # 调用add_sale方法
    print("\n3. 调用add_sale方法:")
    try:
        excel_manager.add_sale(sale_data)
        print("   ✓ add_sale方法执行成功")
    except Exception as e:
        print(f"   ✗ add_sale方法执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 检查销售记录表的状态变化
    print("\n4. 保存后的销售记录表状态:")
    after_df = excel_manager.get_all_sales()
    print(f"   行数: {len(after_df)}")
    if len(after_df) > 1:
        content = after_df.iloc[1:]
        print(f"   数据行数: {len(content)}")
        if not content.empty:
            for idx, row in content.iterrows():
                print(f"   数据行 {idx}: {dict(row)}")
    else:
        print("   仍然只有标题行")
    
    # 检查Excel文件是否真的被修改了
    print("\n5. 直接读取Excel文件验证:")
    try:
        direct_read = pd.read_excel(excel_manager.filename, sheet_name="销售记录", engine='openpyxl')
        print(f"   直接读取行数: {len(direct_read)}")
        if len(direct_read) > 1:
            direct_content = direct_read.iloc[1:]
            print(f"   直接读取数据行数: {len(direct_content)}")
            if not direct_content.empty:
                for idx, row in direct_content.iterrows():
                    print(f"   直接读取行 {idx}: {dict(row)}")
    except Exception as e:
        print(f"   直接读取失败: {e}")

def debug_append_method():
    """调试append_to_sheet方法"""
    print("\n" + "="*40)
    print("append_to_sheet方法调试")
    
    excel_manager = ExcelManager()
    
    # 检查append_to_sheet方法是否正常工作
    test_data = ["DEBUG001", "TEST001", "测试商品", 1.0, 100.0, 100.0, 100.0, "测试客户", "2024-01-01 12:00:00", "斤"]
    
    print(f"\n测试数据: {test_data}")
    
    try:
        excel_manager.append_to_sheet("销售记录", test_data)
        print("✓ append_to_sheet执行成功")
        
        # 验证是否真的添加了数据
        df = excel_manager.read_sheet("销售记录")
        print(f"追加后行数: {len(df)}")
        if len(df) > 1:
            content = df.iloc[1:]
            print(f"数据行数: {len(content)}")
            last_row = content.iloc[-1] if len(content) > 0 else None
            if last_row is not None:
                print(f"最后一行: {dict(last_row)}")
                
    except Exception as e:
        print(f"✗ append_to_sheet执行失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    debug_add_sale()
    debug_append_method()
    print(f"\n{'='*40}")
    print("调试完成")

if __name__ == "__main__":
    main()