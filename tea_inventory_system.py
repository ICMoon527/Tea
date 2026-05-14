from excel_manager import ExcelManager
from tea_commodity import TeaCommodity
from sale_record import SaleRecord
from stock_record import StockRecord
from supplier import Supplier
from customer import Customer
from data_visualization import DataVisualization
from shopping_cart import ShoppingCart
from utils import convert_to_jin
from datetime import datetime, timedelta
import pandas as pd
from prettytable import PrettyTable
import textwrap


class TeaInventorySystem:
    def __init__(self):
        self.excel_manager = ExcelManager()
        self.data_viz = DataVisualization(self.excel_manager)
        self.shopping_cart = ShoppingCart(self.excel_manager)
    
    # 商品管理功能
    def add_commodity(self):
        """添加新商品"""
        print("=== 添加茶叶商品 ===")
        
        com_id_input = input("请输入商品编号(留空则自动生成): ").strip()
        if com_id_input:
            com_id = com_id_input
            existing = self.excel_manager.get_commodity_by_id(com_id)
            if existing is not None:
                print("错误：该商品编号已存在！")
                return
        else:
            # 自动生成商品编号
            com_id = self.excel_manager.generate_id("C", "商品信息", "商品编号")
            print(f"自动生成的商品编号: {com_id}")
        
        tea_category = input("请输入茶类(红茶/绿茶/乌龙茶/白茶/黄茶/黑茶/普洱茶等): ").strip()
        variety = input("请输入品种(如：正山小种/铁观音/大红袍等): ").strip()
        company = input("请输入公司/品牌: ").strip()
        origin = input("请输入产区: ").strip()
        name = input("请输入商品名称: ").strip()
        specification = input("请输入规格(如：斤、盒、包等): ").strip()
        
        try:
            cost_price = float(input("请输入成本价(每斤): "))
            retail_price = float(input("请输入零售价(每斤): "))
            current_stock = float(input("请输入初始库存(斤): "))
        except ValueError:
            print("错误：价格和库存必须是数字！")
            return
        
        production_date = input("请输入生产日期(格式：YYYY-MM-DD): ").strip()
        shelf_life = int(input("请输入保质期(月): "))
        quality_features = input("请输入品质特征: ").strip()
        year = input("请输入年份: ").strip()
        grade = input("请输入等级(特级/一级/二级等): ").strip()
        unit = input("请输入计量单位(斤/克，默认为斤): ").strip() or "斤"
        
        commodity = TeaCommodity(
            com_id=com_id, tea_category=tea_category, variety=variety,
            company=company, origin=origin, name=name,
            specification=specification, cost_price=cost_price,
            retail_price=retail_price, production_date=production_date,
            shelf_life=shelf_life, current_stock=current_stock,
            quality_features=quality_features, year=year, grade=grade, unit=unit
        )
        
        self.excel_manager.add_commodity(commodity.to_list())
        print("商品添加成功！")
    
    def query_all_commodities(self):
        """查询所有商品"""
        df = self.excel_manager.get_all_commodities()
        if df.empty or len(df) <= 0:  # pandas已经处理了标题行
            print("暂无商品信息")
            return
        
        # 不需要移除标题行，因为pandas.read_excel已经将Excel第一行作为列标题
        # 所有数据行都在DataFrame中，无需进一步切片
        df_data = df
        
        # 重新检查是否还有数据
        if df_data.empty or len(df_data) == 0:
            print("暂无商品信息")
            return
            
        table = PrettyTable()
        table.field_names = df_data.columns.tolist()
        
        for _, row in df_data.iterrows():
            # 对品质特征进行换行处理
            if '品质特征' in row.index:
                description = str(row['品质特征']) if pd.notna(row['品质特征']) else ''
                wrapped_desc = '\n'.join(textwrap.wrap(description, width=30)) if description else ''
                row['品质特征'] = wrapped_desc
            
            table.add_row(row.values)
        
        print(table)
        print(f"以上共 {len(df_data)} 条记录。")
    
    def query_commodity_by_id(self):
        """按编号查询商品"""
        com_id = input("请输入商品编号: ").strip()
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        
        if commodity is None:
            print("未找到该商品")
            return
        
        table = PrettyTable(['属性', '值'])
        for key, value in commodity.items():
            # 对品质特征进行换行处理
            if key == '品质特征' and pd.notna(value):
                wrapped_desc = '\n'.join(textwrap.wrap(str(value), width=30))
                table.add_row([key, wrapped_desc])
            else:
                table.add_row([key, value])
        
        print(table)
    
    def update_commodity(self):
        """修改商品信息"""
        com_id = input("请输入要修改的商品编号: ").strip()
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        
        if commodity is None:
            print("未找到该商品")
            return
        
        print("当前商品信息：")
        self._print_single_commodity(commodity)
        
        print("\n请输入新的信息（直接回车保持原值）：")
        
        updates = {}
        
        new_tea_category = input(f"茶类 (当前: {commodity['茶类']}): ").strip()
        if new_tea_category: updates['茶类'] = new_tea_category
        
        new_variety = input(f"品种 (当前: {commodity['品种']}): ").strip()
        if new_variety: updates['品种'] = new_variety
        
        new_company = input(f"公司 (当前: {commodity['公司']}): ").strip()
        if new_company: updates['公司'] = new_company
        
        new_origin = input(f"产区 (当前: {commodity['产区']}): ").strip()
        if new_origin: updates['产区'] = new_origin
        
        new_name = input(f"商品名称 (当前: {commodity['商品名称']}): ").strip()
        if new_name: updates['商品名称'] = new_name
        
        new_specification = input(f"规格 (当前: {commodity['规格']}): ").strip()
        if new_specification: updates['规格'] = new_specification
        
        new_cost_price = input(f"成本价 (当前: {commodity['成本价']}): ").strip()
        if new_cost_price: 
            try:
                updates['成本价'] = float(new_cost_price)
            except ValueError:
                print("成本价必须是数字！")
                return
        
        new_retail_price = input(f"零售价 (当前: {commodity['零售价']}): ").strip()
        if new_retail_price: 
            try:
                updates['零售价'] = float(new_retail_price)
            except ValueError:
                print("零售价必须是数字！")
                return
        
        new_production_date = input(f"生产日期 (当前: {commodity['生产日期']}): ").strip()
        if new_production_date: updates['生产日期'] = new_production_date
        
        new_shelf_life = input(f"保质期(月) (当前: {commodity['保质期(月)']}): ").strip()
        if new_shelf_life: 
            try:
                updates['保质期(月)'] = int(new_shelf_life)
            except ValueError:
                print("保质期必须是整数！")
                return
        
        new_current_stock = input(f"当前库存 (当前: {commodity['当前库存']}): ").strip()
        if new_current_stock: 
            try:
                updates['当前库存'] = float(new_current_stock)
            except ValueError:
                print("库存必须是数字！")
                return
        
        new_quality_features = input(f"品质特征 (当前: {commodity['品质特征']}): ").strip()
        if new_quality_features: updates['品质特征'] = new_quality_features
        
        new_year = input(f"年份 (当前: {commodity['年份']}): ").strip()
        if new_year: updates['年份'] = new_year
        
        new_grade = input(f"等级 (当前: {commodity['等级']}): ").strip()
        if new_grade: updates['等级'] = new_grade
        
        if updates:
            success = self.excel_manager.update_commodity(com_id, updates)
            if success.get('success'):
                print("商品信息更新成功！")
            else:
                print("更新失败！")
        else:
            print("未做任何修改。")
    
    def delete_commodity(self):
        """删除商品"""
        com_id = input("请输入要删除的商品编号: ").strip()
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        
        if commodity is None:
            print("未找到该商品")
            return
        
        confirm = input(f"确定要删除商品 '{commodity['商品名称']}' 吗？(y/N): ").strip().lower()
        if confirm == 'y':
            success = self.excel_manager.delete_commodity(com_id)
            if success.get('success'):
                print("商品删除成功！")
            else:
                print("删除失败！")
        else:
            print("操作已取消。")
    
    def _print_single_commodity(self, commodity):
        """打印单个商品信息"""
        table = PrettyTable(['属性', '值'])
        for key, value in commodity.items():
            # 对品质特征进行换行处理
            if key == '品质特征' and pd.notna(value):
                wrapped_desc = '\n'.join(textwrap.wrap(str(value), width=30))
                table.add_row([key, wrapped_desc])
            else:
                table.add_row([key, value])
        print(table)
    
    # 销售功能
    def add_to_cart(self):
        """添加商品到购物车"""
        # 获取所有有库存的商品，显示可销售的商品列表
        all_commodities = self.excel_manager.get_all_commodities()
        if not all_commodities.empty:
            # 筛选出有库存的商品
            available_commodities = all_commodities[all_commodities['当前库存'].astype(float) > 0]
            if not available_commodities.empty:
                print("\n可销售的商品列表 (仅显示有库存的商品):")
                for idx, (_, row) in enumerate(available_commodities.iterrows(), 1):
                    stock_jin = float(row['当前库存'])
                    stock_ke = stock_jin * 500
                    print(f"{idx}. {row['商品名称']} (编号: {row['商品编号']}) - 库存: {stock_jin}斤 ({stock_ke}克)")
        
        com_id_input = input("\n请输入商品编号(留空则从可销售商品列表中选择序号): ").strip()
        
        if not com_id_input:
            # 如果用户没有输入编号，则让他们从列表中选择
            if 'available_commodities' in locals() and not available_commodities.empty:
                try:
                    choice_num = int(input("请输入要购买的商品序号: "))
                    if 1 <= choice_num <= len(available_commodities):
                        selected_commodity = available_commodities.iloc[choice_num-1]
                        com_id = selected_commodity['商品编号']
                        commodity = selected_commodity  # 直接使用选中的商品数据
                        print(f"选择了商品: {commodity['商品名称']} (编号: {com_id})")
                    else:
                        print("无效的选择")
                        return
                except ValueError:
                    print("输入的不是有效数字")
                    return
            else:
                print("没有可销售的商品（库存不足）")
                return
        else:
            com_id = com_id_input
            commodity = self.excel_manager.get_commodity_by_id(com_id)
            
            if commodity is None:
                print("商品不存在")
                return
        
        try:
            available_stock_jin = float(commodity['当前库存'])  # 库存以斤为单位
            available_stock_ke = available_stock_jin * 500  # 转换为克
            print(f"商品名称: {commodity['商品名称']}, 可用库存: {available_stock_jin}斤 ({available_stock_ke}克)")
            
            unit_choice = input("请选择购买单位 (1-斤, 2-克，默认为克): ").strip()
            if unit_choice == '1':
                unit = '斤'
                quantity = float(input("请输入购买数量(斤): "))
                # 转换为克进行库存检查
                quantity_in_ke = quantity * 500
            else:
                unit = '克'
                quantity = float(input("请输入购买数量(克): "))
                # 转换为斤进行库存检查
                quantity_in_ke = quantity
                quantity_in_jin = quantity / 500
            
            if quantity <= 0:
                print("购买数量必须大于0")
                return
                
            if quantity_in_ke > available_stock_ke:
                print(f"库存不足！当前可用库存: {available_stock_jin}斤 ({available_stock_ke}克)")
                return
        except ValueError:
            print("输入的数量格式不正确")
            return
        
        # 检查购物车是否已有该商品
        for item in self.shopping_cart:
            if item['商品编号'] == com_id:
                print("该商品已在购物车中，正在更新数量...")
                item['购买数量'] = quantity
                item['购买单位'] = unit
                # 根据单位计算价格（零售价是按斤计算的）
                if unit == '斤':
                    item['小计'] = quantity * float(commodity['零售价'])
                else:  # 克
                    item['小计'] = (quantity / 500) * float(commodity['零售价'])
                print("购物车已更新")
                return
        
        # 添加新商品到购物车
        cart_item = {
            '商品编号': com_id,
            '商品名称': commodity['商品名称'],
            '单价(每斤)': float(commodity['零售价']),
            '购买数量': quantity,
            '购买单位': unit,
            '小计': (quantity / 500) * float(commodity['零售价']) if unit == '克' else quantity * float(commodity['零售价'])
        }
        
        self.shopping_cart.append(cart_item)
        print("已添加到购物车")
    
    def view_cart(self):
        """查看购物车"""
        if self.shopping_cart.is_empty():
            print("购物车为空")
            return
        
        table = PrettyTable(['商品编号', '商品名称', '单价(每斤)', '数量', '单位', '小计'])
        
        for item in self.shopping_cart.get_items():
            table.add_row([
                item['商品编号'],
                item['商品名称'],
                item['单价(每斤)'],
                item['购买数量'],
                item['购买单位'],
                item['小计']
            ])
        
        print(table)
        print(f"总计: {self.shopping_cart.get_total_amount():.2f} 元")
    
    def clear_cart(self):
        """清空购物车"""
        if self.shopping_cart.is_empty():
            print("购物车已经为空")
            return
        
        confirm = input("确定要清空购物车吗？(y/N): ").strip().lower()
        if confirm == 'y':
            self.shopping_cart.clear()
            print("购物车已清空")
        else:
            print("操作已取消")
    
    def checkout(self):
        """结账"""
        if self.shopping_cart.is_empty():
            print("购物车为空，无法结账")
            return
        
        total_amount = self.shopping_cart.get_total_amount()
        print(f"应付总额: {total_amount:.2f} 元")
        
        customer_name = input("请输入客户名称: ").strip()
        
        try:
            received_amount = float(input("请输入实收金额: "))
            if received_amount < 0:
                print("实收金额不能为负数")
                return
        except ValueError:
            print("实收金额格式不正确")
            return
        
        if received_amount < total_amount:
            print(f"实收金额 {received_amount:.2f} 元低于应收金额 {total_amount:.2f} 元")
            confirm = input("是否继续销售？(y/N): ").strip().lower()
            if confirm != 'y' and confirm != 'yes':
                print("销售已取消")
                return
            else:
                print(f"销售继续，折扣金额: {total_amount - received_amount:.2f} 元")
        
        # 生成销售记录并保存
        # 无论实收金额是高还是低，都按比例分配给每个商品
        discount_ratio = received_amount / total_amount if total_amount > 0 else 1.0
            
        for item in self.shopping_cart:
            sale_id = self.excel_manager.generate_id("S", "销售记录", "销售编号")
            # 如果销售单位是克，需要转换为斤来更新库存
            quantity_in_jin = item['购买数量'] / 500 if item['购买单位'] == '克' else item['购买数量']
            
            # 按折扣比例计算实际收到的金额
            item_received_amount = item['小计'] * discount_ratio
            
            sale_record = SaleRecord(
                sale_id=sale_id,
                com_id=item['商品编号'],
                com_name=item['商品名称'],
                quantity=item['购买数量'],
                unit_price=item['单价(每斤)'],
                total_amount=item['小计'],
                received_amount=item_received_amount,
                customer_name=customer_name,
                sale_unit=item['购买单位']
            )
            self.excel_manager.add_sale(sale_record.to_list())
        
        if received_amount < total_amount:
            print(f"结账成功！折扣金额: {total_amount - received_amount:.2f} 元")
        elif received_amount > total_amount:
            print(f"结账成功！溢价金额: {received_amount - total_amount:.2f} 元")
        else:
            print("结账成功！")
        print("销售记录已保存")
        
        # 清空购物车
        self.shopping_cart.clear()
    
    # 进货功能
    def stock_in(self):
        """进货入库"""
        print("=== 商品进货 ===")
        
        # 获取所有进货记录，展示历史品种列表
        df_stocks = self.excel_manager.get_all_stocks()
        if not df_stocks.empty and len(df_stocks) > 0:  # 修复：不再假设需要跳过标题行
            if not df_stocks.empty:
                print("\n历史进货品种列表:")
                # 显示所有进货记录，不进行去重，以便用户能看到每次进货的详细信息
                for idx, (original_idx, row) in enumerate(df_stocks.iterrows(), 1):
                    print(f"{idx}. ", end="")
                    # 遍历当前行的所有字段，显示非空值
                    fields = []
                    for col in row.index:
                        if pd.notna(row[col]) and col != '序号':  # 排除序号列，显示其他所有列
                            fields.append(f"{col}:{row[col]}")
                    print(" | ".join(fields))
        
        com_id_input = input("\n请输入商品编号(留空则手动选择历史品种编号): ").strip()
        if not com_id_input:
            # 让用户从历史品种中选择
            if not df_stocks.empty:
                try:
                    choice_num = int(input("请输入要进货的历史品种编号 (输入序号): "))
                    if 1 <= choice_num <= len(df_stocks):
                        selected_product = df_stocks.iloc[choice_num-1]
                        com_id = selected_product['商品编号']
                        print(f"选择了商品: {selected_product['商品名称']} (编号: {com_id})")
                    else:
                        print("无效的选择")
                        return
                except ValueError:
                    print("输入的不是有效数字")
                    return
            else:
                print("没有历史进货记录，请手动输入商品编号")
                com_id = input("请输入商品编号: ").strip()
        else:
            com_id = com_id_input
            
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        
        if commodity is None:
            print("商品不存在，请先添加商品")
            add_new = input("是否添加新商品？(y/N): ").strip().lower()
            if add_new == 'y':
                self.add_commodity()
                return
            else:
                return
        
        try:
            unit_price = float(input("请输入进货单价(每斤): "))
            quantity = float(input("请输入进货数量: "))
            unit = input("请输入进货单位(斤/克，默认为斤): ").strip() or "斤"
        except ValueError:
            print("数量和单价必须是数字")
            return
        
        supplier = input("请输入供应商: ").strip()
        stock_date = input("请输入进货日期(格式：YYYY-MM-DD，直接回车使用今天): ").strip()
        if not stock_date:
            stock_date = datetime.now().strftime("%Y-%m-%d")
        
        remarks = input("请输入备注: ").strip()
        
        # 自动生成进货编号
        stock_id = self.excel_manager.generate_id("I", "进货记录", "进货编号")
        stock_record = StockRecord(
            stock_id=stock_id,
            com_id=com_id,
            com_name=commodity['商品名称'],
            quantity=quantity,
            unit_price=unit_price,
            supplier=supplier,
            stock_date=stock_date,
            remarks=remarks,
            stock_unit=unit
        )
        
        self.excel_manager.add_stock(stock_record.to_list())
        print(f"进货记录已保存，进货编号: {stock_id}")
    
    # 供应商管理
    def manage_suppliers(self):
        """管理供应商"""
        while True:
            print("\n=== 供应商管理 ===")
            print("1. 查看所有供应商")
            print("2. 添加供应商")
            print("3. 修改供应商")
            print("4. 删除供应商")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.view_all_suppliers()
            elif choice == '2':
                self.add_supplier()
            elif choice == '3':
                self.update_supplier()
            elif choice == '4':
                self.delete_supplier()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def view_all_suppliers(self):
        """查看所有供应商"""
        df = self.excel_manager.get_all_suppliers()
        if df.empty:
            print("暂无供应商信息")
            return
            
        table = PrettyTable()
        table.field_names = df.columns.tolist()
        
        for _, row in df.iterrows():
            table.add_row(row.values)
        
        print(table)
        print(f"以上共 {len(df)} 条记录。")
    
    def add_supplier(self):
        """添加供应商"""
        print("=== 添加供应商 ===")
        
        supplier_id_input = input("请输入供应商编号(留空则自动生成): ").strip()
        if supplier_id_input:
            supplier_id = supplier_id_input
            df = self.excel_manager.get_all_suppliers()
            if not df.empty:
                existing = df[df['供应商编号'] == supplier_id]
                if not existing.empty:
                    print("错误：该供应商编号已存在！")
                    return
        else:
            # 自动生成供应商编号
            supplier_id = self.excel_manager.generate_id("SP", "供应商", "供应商编号")
            print(f"自动生成的供应商编号: {supplier_id}")
        
        name = input("请输入供应商名称: ").strip()
        contact_person = input("请输入联系人: ").strip()
        phone = input("请输入联系电话: ").strip()
        address = input("请输入地址: ").strip()
        remarks = input("请输入备注: ").strip()
        
        supplier = Supplier(
            supplier_id=supplier_id,
            name=name,
            contact_person=contact_person,
            phone=phone,
            address=address,
            remarks=remarks
        )
        
        self.excel_manager.add_supplier(supplier.to_list())
        print("供应商添加成功！")
    
    def update_supplier(self):
        """修改供应商"""
        self.view_all_suppliers()
        supplier_id = input("请输入要修改的供应商编号: ").strip()
        
        df = self.excel_manager.get_all_suppliers()
        if df.empty:
            print("暂无供应商信息")
            return
        
        supplier_idx = df[df['供应商编号'] == supplier_id].index
        
        if len(supplier_idx) == 0:
            print("未找到该供应商")
            return
        
        print("当前供应商信息：")
        supplier_row = df.loc[supplier_idx[0]]
        table = PrettyTable(['属性', '值'])
        for key, value in supplier_row.items():
            table.add_row([key, value])
        print(table)
        
        print("\n请输入新的信息（直接回车保持原值）：")
        updates = {}
        
        new_name = input(f"供应商名称 (当前: {supplier_row['供应商名称']}): ").strip()
        if new_name: updates['供应商名称'] = new_name
        
        new_contact = input(f"联系人 (当前: {supplier_row['联系人']}): ").strip()
        if new_contact: updates['联系人'] = new_contact
        
        new_phone = input(f"联系电话 (当前: {supplier_row['联系电话']}): ").strip()
        if new_phone: updates['联系电话'] = new_phone
        
        new_address = input(f"地址 (当前: {supplier_row['地址']}): ").strip()
        if new_address: updates['地址'] = new_address
        
        new_remarks = input(f"备注 (当前: {supplier_row['备注']}): ").strip()
        if new_remarks: updates['备注'] = new_remarks
        
        if updates:
            # 更新DataFrame
            for col, value in updates.items():
                df.at[supplier_idx[0], col] = value
            
            # 重写整个供应商表
            self.excel_manager.write_sheet("供应商", df)
            print("供应商信息更新成功！")
        else:
            print("未做任何修改。")
    
    def delete_supplier(self):
        """删除供应商"""
        self.view_all_suppliers()
        supplier_id = input("请输入要删除的供应商编号: ").strip()
        
        df = self.excel_manager.get_all_suppliers()
        if df.empty:
            print("暂无供应商信息")
            return
        
        supplier_idx = df[df['供应商编号'] == supplier_id].index
        
        if len(supplier_idx) == 0:
            print("未找到该供应商")
            return
        
        supplier_row = df.loc[supplier_idx[0]]
        confirm = input(f"确定要删除供应商 '{supplier_row['供应商名称']}' 吗？(y/N): ").strip().lower()
        if confirm == 'y':
            df = df.drop(supplier_idx)
            self.excel_manager.write_sheet("供应商", df)
            print("供应商删除成功！")
        else:
            print("操作已取消。")
    
    # 统计分析功能
    def sales_statistics(self):
        """销售统计"""
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty or len(df) <= 0:  # 修改条件，不再需要判断<=1
            print("暂无销售记录")
            return
        
        # 不再移除第一行，因为pandas已经正确处理了列标题
        if df.empty:
            print("暂无销售记录")
            return
        
        # 获取商品信息用于成本计算
        commodity_df = self.excel_manager.get_all_commodities()
        if commodity_df.empty:
            print("暂无商品信息，无法进行详细统计")
            return
        
        commodity_df['成本价'] = pd.to_numeric(commodity_df['成本价'], errors='coerce')
        
        # 将销售记录与商品信息合并
        merged_df = pd.merge(df, commodity_df[['商品编号', '茶类', '品种', '成本价']], 
                           on='商品编号', how='left')
        
        # 计算统计信息
        total_sales_count = len(df)
        total_income = df['实收金额'].sum() if '实收金额' in df.columns else 0
        
        # 计算总销售数量（需要考虑销售单位转换）- 向量化操作
        units = merged_df.get('销售单位', pd.Series(['斤'] * len(merged_df), index=merged_df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        merged_df['销售数量(斤)'] = merged_df['销售数量'] * unit_multiplier
        total_quantity = merged_df['销售数量(斤)'].sum()
        
        # 计算总成本和利润，需要考虑销售单位 - 向量化操作
        merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
        total_cost = merged_df['销售成本'].sum()
        total_profit = total_income - total_cost
        profit_margin = (total_profit / total_income * 100) if total_income > 0 else 0
        
        print("\n=== 销售统计 ===")
        print(f"总销售笔数: {total_sales_count}")
        print(f"总销售额: {total_income:.2f} 元")
        print(f"总销售成本: {total_cost:.2f} 元")
        print(f"总利润: {total_profit:.2f} 元")
        print(f"利润率: {profit_margin:.2f}%")
        print(f"总销售数量: {total_quantity:.3f} 斤")
        
        # 提供统计维度选择
        while True:
            print("\n请选择统计维度:")
            print("1. 按一级茶类统计")
            print("2. 按二级茶类（品种）统计")
            print("3. 按商品统计")
            print("4. 按时间统计（日/周/月）")
            print("0. 返回上级菜单")
            
            choice = input("请选择: ").strip()
            
            if choice == '1':
                # 按一级茶类统计 - 向量化操作
                if '茶类' in merged_df.columns:
                    tea_stats = merged_df.groupby('茶类').agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum'
                    }).round(2)
                    tea_stats['利润'] = tea_stats['实收金额'] - tea_stats['销售成本']
                    tea_stats['利润率(%)'] = (tea_stats['利润'] / tea_stats['实收金额'] * 100).round(2)
                    
                    print("\n按一级茶类统计:")
                    tea_table = PrettyTable(['茶类', '销售数量(斤)', '销售额', '销售成本', '利润', '利润率(%)'])
                    for tea_type, row in tea_stats.iterrows():
                        tea_table.add_row([
                            tea_type, 
                            row['销售数量(斤)'], 
                            row['实收金额'], 
                            row['销售成本'],
                            row['利润'],
                            row['利润率(%)']
                        ])
                    print(tea_table)
                else:
                    print("暂无茶类信息")
                    
            elif choice == '2':
                # 按二级茶类（品种）统计 - 向量化操作
                if '品种' in merged_df.columns:
                    variety_stats = merged_df.groupby('品种').agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum'
                    }).round(2)
                    variety_stats['利润'] = variety_stats['实收金额'] - variety_stats['销售成本']
                    variety_stats['利润率(%)'] = (variety_stats['利润'] / variety_stats['实收金额'] * 100).round(2)
                    
                    print("\n按品种统计:")
                    variety_table = PrettyTable(['品种', '销售数量(斤)', '销售额', '销售成本', '利润', '利润率(%)'])
                    for variety, row in variety_stats.iterrows():
                        variety_table.add_row([
                            variety, 
                            row['销售数量(斤)'], 
                            row['实收金额'], 
                            row['销售成本'],
                            row['利润'],
                            row['利润率(%)']
                        ])
                    print(variety_table)
                else:
                    print("暂无品种信息")
                    
            elif choice == '3':
                # 按商品统计 - 向量化操作
                if '商品名称' in merged_df.columns:
                    product_stats = merged_df.groupby(['商品编号', '商品名称']).agg({
                        '销售数量(斤)': 'sum',
                        '实收金额': 'sum',
                        '销售成本': 'sum'
                    }).round(2)
                    product_stats['利润'] = product_stats['实收金额'] - product_stats['销售成本']
                    product_stats['利润率(%)'] = (product_stats['利润'] / product_stats['实收金额'] * 100).round(2)
                    
                    print("\n按商品统计:")
                    product_table = PrettyTable(['商品编号', '商品名称', '销售数量(斤)', '销售额', '销售成本', '利润', '利润率(%)'])
                    for (com_id, com_name), row in product_stats.iterrows():
                        product_table.add_row([
                            com_id,
                            com_name,
                            row['销售数量(斤)'], 
                            row['实收金额'], 
                            row['销售成本'],
                            row['利润'],
                            row['利润率(%)']
                        ])
                    print(product_table)
                else:
                    print("暂无商品名称信息")
                    
            elif choice == '4':
                # 按时间统计 - 向量化操作
                if '销售日期' in merged_df.columns:
                    # 将销售日期转换为datetime类型
                    merged_df['销售日期'] = pd.to_datetime(merged_df['销售日期'])
                    
                    print("\n请选择时间维度:")
                    print("1. 按日统计")
                    print("2. 按周统计") 
                    print("3. 按月统计")
                    time_choice = input("请选择: ").strip()
                    
                    if time_choice == '1':
                        time_group = merged_df.groupby(merged_df['销售日期'].dt.date).agg({
                            '销售数量(斤)': 'sum',
                            '实收金额': 'sum',
                            '销售成本': 'sum'
                        })
                    elif time_choice == '2':
                        time_group = merged_df.groupby(merged_df['销售日期'].dt.to_period('W')).agg({
                            '销售数量(斤)': 'sum',
                            '实收金额': 'sum',
                            '销售成本': 'sum'
                        })
                    elif time_choice == '3':
                        time_group = merged_df.groupby(merged_df['销售日期'].dt.to_period('M')).agg({
                            '销售数量(斤)': 'sum',
                            '实收金额': 'sum',
                            '销售成本': 'sum'
                        })
                    else:
                        print("无效选择")
                        continue
                    
                    time_group['利润'] = time_group['实收金额'] - time_group['销售成本']
                    time_group['利润率(%)'] = (time_group['利润'] / time_group['实收金额'] * 100).round(2)
                    
                    time_label = "日" if time_choice == '1' else ("周" if time_choice == '2' else "月")
                    print(f"\n按{time_label}统计:")
                    time_table = PrettyTable([f'{time_label}期', '销售数量(斤)', '销售额', '销售成本', '利润', '利润率(%)'])
                    for period, row in time_group.iterrows():
                        time_table.add_row([
                            str(period), 
                            row['销售数量(斤)'], 
                            row['实收金额'], 
                            row['销售成本'],
                            row['利润'],
                            row['利润率(%)']
                        ])
                    print(time_table)
                else:
                    print("暂无销售日期信息")
                    
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    

    
    def top_selling_products(self):
        """热销商品排行"""
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty or len(df) <= 0:  # 修改条件
            print("暂无销售记录")
            return
        
        # 不再移除第一行，因为pandas已经正确处理了列标题
        if df.empty:
            print("暂无销售记录")
            return
        
        # 需要考虑销售单位（斤/克）的转换，将所有销售数量统一转换为斤 - 向量化操作
        units = df.get('销售单位', pd.Series(['斤'] * len(df), index=df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        df['销售数量(斤)'] = df['销售数量'] * unit_multiplier
        
        # 按商品编号统计销售数量（以斤为单位）
        sales_summary = df.groupby('商品编号').agg({
            '销售数量(斤)': 'sum',
            '实收金额': 'sum'
        }).round(2)
        sales_summary.columns = ['总销售数量(斤)', '总销售额']
        
        # 与商品信息合并获取商品名称
        commodity_df = self.excel_manager.get_all_commodities()
        if not commodity_df.empty:
            result = pd.merge(sales_summary, commodity_df[['商品编号', '商品名称', '茶类']], 
                            on='商品编号', how='left')
            
            # 按销售数量排序
            result = result.sort_values(by='总销售数量(斤)', ascending=False)
            
            print("\n=== 热销商品排行 ===")
            table = PrettyTable(['排名', '商品编号', '商品名称', '茶类', '销售数量(斤)', '销售额'])
            rank = 1
            for _, row in result.head(10).iterrows():  # 显示前10名
                table.add_row([rank, row['商品编号'], row['商品名称'], 
                             row['茶类'], row['总销售数量(斤)'], row['总销售额']])
                rank += 1
            print(table)
    
    def profit_analysis(self):
        """盈利分析"""
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty or len(df) <= 0:  # 修改条件
            print("暂无销售记录")
            return
        
        # 不再移除第一行，因为pandas已经正确处理了列标题
        if df.empty:
            print("暂无销售记录")
            return
        
        # 与商品信息合并获取成本价
        commodity_df = self.excel_manager.get_all_commodities()
        if not commodity_df.empty:
            commodity_df['成本价'] = pd.to_numeric(commodity_df['成本价'], errors='coerce')
            
            # 计算每笔销售的成本
            merged_df = pd.merge(df, commodity_df[['商品编号', '成本价']], 
                               on='商品编号', how='left')
            
            # 计算每笔销售的成本和利润，需要考虑销售单位 - 向量化操作
            units = merged_df.get('销售单位', pd.Series(['斤'] * len(merged_df), index=merged_df.index))
            unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
            quantity_in_jin = merged_df['销售数量'] * unit_multiplier
            merged_df['销售成本'] = quantity_in_jin * merged_df['成本价']
            merged_df['销售收入'] = merged_df['实收金额']
            merged_df['利润'] = merged_df['销售收入'] - merged_df['销售成本']
            
            total_cost = merged_df['销售成本'].sum()
            total_income = merged_df['销售收入'].sum()
            total_profit = merged_df['利润'].sum()
            profit_margin = (total_profit / total_income * 100) if total_income > 0 else 0
            
            print("\n=== 盈利分析 ===")
            print(f"总销售收入: {total_income:.2f} 元")
            print(f"总销售成本: {total_cost:.2f} 元")
            print(f"总利润: {total_profit:.2f} 元")
            print(f"利润率: {profit_margin:.2f}%")
    
    def run(self):
        """运行系统"""
        while True:
            print("\n" + "="*50)
            print("           茶叶进销存管理系统")
            print("="*50)
            print("1. 商品管理")
            print("2. 销售功能")
            print("3. 进货管理")
            print("4. 供应商管理")
            print("5. 客户管理")
            print("6. 销售记录管理")
            print("7. 统计分析")
            print("0. 退出系统")
            print("-"*50)

            choice = input("请选择功能: ").strip()

            if choice == '1':
                self.product_management_menu()
            elif choice == '2':
                self.sales_management_menu()
            elif choice == '3':
                self.stock_management_menu()
            elif choice == '4':
                self.manage_suppliers()
            elif choice == '5':
                self.manage_customers()
            elif choice == '6':
                self.sales_record_management_menu()
            elif choice == '7':
                self.statistics_analysis_menu()
            elif choice == '0':
                print("感谢使用茶叶进销存管理系统！")
                break
            else:
                print("无效选择，请重新输入")
    
    def product_management_menu(self):
        """商品管理菜单"""
        while True:
            print("\n=== 商品管理 ===")
            print("1. 添加商品")
            print("2. 查询所有商品")
            print("3. 按编号查询商品")
            print("4. 修改商品信息")
            print("5. 删除商品")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.add_commodity()
            elif choice == '2':
                self.query_all_commodities()
            elif choice == '3':
                self.query_commodity_by_id()
            elif choice == '4':
                self.update_commodity()
            elif choice == '5':
                self.delete_commodity()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def sales_management_menu(self):
        """销售管理菜单"""
        while True:
            print("\n=== 销售管理 ===")
            print("1. 添加商品到购物车")
            print("2. 查看购物车")
            print("3. 清空购物车")
            print("4. 结账")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.add_to_cart()
            elif choice == '2':
                self.view_cart()
            elif choice == '3':
                self.clear_cart()
            elif choice == '4':
                self.checkout()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def stock_management_menu(self):
        """进货管理菜单"""
        while True:
            print("\n=== 进货管理 ===")
            print("1. 进货入库")
            print("2. 查看进货记录")
            print("0. 返回上级菜单")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '1':
                self.stock_in()
            elif choice == '2':
                df = self.excel_manager.get_all_stocks()
                if df.empty:
                    print("暂无进货记录")
                else:
                    # 修复：只要DataFrame不为空，就说明有数据记录
                    # pandas读取Excel时，会将第一行作为列标题，后续行为实际数据
                    if not df.empty:
                        table = PrettyTable()
                        table.field_names = df.columns.tolist()  # 使用原始列名
                        for _, row in df.iterrows():
                            table.add_row(row.values)
                        print(table)
                        print(f"以上共 {len(df)} 条记录。")
                    else:
                        print("暂无进货记录")
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")
    
    def statistics_analysis_menu(self):
        """统计分析菜单"""
        while True:
            print("\n=== 统计分析 ===")
            print("1. 销售统计")
            print("2. 热销商品排行")
            print("3. 盈利分析")
            print("4. 数据可视化")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self.sales_statistics()
            elif choice == '2':
                self.top_selling_products()
            elif choice == '3':
                self.profit_analysis()
            elif choice == '4':
                self.data_viz.show_chart_menu()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")

    # 客户管理
    def manage_customers(self):
        """管理客户"""
        while True:
            print("\n=== 客户管理 ===")
            print("1. 查看所有客户")
            print("2. 添加客户")
            print("3. 按编号查询客户")
            print("4. 按名称查询客户")
            print("5. 修改客户信息")
            print("6. 删除客户")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self.view_all_customers()
            elif choice == '2':
                self.add_customer()
            elif choice == '3':
                self.query_customer_by_id()
            elif choice == '4':
                self.query_customer_by_name()
            elif choice == '5':
                self.update_customer()
            elif choice == '6':
                self.delete_customer()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")

    def view_all_customers(self):
        """查看所有客户"""
        df = self.excel_manager.get_all_customers()
        if df.empty:
            print("暂无客户信息")
            return

        table = PrettyTable()
        table.field_names = df.columns.tolist()

        for _, row in df.iterrows():
            table.add_row(row.values)

        print(table)
        print(f"以上共 {len(df)} 条记录。")

    def add_customer(self):
        """添加客户"""
        print("=== 添加客户 ===")

        customer_id_input = input("请输入客户编号(留空则自动生成): ").strip()
        if customer_id_input:
            customer_id = customer_id_input
            existing = self.excel_manager.get_customer_by_id(customer_id)
            if existing is not None:
                print("错误：该客户编号已存在！")
                return
        else:
            customer_id = self.excel_manager.generate_id("K", "客户信息", "客户编号")
            print(f"自动生成的客户编号: {customer_id}")

        name = input("请输入客户名称: ").strip()
        phone = input("请输入联系电话: ").strip()
        email = input("请输入电子邮箱: ").strip()
        address = input("请输入地址: ").strip()
        remarks = input("请输入备注: ").strip()

        customer = Customer(
            customer_id=customer_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            remarks=remarks
        )

        self.excel_manager.add_customer(customer.to_list())
        print("客户添加成功！")

    def query_customer_by_id(self):
        """按编号查询客户"""
        customer_id = input("请输入客户编号: ").strip()
        customer = self.excel_manager.get_customer_by_id(customer_id)

        if customer is None:
            print("未找到该客户")
            return

        table = PrettyTable(['属性', '值'])
        for key, value in customer.items():
            table.add_row([key, value])
        print(table)

    def query_customer_by_name(self):
        """按名称查询客户"""
        name = input("请输入客户名称: ").strip()
        customer = self.excel_manager.get_customer_by_name(name)

        if customer is None:
            print("未找到该客户")
            return

        table = PrettyTable(['属性', '值'])
        for key, value in customer.items():
            table.add_row([key, value])
        print(table)

    def update_customer(self):
        """修改客户信息"""
        customer_id = input("请输入要修改的客户编号: ").strip()
        customer = self.excel_manager.get_customer_by_id(customer_id)

        if customer is None:
            print("未找到该客户")
            return

        print("当前客户信息：")
        self._print_single_customer(customer)

        print("\n请输入新的信息（直接回车保持原值）：")

        updates = {}

        new_name = input(f"客户名称 (当前: {customer['客户名称']}): ").strip()
        if new_name: updates['客户名称'] = new_name

        new_phone = input(f"联系电话 (当前: {customer['联系电话']}): ").strip()
        if new_phone: updates['联系电话'] = new_phone

        new_email = input(f"电子邮箱 (当前: {customer['电子邮箱']}): ").strip()
        if new_email: updates['电子邮箱'] = new_email

        new_address = input(f"地址 (当前: {customer['地址']}): ").strip()
        if new_address: updates['地址'] = new_address

        new_remarks = input(f"备注 (当前: {customer['备注']}): ").strip()
        if new_remarks: updates['备注'] = new_remarks

        if updates:
            success = self.excel_manager.update_customer(customer_id, updates)
            if success:
                print("客户信息更新成功！")
            else:
                print("更新失败！")
        else:
            print("未做任何修改。")

    def delete_customer(self):
        """删除客户"""
        customer_id = input("请输入要删除的客户编号: ").strip()
        customer = self.excel_manager.get_customer_by_id(customer_id)

        if customer is None:
            print("未找到该客户")
            return

        confirm = input(f"确定要删除客户 '{customer['客户名称']}' 吗？(y/N): ").strip().lower()
        if confirm == 'y':
            success = self.excel_manager.delete_customer(customer_id)
            if success:
                print("客户删除成功！")
            else:
                print("删除失败！")
        else:
            print("操作已取消。")

    def _print_single_customer(self, customer):
        """打印单个客户信息"""
        table = PrettyTable(['属性', '值'])
        for key, value in customer.items():
            table.add_row([key, value])
        print(table)

    # 销售记录管理
    def sales_record_management_menu(self):
        """销售记录管理菜单"""
        while True:
            print("\n=== 销售记录管理 ===")
            print("1. 查询销售记录（多条件）")
            print("2. 查看所有销售记录")
            print("3. 修改销售记录")
            print("4. 作废销售记录")
            print("0. 返回上级菜单")

            choice = input("请选择操作: ").strip()

            if choice == '1':
                self.query_sales_records()
            elif choice == '2':
                self.view_all_sales()
            elif choice == '3':
                self.update_sale_record()
            elif choice == '4':
                self.void_sale_record()
            elif choice == '0':
                break
            else:
                print("无效选择，请重新输入")

    def view_all_sales(self):
        """查看所有销售记录"""
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty:
            print("暂无销售记录")
            return

        table = PrettyTable()
        table.field_names = df.columns.tolist()

        for _, row in df.iterrows():
            table.add_row(row.values)

        print(table)
        print(f"以上共 {len(df)} 条记录。")

    def query_sales_records(self):
        """多条件查询销售记录"""
        print("=== 销售记录查询 ===")
        print("（留空表示不限制该条件）")

        start_date = input("请输入开始日期 (YYYY-MM-DD): ").strip() or None
        end_date = input("请输入结束日期 (YYYY-MM-DD): ").strip() or None
        customer_name = input("请输入客户名称: ").strip() or None
        com_id = input("请输入商品编号: ").strip() or None
        com_name = input("请输入商品名称: ").strip() or None

        df = self.excel_manager.query_sales(
            start_date=start_date,
            end_date=end_date,
            customer_name=customer_name,
            com_id=com_id,
            com_name=com_name
        )

        if df.empty:
            print("未找到符合条件的销售记录")
            return

        table = PrettyTable()
        table.field_names = df.columns.tolist()

        for _, row in df.iterrows():
            table.add_row(row.values)

        print(table)
        print(f"以上共 {len(df)} 条记录。")

    def update_sale_record(self):
        """修改销售记录"""
        sale_id = input("请输入要修改的销售编号: ").strip()
        sale = self.excel_manager.get_sale_by_id(sale_id)

        if sale is None:
            print("未找到该销售记录")
            return

        print("当前销售记录信息：")
        self._print_single_sale(sale)

        print("\n请输入新的信息（直接回车保持原值）：")
        print("注意：修改数量或单位会回滚并重新扣减库存！")

        updates = {}
        rollback = False

        new_qty = input(f"销售数量 (当前: {sale['销售数量']}): ").strip()
        if new_qty:
            try:
                updates['销售数量'] = float(new_qty)
                rollback = True
            except ValueError:
                print("数量必须是数字！")
                return

        new_unit = input(f"销售单位 (当前: {sale.get('销售单位', '克')}): ").strip()
        if new_unit:
            updates['销售单位'] = new_unit
            rollback = True

        new_price = input(f"单价 (当前: {sale['单价']}): ").strip()
        if new_price:
            try:
                updates['单价'] = float(new_price)
            except ValueError:
                print("单价必须是数字！")
                return

        new_customer = input(f"客户名称 (当前: {sale['客户名称']}): ").strip()
        if new_customer:
            updates['客户名称'] = new_customer

        if updates:
            confirm = input(f"确认修改销售记录？(y/N): ").strip().lower()
            if confirm == 'y':
                success = self.excel_manager.update_sale(sale_id, updates, rollback_stock=rollback)
                if success:
                    print("销售记录更新成功！")
                else:
                    print("更新失败！")
            else:
                print("操作已取消。")
        else:
            print("未做任何修改。")

    def void_sale_record(self):
        """作废销售记录"""
        sale_id = input("请输入要作废的销售编号: ").strip()
        sale = self.excel_manager.get_sale_by_id(sale_id)

        if sale is None:
            print("未找到该销售记录")
            return

        print("当前销售记录信息：")
        self._print_single_sale(sale)

        confirm = input(f"确定要作废该销售记录？这将回滚库存！(y/N): ").strip().lower()
        if confirm == 'y':
            success = self.excel_manager.void_sale(sale_id)
            if success:
                print("销售记录已作废，库存已回滚！")
            else:
                print("作废失败！")
        else:
            print("操作已取消。")

    def _print_single_sale(self, sale):
        """打印单个销售记录"""
        table = PrettyTable(['属性', '值'])
        for key, value in sale.items():
            table.add_row([key, value])
        print(table)

    # ==================== 纯业务方法（可供 CLI 和 GUI 共用） ====================

    def add_commodity_business(self, com_id_input, tea_category, variety, company, origin,
                               name, specification, cost_price, retail_price, current_stock,
                               production_date, shelf_life, quality_features, year, grade, unit):
        if com_id_input:
            existing = self.excel_manager.get_commodity_by_id(com_id_input)
            if existing is not None:
                return {'success': False, 'message': '该商品编号已存在！'}
            com_id = com_id_input
        else:
            com_id = self.excel_manager.generate_id("C", "商品信息", "商品编号")

        commodity = TeaCommodity(
            com_id=com_id, tea_category=tea_category, variety=variety,
            company=company, origin=origin, name=name,
            specification=specification, cost_price=cost_price,
            retail_price=retail_price, production_date=production_date,
            shelf_life=shelf_life, current_stock=current_stock,
            quality_features=quality_features, year=year, grade=grade, unit=unit
        )
        self.excel_manager.add_commodity(commodity.to_list())
        return {'success': True, 'message': '商品添加成功！', 'com_id': com_id}

    def checkout_process(self, customer_name, received_amount):
        return self.shopping_cart.checkout(customer_name, received_amount)

    def create_stock_record_business(self, com_id, unit_price, quantity, unit, supplier,
                                     stock_date, remarks):
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        if commodity is None:
            return {'success': False, 'message': '商品不存在，请先添加商品'}

        stock_id = self.excel_manager.generate_id("I", "进货记录", "进货编号")
        stock_record = StockRecord(
            stock_id=stock_id, com_id=com_id, com_name=commodity['商品名称'],
            quantity=quantity, unit_price=unit_price, supplier=supplier,
            stock_date=stock_date, remarks=remarks, stock_unit=unit
        )
        self.excel_manager.add_stock(stock_record.to_list())
        return {'success': True, 'message': '进货记录已保存', 'stock_id': stock_id}

    def add_supplier_business(self, supplier_id_input, name, contact_person, phone, address, remarks):
        if supplier_id_input:
            supplier_id = supplier_id_input
            df = self.excel_manager.get_all_suppliers()
            if not df.empty:
                existing = df[df['供应商编号'] == supplier_id]
                if not existing.empty:
                    return {'success': False, 'message': '该供应商编号已存在！'}
        else:
            supplier_id = self.excel_manager.generate_id("SP", "供应商", "供应商编号")

        supplier = Supplier(
            supplier_id=supplier_id, name=name, contact_person=contact_person,
            phone=phone, address=address, remarks=remarks
        )
        self.excel_manager.add_supplier(supplier.to_list())
        return {'success': True, 'message': '供应商添加成功！', 'supplier_id': supplier_id}

    def update_supplier_business(self, supplier_id, updates):
        df = self.excel_manager.get_all_suppliers()
        if df.empty:
            return {'success': False, 'message': '暂无供应商信息'}

        idx_list = df[df['供应商编号'] == supplier_id].index
        if len(idx_list) == 0:
            return {'success': False, 'message': '未找到该供应商'}

        for key, value in updates.items():
            if value:
                df.at[idx_list[0], key] = value

        self.excel_manager.write_sheet("供应商", df)
        return {'success': True, 'message': '供应商信息更新成功！'}

    def delete_supplier_business(self, supplier_id):
        df = self.excel_manager.get_all_suppliers()
        if df.empty:
            return {'success': False, 'message': '暂无供应商信息'}

        supplier_row = df[df['供应商编号'] == supplier_id]
        if supplier_row.empty:
            return {'success': False, 'message': '未找到该供应商'}

        supplier_name = supplier_row.iloc[0]['供应商名称']
        new_df = df[df['供应商编号'] != supplier_id]
        self.excel_manager.write_sheet("供应商", new_df)
        return {'success': True, 'message': '供应商删除成功！', 'name': supplier_name}

    def add_customer_business(self, customer_id_input, name, phone, email, address, remarks):
        if customer_id_input:
            customer_id = customer_id_input
            existing = self.excel_manager.get_customer_by_id(customer_id)
            if existing is not None:
                return {'success': False, 'message': '该客户编号已存在！'}
        else:
            customer_id = self.excel_manager.generate_id("K", "客户信息", "客户编号")

        customer = Customer(
            customer_id=customer_id, name=name, phone=phone, email=email,
            address=address, remarks=remarks
        )
        customer.update_customer_level()
        self.excel_manager.add_customer(customer.to_list())
        return {'success': True, 'message': '客户添加成功！', 'customer_id': customer_id,
                'customer_level': customer.customer_level}

    def update_customer_business(self, customer_id, updates):
        all_customers = self.excel_manager.get_all_customers()
        if all_customers.empty:
            return {'success': False, 'message': '暂无客户信息'}

        idx_list = all_customers[all_customers['客户编号'] == customer_id].index
        if len(idx_list) == 0:
            return {'success': False, 'message': '未找到该客户'}

        for key, value in updates.items():
            all_customers.at[idx_list[0], key] = value

        total_purchases = updates.get('累计消费', all_customers.at[idx_list[0], '累计消费'])
        if float(total_purchases) >= 10000:
            customer_level = "VIP客户"
        elif float(total_purchases) >= 5000:
            customer_level = "高级客户"
        elif float(total_purchases) >= 2000:
            customer_level = "中级客户"
        else:
            customer_level = "普通客户"
        all_customers.at[idx_list[0], '客户等级'] = customer_level

        self.excel_manager.write_sheet("客户", all_customers)
        return {'success': True, 'message': '客户信息更新成功！'}

    def delete_customer_business(self, customer_id):
        all_customers = self.excel_manager.get_all_customers()
        if all_customers.empty:
            return {'success': False, 'message': '暂无客户信息'}

        customer_row = all_customers[all_customers['客户编号'] == customer_id]
        if customer_row.empty:
            return {'success': False, 'message': '未找到该客户'}

        customer_name = customer_row.iloc[0]['客户名称']
        new_df = all_customers[all_customers['客户编号'] != customer_id]
        self.excel_manager.write_sheet("客户", new_df)
        return {'success': True, 'message': '客户删除成功！', 'name': customer_name}

    def get_sales_statistics_data(self, dimension=None):
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty:
            return None

        commodity_df = self.excel_manager.get_all_commodities()
        if commodity_df.empty:
            return None

        commodity_df['成本价'] = pd.to_numeric(commodity_df['成本价'], errors='coerce')
        merged_df = pd.merge(df, commodity_df[['商品编号', '茶类', '品种', '成本价']],
                           on='商品编号', how='left')

        units = merged_df.get('销售单位', pd.Series(['斤'] * len(merged_df), index=merged_df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        merged_df['销售数量(斤)'] = merged_df['销售数量'] * unit_multiplier
        merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
        merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']

        total_income = merged_df['实收金额'].sum()
        total_cost = merged_df['销售成本'].sum()
        total_profit = merged_df['利润'].sum()
        total_quantity = merged_df['销售数量(斤)'].sum()

        summary = {
            'total_sales_count': len(df),
            'total_income': total_income,
            'total_cost': total_cost,
            'total_profit': total_profit,
            'profit_margin': (total_profit / total_income * 100) if total_income > 0 else 0,
            'total_quantity': total_quantity,
            'merged_df': merged_df
        }

        if dimension is None:
            return summary

        if dimension == '茶类' and '茶类' in merged_df.columns:
            stats = merged_df.groupby('茶类').agg({
                '销售数量(斤)': 'sum', '实收金额': 'sum',
                '销售成本': 'sum', '利润': 'sum'
            }).round(2)
            stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
            return stats.reset_index()

        elif dimension == '品种' and '品种' in merged_df.columns:
            stats = merged_df.groupby('品种').agg({
                '销售数量(斤)': 'sum', '实收金额': 'sum',
                '销售成本': 'sum', '利润': 'sum'
            }).round(2)
            stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
            return stats.reset_index()

        elif dimension == '商品' and '商品名称' in merged_df.columns:
            stats = merged_df.groupby(['商品编号', '商品名称']).agg({
                '销售数量(斤)': 'sum', '实收金额': 'sum',
                '销售成本': 'sum', '利润': 'sum'
            }).round(2)
            stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
            return stats.reset_index()

        return summary

    def get_sales_statistics_by_time_data(self, time_unit):
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty:
            return None

        df['销售日期'] = pd.to_datetime(df['销售日期'], errors='coerce')

        units = df.get('销售单位', pd.Series(['斤'] * len(df), index=df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        df['销售数量(斤)'] = df['销售数量'] * unit_multiplier

        commodity_df = self.excel_manager.get_all_commodities()
        if not commodity_df.empty:
            merged_df = pd.merge(df, commodity_df[['商品编号', '成本价']],
                               on='商品编号', how='left')
            merged_df['销售成本'] = merged_df['销售数量(斤)'] * pd.to_numeric(merged_df['成本价'], errors='coerce')
            merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']
        else:
            merged_df = df
            merged_df['销售成本'] = 0
            merged_df['利润'] = merged_df['实收金额']

        if time_unit == '日':
            grouped = merged_df.groupby(merged_df['销售日期'].dt.date)
        elif time_unit == '周':
            grouped = merged_df.groupby(merged_df['销售日期'].dt.to_period('W'))
        elif time_unit == '月':
            grouped = merged_df.groupby(merged_df['销售日期'].dt.to_period('M'))
        else:
            return None

        stats = grouped.agg({
            '销售数量(斤)': 'sum', '实收金额': 'sum',
            '销售成本': 'sum', '利润': 'sum'
        }).round(2)
        stats['利润率(%)'] = (stats['利润'] / stats['实收金额'] * 100).round(2)
        return stats.reset_index()

    def get_top_selling_products_data(self):
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty:
            return None

        units = df.get('销售单位', pd.Series(['斤'] * len(df), index=df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        df['销售数量(斤)'] = df['销售数量'] * unit_multiplier

        stats = df.groupby(['商品编号', '商品名称']).agg({
            '销售数量(斤)': 'sum', '实收金额': 'sum'
        }).round(2)
        stats = stats.sort_values(by='销售数量(斤)', ascending=False).head(10)
        return stats.reset_index()

    def get_profit_analysis_data(self):
        df = self.excel_manager.get_all_sales(include_voided=False)
        if df.empty:
            return None

        commodity_df = self.excel_manager.get_all_commodities()
        if commodity_df.empty:
            return None

        commodity_df['成本价'] = pd.to_numeric(commodity_df['成本价'], errors='coerce')
        merged_df = pd.merge(df, commodity_df[['商品编号', '成本价']],
                           on='商品编号', how='left')

        units = merged_df.get('销售单位', pd.Series(['斤'] * len(merged_df), index=merged_df.index))
        unit_multiplier = units.map(lambda x: 1/500 if x == '克' else 1)
        merged_df['销售数量(斤)'] = merged_df['销售数量'] * unit_multiplier
        merged_df['销售成本'] = merged_df['销售数量(斤)'] * merged_df['成本价']
        merged_df['利润'] = merged_df['实收金额'] - merged_df['销售成本']

        total_income = merged_df['实收金额'].sum()
        total_cost = merged_df['销售成本'].sum()
        total_profit = merged_df['利润'].sum()
        profit_margin = (total_profit / total_income * 100) if total_income > 0 else 0

        product_profit = merged_df.groupby(['商品编号', '商品名称']).agg({
            '销售数量(斤)': 'sum', '实收金额': 'sum',
            '销售成本': 'sum', '利润': 'sum'
        }).round(2)
        product_profit['利润率(%)'] = (product_profit['利润'] / product_profit['实收金额'] * 100).round(2)
        product_profit = product_profit.sort_values(by='利润', ascending=False)

        return {
            'total_income': total_income,
            'total_cost': total_cost,
            'total_profit': total_profit,
            'profit_margin': profit_margin,
            'product_profit': product_profit.reset_index()
        }