#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
茶叶进销存管理系统
使用Excel作为数据存储，替代原有的SQL Server数据库
"""

from tea_inventory_system import TeaInventorySystem

def main():
    print("欢迎使用茶叶进销存管理系统！")
    print("系统正在启动...")
    
    # 创建系统实例
    system = TeaInventorySystem()
    
    # 运行系统
    system.run()

if __name__ == "__main__":
    main()