#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查成本计算问题
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import pandas as pd

def check_cost_calculation_issue():
    """检查成本计算问题"""
    print("销售统计成本计算问题检查")
    print("="*50)
    
    system = TeaInventorySystem()
    
    # 获取销售记录
    sales_df = system.excel_manager.get_all_sales()
    if not sales_df.empty and len(sales_df) > 1:
        sales_df = sales_df.iloc[1:]
        print("销售记录详情:")
        for idx, row in sales_df.iterrows():
            print(f"  {idx}: 商品编号={row['商品编号']}, 商品名称={row['商品名称']}, "
                  f"销售数量={row['销售数量']}, 实收金额={row['实收金额']}, "
                  f"销售单位={row.get('销售单位', '未知')}")
    
    # 获取商品信息
    commodity_df = system.excel_manager.get_all_commodities()
    if not commodity_df.empty and len(commodity_df) > 1:
        commodity_df = commodity_df.iloc[1:]
        print("\n商品信息详情:")
        for idx, row in commodity_df.iterrows():
            print(f"  {idx}: 编号={row['商品编号']}, 名称={row['商品名称']}, "
                  f"茶类={row['茶类']}, 品种={row['品种']}, "
                  f"成本价={row['成本价']}, 零售价={row['零售价']}, "
                  f"当前库存={row['当前库存']}")
    
    # 数据合并和成本计算检查
    if not sales_df.empty and not commodity_df.empty:
        print("\n数据合并检查:")
        merged_df = pd.merge(sales_df, commodity_df[['商品编号', '茶类', '品种', '成本价', '零售价']], 
                           on='商品编号', how='left')
        
        print("合并后的数据及成本计算:")
        for idx, row in merged_df.iterrows():
            print(f"  {idx}: 商品={row['商品名称']}, 销售数量={row['销售数量']}, "
                  f"成本价(每斤)={row['成本价']}, 销售收入={row['实收金额']}")
            
            # 计算销售成本
            sales_cost = row['销售数量'] * row['成本价']
            print(f"       销售成本计算: {row['销售数量']}斤 × {row['成本价']}元/斤 = {sales_cost}元")
            print(f"       利润: {row['实收金额']} - {sales_cost} = {row['实收金额'] - sales_cost}元")
    
    print(f"\n{'='*50}")
    print("问题诊断:")
    print("可能的原因:")
    print("1. 成本价数据录入错误（例如录入了总价值而非单价）")
    print("2. 销售数量和成本价的单位不匹配")
    print("3. 需要在成本计算时考虑销售单位（斤/克）")

def fix_cost_calculation():
    """修复成本计算逻辑以考虑单位"""
    print(f"\n修复成本计算逻辑以考虑销售单位")
    
    system = TeaInventorySystem()
    
    # 获取数据
    sales_df = system.excel_manager.get_all_sales()
    commodity_df = system.excel_manager.get_all_commodities()
    
    if not sales_df.empty and len(sales_df) > 1:
        sales_df = sales_df.iloc[1:]
    if not commodity_df.empty and len(commodity_df) > 1:
        commodity_df = commodity_df.iloc[1:]
    
    if not sales_df.empty and not commodity_df.empty:
        merged_df = pd.merge(sales_df, commodity_df[['商品编号', '成本价']], 
                           on='商品编号', how='left')
        
        # 确保数值列是数字类型
        merged_df['销售数量'] = pd.to_numeric(merged_df['销售数量'], errors='coerce')
        merged_df['成本价'] = pd.to_numeric(merged_df['成本价'], errors='coerce')
        merged_df['实收金额'] = pd.to_numeric(merged_df['实收金额'], errors='coerce')
        
        # 处理销售单位
        if '销售单位' in merged_df.columns:
            # 如果销售单位是克，需要转换为斤来计算成本
            for idx, row in merged_df.iterrows():
                quantity = row['销售数量']
                unit = row.get('销售单位', '斤')
                
                if unit == '克':
                    quantity_in_jin = quantity / 500  # 克转斤
                else:  # 默认是斤
                    quantity_in_jin = quantity
                
                cost = quantity_in_jin * row['成本价']
                income = row['实收金额']
                profit = income - cost
                
                print(f"修正计算 - 商品:{row['商品名称']}, 销售:{row['销售数量']}{unit}, "
                      f"转换后斤数:{quantity_in_jin}, 成本价:{row['成本价']}/斤, "
                      f"销售成本:{cost:.2f}, 收入:{income}, 利润:{profit:.2f}")

def main():
    check_cost_calculation_issue()
    fix_cost_calculation()

if __name__ == "__main__":
    main()