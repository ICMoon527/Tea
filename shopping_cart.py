from utils import convert_to_jin
from sale_record import SaleRecord
import pandas as pd


class ShoppingCart:
    """Shopping cart management class"""
    
    def __init__(self, excel_manager):
        self.excel_manager = excel_manager
        self.items = []
    
    def add_item(self, com_id: str, quantity: float, unit: str) -> dict:
        commodity = self.excel_manager.get_commodity_by_id(com_id)
        if commodity is None:
            return {'success': False, 'message': 'Product not found'}
        
        available_stock = float(commodity['当前库存'])
        quantity_in_jin = convert_to_jin(quantity, unit)
        
        if quantity_in_jin > available_stock:
            msg = 'Insufficient stock! Available: ' + str(available_stock) + ' jin'
            return {'success': False, 'message': msg}
        
        cost_price = float(commodity['成本价']) if pd.notna(commodity['成本价']) else 0.0
        subtotal_cost = self._calculate_subtotal(quantity, unit, cost_price)
        
        for item in self.items:
            if item['商品编号'] == com_id:
                item['购买数量'] = quantity
                item['购买单位'] = unit
                item['小计'] = self._calculate_subtotal(quantity, unit, float(commodity['零售价']))
                item['成本价(每斤)'] = cost_price
                item['成本小计'] = subtotal_cost
                return {'success': True, 'message': 'Cart updated'}
        
        cart_item = {
            '商品编号': com_id,
            '商品名称': commodity['商品名称'],
            '单价(每斤)': float(commodity['零售价']),
            '成本价(每斤)': cost_price,
            '购买数量': quantity,
            '购买单位': unit,
            '小计': self._calculate_subtotal(quantity, unit, float(commodity['零售价'])),
            '成本小计': subtotal_cost
        }
        
        self.items.append(cart_item)
        return {'success': True, 'message': 'Added to cart'}
    
    def _calculate_subtotal(self, quantity: float, unit: str, unit_price: float) -> float:
        if unit == '斤':
            return quantity * unit_price
        else:
            return (quantity / 500) * unit_price
    
    def remove_item(self, com_id: str) -> bool:
        for i, item in enumerate(self.items):
            if item['商品编号'] == com_id:
                self.items.pop(i)
                return True
        return False
    
    def clear(self):
        self.items.clear()
    
    def is_empty(self):
        return len(self.items) == 0
    
    def get_total_amount(self) -> float:
        return sum(item['小计'] for item in self.items)
    
    def get_total_cost(self) -> float:
        return sum(item.get('成本小计', 0.0) for item in self.items)
    
    def get_items(self) -> list:
        return self.items.copy()
    
    def update_item_quantity(self, com_id, new_quantity, new_unit=None):
        for item in self.items:
            if item['商品编号'] == com_id:
                commodity = self.excel_manager.get_commodity_by_id(com_id)
                if commodity is None:
                    return {'success': False, 'message': 'Product not found'}
                
                unit_to_use = new_unit if new_unit is not None else item['购买单位']
                quantity_in_jin = convert_to_jin(new_quantity, unit_to_use)
                available_stock = float(commodity['当前库存'])
                
                if quantity_in_jin > available_stock:
                    msg = 'Insufficient stock! Available: ' + str(available_stock) + ' jin'
                    return {'success': False, 'message': msg}
                
                cost_price = float(commodity['成本价']) if pd.notna(commodity['成本价']) else 0.0
                item['购买数量'] = new_quantity
                item['购买单位'] = unit_to_use
                item['小计'] = self._calculate_subtotal(new_quantity, unit_to_use, float(commodity['零售价']))
                item['成本价(每斤)'] = cost_price
                item['成本小计'] = self._calculate_subtotal(new_quantity, unit_to_use, cost_price)
                return {'success': True, 'message': 'Quantity updated'}
        
        return {'success': False, 'message': 'Item not found in cart'}
    
    def checkout(self, customer_name, received_amount):
        total_amount = self.get_total_amount()
        
        if total_amount > 0:
            discount_ratio = received_amount / total_amount
        else:
            discount_ratio = 1.0

        sale_ids = []
        for item in self.items:
            sale_id = self.excel_manager.generate_id('S', '销售记录', '销售编号')
            sale_ids.append(sale_id)
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

        self.clear()

        discount = total_amount - received_amount if received_amount < total_amount else 0
        return {
            'success': True,
            'total_amount': total_amount,
            'received_amount': received_amount,
            'change': received_amount - total_amount,
            'discount_amount': discount,
            'sale_ids': sale_ids
        }