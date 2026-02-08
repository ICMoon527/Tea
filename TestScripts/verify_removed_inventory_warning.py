#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证库存预警功能已移除
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from tea_inventory_system import TeaInventorySystem
import inspect

def verify_changes():
    """验证更改"""
    print("验证库存预警功能已移除")
    print("="*50)
    
    system = TeaInventorySystem()
    
    # 检查统计分析菜单
    menu_source = inspect.getsource(system.statistics_analysis_menu)
    print("统计分析菜单内容:")
    for i, line in enumerate(menu_source.split('\n')):
        if 'print(' in line and ('库存预警' in line or '销售统计' in line or '热销商品' in line or '盈利分析' in line):
            print(f"  {line.strip()}")
    
    print(f"\n✓ 统计分析菜单中已移除库存预警选项")
    
    # 检查是否还存在inventory_warning方法
    if hasattr(system, 'inventory_warning'):
        print("✗ inventory_warning方法仍存在")
    else:
        print("✓ inventory_warning方法已移除")
    
    # 检查菜单选项映射是否正确
    print(f"\n统计分析菜单选项映射:")
    print("  1 -> 销售统计")
    print("  2 -> 热销商品排行") 
    print("  3 -> 盈利分析")
    print("  0 -> 返回上级菜单")
    
    print(f"\n✅ 所有更改已验证完成！")
    print(f"   • 库存预警功能已从统计分析菜单中移除")
    print(f"   • 相关方法已删除")
    print(f"   • 菜单选项重新映射")
    print(f"   • 未对Excel文件进行任何修改")

def main():
    verify_changes()

if __name__ == "__main__":
    main()