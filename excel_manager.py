import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
from datetime import datetime
import random

class ExcelManager:
    def __init__(self, filename="tea_inventory.xlsx"):
        self.filename = filename
        self.init_excel_file()
    
    def init_excel_file(self):
        """初始化Excel文件，创建必要的工作表"""
        if not os.path.exists(self.filename):
            wb = Workbook()
            
            # 创建商品表
            ws_commodity = wb.active
            ws_commodity.title = "商品信息"
            ws_commodity.append([
                "商品编号", "茶类", "品种", "公司", "产区", "商品名称", 
                "规格", "成本价", "零售价", "生产日期", 
                "保质期(月)", "当前库存", "品质特征", "年份", "等级", "单位"
            ])
            
            # 创建销售记录表
            ws_sell = wb.create_sheet("销售记录")
            ws_sell.append([
                "销售编号", "商品编号", "商品名称", "销售数量", 
                "单价", "应收金额", "实收金额", "客户名称", "销售日期", "销售单位"
            ])
            
            # 创建进货记录表
            ws_stock = wb.create_sheet("进货记录")
            ws_stock.append([
                "进货编号", "商品编号", "商品名称", "进货数量", 
                "进货单价", "供应商", "进货日期", "备注", "进货单位"
            ])
            
            # 创建供应商表
            ws_supplier = wb.create_sheet("供应商")
            ws_supplier.append([
                "供应商编号", "供应商名称", "联系人", "联系电话", "地址", "备注"
            ])
            
            wb.save(self.filename)
    
    def read_sheet(self, sheet_name):
        """读取指定工作表的数据"""
        try:
            df = pd.read_excel(self.filename, sheet_name=sheet_name, engine='openpyxl')
            return df
        except Exception as e:
            print(f"读取工作表 {sheet_name} 出错: {e}")
            return pd.DataFrame()
    
    def write_sheet(self, sheet_name, data):
        """写入数据到指定工作表"""
        try:
            wb = load_workbook(self.filename)
            
            # 如果工作表存在，先删除
            if sheet_name in wb.sheetnames:
                wb.remove(wb[sheet_name])
            
            # 创建新的工作表
            ws = wb.create_sheet(sheet_name)
            
            # 写入标题行
            if not data.empty:
                ws.append(data.columns.tolist())
                # 写入数据行
                for _, row in data.iterrows():
                    ws.append(row.tolist())
            
            wb.save(self.filename)
        except Exception as e:
            print(f"写入工作表 {sheet_name} 出错: {e}")
    
    def append_to_sheet(self, sheet_name, data_row):
        """向指定工作表追加一行数据"""
        try:
            wb = load_workbook(self.filename)
            ws = wb[sheet_name]
            
            # 如果是DataFrame，则逐行添加
            if isinstance(data_row, pd.DataFrame):
                for _, row in data_row.iterrows():
                    ws.append(row.tolist())
            else:
                # 如果是列表或元组
                ws.append(data_row)
            
            wb.save(self.filename)
        except Exception as e:
            print(f"追加数据到工作表 {sheet_name} 出错: {e}")
    
    def generate_id(self, prefix, sheet_name=None, id_column=None):
        """生成唯一ID"""
        # 如果是商品编号（前缀为"C"），则使用递增编号
        if prefix == "C" and sheet_name == "商品信息" and id_column == "商品编号":
            df = self.read_sheet(sheet_name)
            if df.empty or id_column not in df.columns:
                # 如果工作表为空或列不存在，返回T001
                return "T001"
            
            # 提取现有商品编号中的数字部分
            existing_ids = df[id_column].astype(str).tolist()
            existing_numbers = []
            for id_val in existing_ids:
                if isinstance(id_val, str) and id_val.startswith("T"):
                    num_part = id_val[1:]  # 去掉"T"前缀
                    if num_part.isdigit():
                        existing_numbers.append(int(num_part))
            
            # 找到最大编号，返回下一个
            if existing_numbers:
                next_num = max(existing_numbers) + 1
            else:
                next_num = 1
            
            return f"T{next_num:03d}"
        
        # 如果提供了工作表名和ID列，则确保生成的ID不重复
        if sheet_name and id_column:
            max_attempts = 100  # 最大尝试次数，避免无限循环
            attempt = 0
            while attempt < max_attempts:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                random_part = f"{random.randint(1000, 9999)}"
                new_id = f"{prefix}{timestamp}{random_part}"
                
                # 检查ID是否已存在
                df = self.read_sheet(sheet_name)
                if df.empty or id_column not in df.columns:
                    return new_id  # 如果工作表为空或列不存在，直接返回
                
                existing_ids = df[id_column].astype(str).tolist()
                if new_id not in existing_ids:
                    return new_id  # 找到不重复的ID
                
                attempt += 1
            
            raise Exception(f"无法生成唯一ID: {prefix}")  # 如果尝试失败，抛出异常
        else:
            # 如果没有提供工作表名和ID列，则使用时间戳和随机数
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            random_part = f"{random.randint(1000, 9999)}"
            return f"{prefix}{timestamp}{random_part}"
    
    # 商品相关操作
    def get_all_commodities(self):
        return self.read_sheet("商品信息")
    
    def get_commodity_by_id(self, com_id):
        df = self.read_sheet("商品信息")
        if df.empty:
            return None
        result = df[df['商品编号'] == com_id]
        return result.iloc[0] if not result.empty else None
    
    def add_commodity(self, commodity_data):
        self.append_to_sheet("商品信息", commodity_data)
    
    def update_commodity(self, com_id, new_data):
        df = self.read_sheet("商品信息")
        if df.empty:
            return False
        
        idx = df[df['商品编号'] == com_id].index
        if len(idx) > 0:
            for col, value in new_data.items():
                df.at[idx[0], col] = value
            self.write_sheet("商品信息", df)
            return True
        return False
    
    def delete_commodity(self, com_id):
        df = self.read_sheet("商品信息")
        if df.empty:
            return False
        
        df = df[df['商品编号'] != com_id]
        self.write_sheet("商品信息", df)
        return True
    
    # 销售相关操作
    def get_all_sales(self):
        return self.read_sheet("销售记录")
    
    def add_sale(self, sale_data):
        self.append_to_sheet("销售记录", sale_data)
        
        # 更新库存
        commodity = self.get_commodity_by_id(sale_data[1])  # 商品编号在第二列
        if commodity is not None:
            current_stock = float(commodity['当前库存'])
            sold_qty = float(sale_data[3])  # 销售数量在第四列
            sale_unit = sale_data[9] if len(sale_data) > 9 else '克'  # 销售单位在第10列
            
            # 根据销售单位转换销售数量到斤
            if sale_unit == '克':
                sold_qty_jin = sold_qty / 500  # 克转斤
            else:  # 默认是斤
                sold_qty_jin = sold_qty
            
            new_stock = current_stock - sold_qty_jin
            self.update_commodity(sale_data[1], {'当前库存': new_stock})
    
    # 进货相关操作
    def get_all_stocks(self):
        return self.read_sheet("进货记录")
    
    def add_stock(self, stock_data):
        self.append_to_sheet("进货记录", stock_data)
        
        # 更新库存
        commodity = self.get_commodity_by_id(stock_data[1])  # 商品编号在第二列
        if commodity is not None:
            current_stock = float(commodity['当前库存'])
            stock_qty = float(stock_data[3])  # 进货数量在第四列
            stock_unit = stock_data[8] if len(stock_data) > 8 else '斤'  # 进货单位在第9列
            
            # 根据进货单位转换进货数量到斤
            if stock_unit == '克':
                stock_qty_jin = stock_qty / 500  # 克转斤
            else:  # 默认是斤
                stock_qty_jin = stock_qty
            
            new_stock = current_stock + stock_qty_jin
            self.update_commodity(stock_data[1], {'当前库存': new_stock})
    
    # 供应商相关操作
    def get_all_suppliers(self):
        return self.read_sheet("供应商")
    
    def add_supplier(self, supplier_data):
        self.append_to_sheet("供应商", supplier_data)