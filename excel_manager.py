import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
from datetime import datetime
import random
from utils import convert_to_jin


class ExcelManager:
    def __init__(self, filename="tea_inventory.xlsx"):
        self.filename = filename
        self._cache = {}
        self._dirty_flags = {}
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
                "单价", "应收金额", "实收金额", "客户名称", "销售日期", "销售单位", "是否作废"
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

            # 创建客户表
            ws_customer = wb.create_sheet("客户信息")
            ws_customer.append([
                "客户编号", "客户名称", "联系电话", "电子邮箱", "地址",
                "累计消费", "订单数", "最后购买日期", "客户等级", "备注", "创建日期"
            ])

            wb.save(self.filename)
    
    def read_sheet(self, sheet_name):
        """读取指定工作表的数据（带缓存）"""
        if sheet_name in self._cache:
            return self._cache[sheet_name].copy()
        try:
            df = pd.read_excel(self.filename, sheet_name=sheet_name, engine='openpyxl')
            self._cache[sheet_name] = df.copy()
            self._dirty_flags[sheet_name] = False
            return df
        except Exception as e:
            print(f"读取工作表 {sheet_name} 出错: {e}")
            return pd.DataFrame()
    
    def clear_cache(self):
        """清空所有缓存数据"""
        self._cache.clear()
        self._dirty_flags.clear()
    
    def write_sheet(self, sheet_name, data):
        """写入数据到指定工作表（更新缓存）"""
        try:
            wb = load_workbook(self.filename)
            
            # 如果工作表存在，先删除
            if sheet_name in wb.sheetnames:
                wb.remove(wb[sheet_name])
            
            # 创建新的工作表
            ws = wb.create_sheet(sheet_name)
            
            # 写入标题行 - 即使数据为空也要保留列名
            # 确定要写入的列名
            expected_columns = {
                "商品信息": ["商品编号", "茶类", "品种", "公司", "产区", "商品名称", "规格", "成本价", "零售价", "生产日期", "保质期(月)", "当前库存", "品质特征", "年份", "等级", "单位"],
                "销售记录": ["销售编号", "商品编号", "商品名称", "销售数量", "单价", "应收金额", "实收金额", "客户名称", "销售日期", "销售单位", "是否作废"],
                "进货记录": ["进货编号", "商品编号", "商品名称", "进货数量", "进货单价", "供应商", "进货日期", "备注", "进货单位"],
                "供应商": ["供应商编号", "供应商名称", "联系人", "联系电话", "地址", "备注"],
                "客户信息": ["客户编号", "客户名称", "联系电话", "电子邮箱", "地址", "累计消费", "订单数", "最后购买日期", "客户等级", "备注", "创建日期"]
            }
            
            # 如果数据有列名，使用数据的列名；否则使用默认列名
            if not data.empty:
                columns_to_write = data.columns.tolist()
            elif sheet_name in expected_columns:
                columns_to_write = expected_columns[sheet_name]
            else:
                columns_to_write = []
            
            # 写入标题行
            if columns_to_write:
                ws.append(columns_to_write)
            
            # 写入数据行 - 使用批量方式写入
            if not data.empty:
                for _, row in data.iterrows():
                    ws.append(row.tolist())
            
            wb.save(self.filename)
            self._cache[sheet_name] = data.copy()
            self._dirty_flags[sheet_name] = False
        except Exception as e:
            print(f"写入工作表 {sheet_name} 出错: {e}")
    
    def append_to_sheet(self, sheet_name, data_row):
        """向指定工作表追加一行数据（更新缓存）"""
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
            # 清除该工作表的缓存，下次读取时重新加载
            if sheet_name in self._cache:
                del self._cache[sheet_name]
                del self._dirty_flags[sheet_name]
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
            
            # 使用convert_to_jin函数转换
            sold_qty_jin = convert_to_jin(sold_qty, sale_unit)
            
            new_stock = current_stock - sold_qty_jin
            self.update_commodity(sale_data[1], {'当前库存': new_stock})
        
        # 更新客户信息
        customer_name = sale_data[7]  # 客户名称在第8列
        received_amount = sale_data[6]  # 实收金额在第7列
        sale_date = sale_data[8]  # 销售日期在第9列
        
        if customer_name:
            self.update_customer_after_sale(customer_name, received_amount, sale_date)
    
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
            
            # 使用convert_to_jin函数转换
            stock_qty_jin = convert_to_jin(stock_qty, stock_unit)
            
            new_stock = current_stock + stock_qty_jin
            self.update_commodity(stock_data[1], {'当前库存': new_stock})
        
        # 更新供应商信息
        supplier_name = stock_data[5]  # 供应商名称在第6列
        amount = float(stock_data[3]) * float(stock_data[4])  # 数量 * 单价
        stock_date = stock_data[6]  # 进货日期在第7列
        
        if supplier_name:
            self.update_supplier_after_stock(supplier_name, amount, stock_date)
    
    # 供应商相关操作
    def get_all_suppliers(self):
        try:
            print("=== 开始读取供应商数据 ===")
            df = self.read_sheet("供应商")
            print(f"原始数据行数: {len(df)}")
            print(f"原始数据列名: {list(df.columns)}")
            print(f"原始数据是否为空: {df.empty}")
            
            # 检查数据
            if not df.empty:
                # 打印原始数据的前几行
                print("\n原始数据前3行:")
                for i in range(min(3, len(df))):
                    print(f"  行 {i+1}: {list(df.iloc[i])}")
            
            # 数据清理
            if not df.empty:
                # 1. 首先移除所有字段都是 NaN 的行
                df = df.dropna(how='all')
                print(f"\n移除全 NaN 行后，行数: {len(df)}")
                
                if not df.empty:
                    # 2. 只对文本列进行字符串转换和去空白
                    text_columns = ['供应商编号', '供应商名称', '联系人', '联系电话', '地址']
                    for col in text_columns:
                        if col in df.columns:
                            df[col] = df[col].astype(str).str.strip()
                    
                    # 3. 移除空行（检查关键文本字段）
                    if '供应商名称' in df.columns:
                        mask = df['供应商名称'].notna() & (df['供应商名称'] != '') & (df['供应商名称'] != 'nan') & (df['供应商名称'] != 'NaN')
                        df = df[mask]
                    
                    # 4. 重置索引
                    df = df.reset_index(drop=True)
                    print(f"清理后的数据行数: {len(df)}")
                    
                    if not df.empty:
                        print("\n清理后的数据:")
                        for index, row in df.iterrows():
                            print(f"  行 {index+1}: {list(row)}")
            
            print("=== 读取供应商数据完成 ===")
            return df
        except Exception as e:
            print(f"获取供应商数据时出错: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    def add_supplier(self, supplier_data):
        self.append_to_sheet("供应商", supplier_data)

    def update_supplier_after_stock(self, supplier_name, amount, stock_date):
        """进货后更新供应商信息"""
        df = self.read_sheet("供应商")
        if df.empty:
            # 如果供应商表为空，创建新供应商
            self._create_new_supplier(supplier_name, amount, stock_date)
            return

        # 查找供应商
        supplier_row = df[df['供应商名称'] == supplier_name]
        if supplier_row.empty:
            # 创建新供应商
            self._create_new_supplier(supplier_name, amount, stock_date)
        else:
            # 更新现有供应商
            idx = supplier_row.index[0]
            # 获取当前累计交易金额，如果为空则为0
            current_amount = float(df.at[idx, '累计交易金额']) if pd.notna(df.at[idx, '累计交易金额']) else 0.0
            # 更新累计交易金额
            df.at[idx, '累计交易金额'] = current_amount + amount
            # 保存更新
            self.write_sheet("供应商", df)
            print(f"供应商 {supplier_name} 已更新，累计交易金额: {current_amount + amount}")

    def _create_new_supplier(self, supplier_name, amount, stock_date):
        """创建新供应商"""
        # 生成供应商编号
        supplier_id = self.generate_id("SP", "供应商", "供应商编号")
        
        # 创建供应商数据（包含初始累计交易金额）
        supplier_data = [
            supplier_id, supplier_name, "", "", "", amount
        ]
        
        self.append_to_sheet("供应商", supplier_data)
        print(f"新供应商 {supplier_name} 创建成功，供应商编号: {supplier_id}，初始累计交易金额: {amount}")

    # 客户相关操作
    def get_all_customers(self):
        try:
            print("=== 开始读取客户数据 ===")
            df = self.read_sheet("客户信息")
            print(f"原始数据行数: {len(df)}")
            print(f"原始数据列名: {list(df.columns)}")
            print(f"原始数据是否为空: {df.empty}")
            
            # 检查数据
            if not df.empty:
                # 打印原始数据的前几行
                print("\n原始数据前3行:")
                for i in range(min(3, len(df))):
                    print(f"  行 {i+1}: {list(df.iloc[i])}")
            
            # 数据清理
            if not df.empty:
                # 1. 首先移除所有字段都是 NaN 的行
                df = df.dropna(how='all')
                print(f"\n移除全 NaN 行后，行数: {len(df)}")
                
                if not df.empty:
                    # 2. 只对文本列进行字符串转换和去空白
                    text_columns = ['客户编号', '客户名称', '联系人', '联系电话', '地址', '客户等级', '最后购买日期']
                    for col in text_columns:
                        if col in df.columns:
                            df[col] = df[col].astype(str).str.strip()
                    
                    # 3. 移除空行（检查关键文本字段）
                    if '客户名称' in df.columns:
                        mask = df['客户名称'].notna() & (df['客户名称'] != '') & (df['客户名称'] != 'nan') & (df['客户名称'] != 'NaN')
                        df = df[mask]
                    
                    # 4. 重置索引
                    df = df.reset_index(drop=True)
                    print(f"清理后的数据行数: {len(df)}")
                    
                    if not df.empty:
                        print("\n清理后的数据:")
                        for index, row in df.iterrows():
                            print(f"  行 {index+1}: {list(row)}")
            
            print("=== 读取客户数据完成 ===")
            return df
        except Exception as e:
            print(f"获取客户数据时出错: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    def get_customer_by_id(self, customer_id):
        df = self.read_sheet("客户信息")
        if df.empty:
            return None
        result = df[df['客户编号'] == customer_id]
        return result.iloc[0] if not result.empty else None

    def get_customer_by_name(self, name):
        df = self.read_sheet("客户信息")
        if df.empty:
            return None
        result = df[df['客户名称'] == name]
        return result.iloc[0] if not result.empty else None

    def add_customer(self, customer_data):
        self.append_to_sheet("客户信息", customer_data)

    def update_customer(self, customer_id, new_data):
        df = self.read_sheet("客户信息")
        if df.empty:
            return False

        idx = df[df['客户编号'] == customer_id].index
        if len(idx) > 0:
            for col, value in new_data.items():
                df.at[idx[0], col] = value
            self.write_sheet("客户信息", df)
            return True
        return False

    def delete_customer(self, customer_id):
        df = self.read_sheet("客户信息")
        if df.empty:
            return False

        df = df[df['客户编号'] != customer_id]
        self.write_sheet("客户信息", df)
        return True

    def update_customer_after_sale(self, customer_name, amount, sale_date):
        """销售后更新客户信息"""
        df = self.read_sheet("客户信息")
        if df.empty:
            # 如果客户表为空，创建新客户
            self._create_new_customer(customer_name, amount, sale_date)
            return

        # 查找客户
        customer_row = df[df['客户名称'] == customer_name]
        if customer_row.empty:
            # 创建新客户
            self._create_new_customer(customer_name, amount, sale_date)
        else:
            # 更新现有客户
            idx = customer_row.index[0]
            current_purchases = float(df.at[idx, '累计消费']) if pd.notna(df.at[idx, '累计消费']) else 0.0
            current_orders = int(df.at[idx, '订单数']) if pd.notna(df.at[idx, '订单数']) else 0
            
            # 更新客户信息
            new_purchases = current_purchases + amount
            new_orders = current_orders + 1
            
            # 更新客户等级
            if new_purchases >= 5000:
                customer_level = "VIP客户"
            elif new_purchases >= 2000:
                customer_level = "高级客户"
            elif new_purchases >= 1000:
                customer_level = "中级客户"
            else:
                customer_level = "普通客户"
            
            df.at[idx, '累计消费'] = new_purchases
            df.at[idx, '订单数'] = new_orders
            df.at[idx, '最后购买日期'] = sale_date
            df.at[idx, '客户等级'] = customer_level
            
            self.write_sheet("客户信息", df)

    def _create_new_customer(self, customer_name, amount, sale_date):
        """创建新客户"""
        # 生成客户编号
        customer_id = self.generate_id("K", "客户信息", "客户编号")
        
        # 确定客户等级
        if amount >= 5000:
            customer_level = "VIP客户"
        elif amount >= 2000:
            customer_level = "高级客户"
        elif amount >= 1000:
            customer_level = "中级客户"
        else:
            customer_level = "普通客户"
        
        # 创建客户数据
        customer_data = [
            customer_id, customer_name, "", "", "",
            amount, 1, sale_date, customer_level, "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        self.append_to_sheet("客户信息", customer_data)

    # 销售记录查询与修改
    def get_sale_by_id(self, sale_id):
        df = self.read_sheet("销售记录")
        if df.empty:
            return None
        result = df[df['销售编号'] == sale_id]
        return result.iloc[0] if not result.empty else None

    def query_sales(self, start_date=None, end_date=None, customer_name=None,
                    com_id=None, com_name=None):
        """多条件查询销售记录"""
        df = self.read_sheet("销售记录")
        if df.empty:
            return df

        # 过滤掉作废记录
        if '是否作废' in df.columns:
            df = df[df['是否作废'] != True]

        # 按日期范围过滤
        if start_date:
            df = df[df['销售日期'] >= start_date]
        if end_date:
            df = df[df['销售日期'] <= end_date]

        # 按客户过滤
        if customer_name:
            df = df[df['客户名称'] == customer_name]

        # 按商品过滤
        if com_id:
            df = df[df['商品编号'] == com_id]
        if com_name:
            df = df[df['商品名称'] == com_name]

        return df

    def update_sale(self, sale_id, new_data, rollback_stock=False):
        """修改销售记录，可选回滚库存"""
        df = self.read_sheet("销售记录")
        if df.empty:
            return False

        idx = df[df['销售编号'] == sale_id].index
        if len(idx) == 0:
            return False

        old_sale = df.iloc[idx[0]]

        # 如果需要回滚库存
        if rollback_stock:
            # 恢复原库存
            commodity = self.get_commodity_by_id(old_sale['商品编号'])
            if commodity is not None:
                old_qty_jin = convert_to_jin(old_sale['销售数量'], old_sale.get('销售单位', '克'))
                current_stock = float(commodity['当前库存'])
                self.update_commodity(old_sale['商品编号'], {'当前库存': current_stock + old_qty_jin})

            # 如果有新数据，扣减新库存
            if '销售数量' in new_data or '销售单位' in new_data:
                new_qty = new_data.get('销售数量', old_sale['销售数量'])
                new_unit = new_data.get('销售单位', old_sale.get('销售单位', '克'))
                new_qty_jin = convert_to_jin(new_qty, new_unit)
                commodity = self.get_commodity_by_id(old_sale['商品编号'])
                if commodity is not None:
                    current_stock = float(commodity['当前库存'])
                    self.update_commodity(old_sale['商品编号'], {'当前库存': current_stock - new_qty_jin})

        # 更新销售记录
        for col, value in new_data.items():
            df.at[idx[0], col] = value

        self.write_sheet("销售记录", df)
        return True

    def void_sale(self, sale_id):
        """作废销售记录，回滚库存"""
        df = self.read_sheet("销售记录")
        if df.empty:
            return False

        idx = df[df['销售编号'] == sale_id].index
        if len(idx) == 0:
            return False

        sale = df.iloc[idx[0]]

        # 回滚库存
        commodity = self.get_commodity_by_id(sale['商品编号'])
        if commodity is not None:
            qty_jin = convert_to_jin(sale['销售数量'], sale.get('销售单位', '克'))
            current_stock = float(commodity['当前库存'])
            self.update_commodity(sale['商品编号'], {'当前库存': current_stock + qty_jin})

        # 标记为作废
        df.at[idx[0], '是否作废'] = True
        self.write_sheet("销售记录", df)
        return True