#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
茶叶进销存管理系统
使用Excel作为数据存储，替代原有的SQL Server数据库
"""

from tea_inventory_system import TeaInventorySystem
from error_handler import setup_global_exception_handler
from logger import get_logger

_logger = get_logger()


def main():
    setup_global_exception_handler()
    print("欢迎使用茶叶进销存管理系统！")
    print("系统正在启动...")
    
    try:
        system = TeaInventorySystem()
        system.run()
    except KeyboardInterrupt:
        print("\n系统已退出。")
    except Exception as e:
        _logger.exception(f"系统运行异常: {e}")
        print(f"\n系统发生错误: {e}")
        print("详细信息已记录到日志文件。")
        input("按回车键退出...")


if __name__ == "__main__":
    main()