#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模拟完整的销售流程以复现问题
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import pandas as pd

def simulate_full_sale_process():
    """模拟完整的销售流程"""
    print("模拟完整销售流程")
    print("="*50)
    
    # 创建系统实例
    system = TeaInventorySystem()
    
    print("\n1. 初始状态检查:")
    initial_sales = system.excel_manager.get_all_sales()
    print(f"   销售记录行数: {len(initial_sales)}")
    
    initial_commodities = system.excel_manager.get_all_commodities()
    if len(initial_commodities) > 1:
        initial_stock = initial_commodities.iloc[1:]
        print("   初始库存状态:")
        for idx, row in initial_stock.iterrows():
            print(f"     {row['商品编号']}: {row['商品名称']} - {row['当前库存']}斤")
    
    print("\n2. 模拟添加商品到购物车:")
    # 先查询现有商品
    commodities = system.excel_manager.get_all_commodities()
    if len(commodities) > 1:
        commodities = commodities.iloc[1:]  # 移除标题行
        available = commodities[commodities['当前库存'].astype(float) > 0]
        
        if not available.empty:
            first_available = available.iloc[0]
            com_id = first_available['商品编号']
            com_name = first_available['商品名称']
            current_stock = float(first_available['当前库存'])
            
            print(f"   选择商品: {com_name} (编号: {com_id}), 当前库存: {current_stock}斤")
            
            # 手动添加到购物车（绕过输入）
            cart_item = {
                '商品编号': com_id,
                '商品名称': com_name,
                '单价(每斤)': float(first_available['零售价']),
                '购买数量': min(0.2, current_stock),  # 购买0.2斤或库存量（取较小者）
                '购买单位': '斤',
                '小计': min(0.2, current_stock) * float(first_available['零售价'])
            }
            
            system.shopping_cart.append(cart_item)
            print(f"   已添加到购物车: {cart_item['购买数量']}斤 {com_name}")
            print(f"   购物车总价: {cart_item['小计']:.2f}元")
    
    print(f"\n3. 购物车状态:")
    if system.shopping_cart:
        for i, item in enumerate(system.shopping_cart):
            print(f"   {i+1}. {item['商品名称']} - {item['购买数量']}{item['购买单位']} - {item['小计']:.2f}元")
    else:
        print("   购物车为空")
    
    if system.shopping_cart:
        print("\n4. 执行结账:")
        # 模拟结账过程
        customer_name = "模拟客户"
        total_amount = sum(item['小计'] for item in system.shopping_cart)
        received_amount = total_amount  # 收款等于总价
        
        print(f"   客户: {customer_name}")
        print(f"   应收: {total_amount:.2f}元")
        print(f"   实收: {received_amount:.2f}元")
        
        # 执行销售记录保存逻辑（来自checkout方法）
        for item in system.shopping_cart:
            sale_id = system.excel_manager.generate_id("S", "销售记录", "销售编号")
            # 如果销售单位是克，需要转换为斤来更新库存
            quantity_in_jin = item['购买数量'] / 500 if item['购买单位'] == '克' else item['购买数量']
            
            from sale_record import SaleRecord
            sale_record = SaleRecord(
                sale_id=sale_id,
                com_id=item['商品编号'],
                com_name=item['商品名称'],
                quantity=item['购买数量'],
                unit_price=item['单价(每斤)'],
                total_amount=item['小计'],
                received_amount=item['小计'],
                customer_name=customer_name,
                sale_unit=item['购买单位']
            )
            system.excel_manager.add_sale(sale_record.to_list())
            print(f"   已保存销售记录: {sale_id} - {item['商品名称']}")
        
        print("   销售记录已保存，购物车已清空")
        system.shopping_cart.clear()
    
    print("\n5. 结账后状态检查:")
    after_sales = system.excel_manager.get_all_sales()
    print(f"   销售记录行数: {len(after_sales)}")
    
    if len(after_sales) > 1:
        sales_content = after_sales.iloc[1:]
        print(f"   实际销售记录数: {len(sales_content)}")
        for idx, row in sales_content.iterrows():
            print(f"     {idx}. {row['商品名称']} - {row['销售数量']}{row['销售单位']} - {row['实收金额']:.2f}元")
    
    # 再次检查商品库存
    after_commodities = system.excel_manager.get_all_commodities()
    if len(after_commodities) > 1:
        after_stock = after_commodities.iloc[1:]
        print("   结账后库存状态:")
        for idx, row in after_stock.iterrows():
            print(f"     {row['商品编号']}: {row['商品名称']} - {row['当前库存']}斤")

def test_system_statistics():
    """测试系统统计功能"""
    print("\n" + "="*50)
    print("测试系统统计功能")
    
    system = TeaInventorySystem()
    
    print("\n调用系统销售统计方法:")
    try:
        system.sales_statistics()
    except Exception as e:
        print(f"统计方法出错: {e}")
        import traceback
        traceback.print_exc()

def main():
    simulate_full_sale_process()
    test_system_statistics()
    print(f"\n{'='*50}")
    print("流程模拟完成")

if __name__ == "__main__":
    main()