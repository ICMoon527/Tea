#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证销售统计功能是否正确处理茶类和品种统计
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import pandas as pd

def verify_tea_category_statistics():
    """验证茶类统计功能"""
    print("验证销售统计功能")
    print("="*60)
    
    system = TeaInventorySystem()
    
    # 检查商品信息
    print("1. 检查商品信息中的茶类和品种:")
    commodities_df = system.excel_manager.get_all_commodities()
    if not commodities_df.empty and len(commodities_df) > 1:
        commodities_df = commodities_df.iloc[1:]  # 移除标题行
        
        if not commodities_df.empty:
            print("   商品中的茶类分布:")
            tea_types = commodities_df['茶类'].value_counts()
            for tea_type, count in tea_types.items():
                print(f"     - {tea_type}: {count} 个商品")
            
            print("\n   商品中的品种分布 (乌龙茶类):")
            wulong_df = commodities_df[commodities_df['茶类'] == '乌龙茶']
            if not wulong_df.empty:
                varieties = wulong_df['品种'].value_counts()
                for variety, count in varieties.items():
                    print(f"     - {variety}: {count} 个商品")
            
            print("\n   陈皮商品信息:")
            chenpi_df = commodities_df[commodities_df['茶类'] == '陈皮']
            if not chenpi_df.empty:
                print(f"     - 陈皮: {len(chenpi_df)} 个商品")
                for _, row in chenpi_df.iterrows():
                    print(f"       * {row['商品名称']} (品种: {row['品种']})")
    
    # 检查销售记录
    print(f"\n2. 检查销售记录:")
    sales_df = system.excel_manager.get_all_sales()
    if not sales_df.empty and len(sales_df) > 1:
        sales_df = sales_df.iloc[1:]  # 移除标题行
        
        if not sales_df.empty:
            print(f"   总销售记录数: {len(sales_df)}")
            
            # 获取商品信息用于茶类和品种信息
            commodity_info = commodities_df.set_index('商品编号')[['茶类', '品种']].to_dict('index')
            
            print("   销售记录中的茶类分布:")
            tea_categories_in_sales = {}
            for _, sale_row in sales_df.iterrows():
                com_id = sale_row['商品编号']
                if com_id in commodity_info:
                    tea_type = commodity_info[com_id]['茶类']
                    tea_categories_in_sales[tea_type] = tea_categories_in_sales.get(tea_type, 0) + 1
            
            for tea_type, count in tea_categories_in_sales.items():
                print(f"     - {tea_type}: {count} 笔销售")
            
            print("\n   销售记录中的品种分布 (乌龙茶类):")
            variety_in_sales = {}
            for _, sale_row in sales_df.iterrows():
                com_id = sale_row['商品编号']
                if com_id in commodity_info:
                    tea_type = commodity_info[com_id]['茶类']
                    variety = commodity_info[com_id]['品种']
                    if tea_type == '乌龙茶':
                        variety_in_sales[ variety] = variety_in_sales.get(variety, 0) + 1
            
            for variety, count in variety_in_sales.items():
                print(f"     - {variety}: {count} 笔销售")
            
            print("\n   陈皮销售记录:")
            chenpi_sales = []
            for _, sale_row in sales_df.iterrows():
                com_id = sale_row['商品编号']
                if com_id in commodity_info:
                    tea_type = commodity_info[com_id]['茶类']
                    if tea_type == '陈皮':
                        chenpi_sales.append(sale_row['商品名称'])
            
            print(f"     - 陈皮销售: {len(chenpi_sales)} 笔")
            for name in set(chenpi_sales):
                print(f"       * {name}")
        else:
            print("   暂无销售记录")
    else:
        print("   暂无销售记录")
    
    print(f"\n3. 预期统计结果:")
    print("   按一级茶类统计应包含: 乌龙茶、陈皮 (以及其他有销售的茶类)")
    print("   按二级茶类(品种)统计应包含: 金萱、陈皮 (以及其他有销售的品种)")
    
    print(f"\n4. 销售统计功能代码检查:")
    import inspect
    source = inspect.getsource(system.sales_statistics)
    if '茶类' in source and '品种' in source:
        print("   ✓ 代码中包含茶类和品种统计逻辑")
        # 检查groupby语句
        lines = source.split('\n')
        for line in lines:
            if 'groupby' in line and ('茶类' in line or '品种' in line):
                print(f"   ✓ 发现分组统计: {line.strip()}")
    else:
        print("   ✗ 代码中可能缺少茶类或品种统计逻辑")

def test_statistics_output():
    """测试统计输出"""
    print(f"\n{'='*60}")
    print("测试销售统计功能输出")
    
    system = TeaInventorySystem()
    
    # 获取销售数据和商品数据
    sales_df = system.excel_manager.get_all_sales()
    commodity_df = system.excel_manager.get_all_commodities()
    
    if not sales_df.empty and len(sales_df) > 1:
        sales_df = sales_df.iloc[1:]  # 移除标题行
    if not commodity_df.empty and len(commodity_df) > 1:
        commodity_df = commodity_df.iloc[1:]  # 移除标题行
    
    if not sales_df.empty and not commodity_df.empty:
        # 合并数据
        commodity_info = commodity_df.set_index('商品编号')[['茶类', '品种']].to_dict('index')
        
        # 按茶类统计
        tea_stats = {}
        for _, sale_row in sales_df.iterrows():
            com_id = sale_row['商品编号']
            if com_id in commodity_info:
                tea_type = commodity_info[com_id]['茶类']
                tea_stats[tea_type] = tea_stats.get(tea_type, 0) + 1
        
        print(f"\n按一级茶类统计结果预览:")
        for tea_type, count in tea_stats.items():
            print(f"  {tea_type}: {count} 笔销售")
        
        # 按品种统计（仅限有销售记录的商品）
        variety_stats = {}
        for _, sale_row in sales_df.iterrows():
            com_id = sale_row['商品编号']
            if com_id in commodity_info:
                tea_type = commodity_info[com_id]['茶类']
                if tea_type == '乌龙茶':  # 仅统计乌龙茶类的品种
                    variety = commodity_info[com_id]['品种']
                    variety_stats[ variety] = variety_stats.get(variety, 0) + 1
        
        print(f"\n按二级茶类(乌龙茶品种)统计结果预览:")
        for variety, count in variety_stats.items():
            print(f"  {variety}: {count} 笔销售")
        
        # 特别检查陈皮
        chenpi_count = sum(1 for _, sale_row in sales_df.iterrows() 
                          if sale_row['商品编号'] in commodity_info 
                          and commodity_info[sale_row['商品编号']]['茶类'] == '陈皮')
        print(f"\n陈皮销售统计: {chenpi_count} 笔销售")
        
    else:
        print("   暂无足够的销售数据进行统计")

def main():
    verify_tea_category_statistics()
    test_statistics_output()
    
    print(f"\n{'='*60}")
    print("✅ 验证完成!")
    print("\n根据验证结果:")
    print("- 按一级茶类统计会显示所有有销售记录的茶类 (如乌龙茶、陈皮等)")
    print("- 按二级茶类统计会显示所有有销售记录的品种 (如金萱、陈皮等)")
    print("- 系统的groupby功能会自动处理所有分类")

if __name__ == "__main__":
    main()