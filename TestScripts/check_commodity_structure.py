#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查商品数据结构
"""

import sys
import os
# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from excel_manager import ExcelManager
import pandas as pd

def check_commodity_structure():
    """检查商品数据结构"""
    print("检查商品数据结构")
    print("="*50)
    
    excel_manager = ExcelManager()
    
    # 直接读取商品信息表
    df = excel_manager.get_all_commodities()
    
    print(f"商品数据表总行数: {len(df)}")
    print(f"列名: {list(df.columns)}")
    
    print("\n原始数据表内容:")
    for idx, row in df.iterrows():
        print(f"  行 {idx}: {dict(row)}")
    
    print("\n移除标题行后的数据 (df.iloc[1:]):")
    df_without_header = df.iloc[1:]
    for idx, row in df_without_header.iterrows():
        print(f"  行 {idx} (原索引): 编号={row['商品编号'] if '商品编号' in row.index else 'N/A'}, "
              f"名称={row['商品名称'] if '商品名称' in row.index else 'N/A'}")
    
    print(f"\n移除标题行后剩余行数: {len(df_without_header)}")
    
    # 检查是否有T001商品
    if '商品编号' in df.columns:
        t001_found = df[df['商品编号'] == 'T001']
        print(f"\nT001商品在原始表中: {'是' if not t001_found.empty else '否'}")
        if not t001_found.empty:
            for idx, row in t001_found.iterrows():
                print(f"  T001在原始表的行 {idx}: {dict(row)}")
        
        # 检查移除标题行后是否还有T001
        if not df_without_header.empty and '商品编号' in df_without_header.columns:
            t001_after_remove = df_without_header[df_without_header['商品编号'] == 'T001']
            print(f"T001商品在移除标题行后: {'是' if not t001_after_remove.empty else '否'}")
            if not t001_after_remove.empty:
                for idx, row in t001_after_remove.iterrows():
                    print(f"  T001在移除标题行后的行 {idx}: {dict(row)}")

def analyze_problem():
    """分析问题原因"""
    print(f"\n{'='*50}")
    print("问题分析")
    
    excel_manager = ExcelManager()
    df = excel_manager.get_all_commodities()
    
    print(f"\nDataFrame结构分析:")
    print(f"- 总行数: {len(df)}")
    print(f"- 行索引: {list(df.index)}")
    
    if len(df) > 0:
        print(f"- 第0行 (索引0): {dict(df.iloc[0])}")
    if len(df) > 1:
        print(f"- 第1行 (索引1): {dict(df.iloc[1])}")
    if len(df) > 2:
        print(f"- 第2行 (索引2): {dict(df.iloc[2])}")
    
    print(f"\n问题原因:")
    print(f"- pandas.read_excel()会将Excel的第一行作为列标题")
    print(f"- 所以DataFrame的第0行实际上是Excel的标题行")
    print(f"- DataFrame的第1行开始才是真正的数据行")
    print(f"- 当前代码使用 df.iloc[1:] 跳过第0行，这没问题")
    print(f"- 但可能T001商品就在Excel的第1行（DataFrame的第0行），却被误认为是标题行跳过了")
    
    # 重新读取，但不把第一行作为标题
    print(f"\n重新读取，不使用第一行作为标题:")
    try:
        df_no_header = pd.read_excel(excel_manager.filename, sheet_name="商品信息", 
                                   header=None, engine='openpyxl')
        print(f"不设标题的DataFrame行数: {len(df_no_header)}")
        print(f"不设标题的前3行:")
        for idx in range(min(3, len(df_no_header))):
            print(f"  行 {idx}: {df_no_header.iloc[idx].tolist()}")
    except Exception as e:
        print(f"重新读取失败: {e}")

def main():
    check_commodity_structure()
    analyze_problem()

if __name__ == "__main__":
    main()