from datetime import datetime

class StockRecord:
    """进货记录类"""
    def __init__(self, stock_id="", com_id="", com_name="", quantity=0, 
                 unit_price=0.0, supplier="", stock_date="", remarks="", stock_unit="斤"):
        self.stock_id = stock_id
        self.com_id = com_id
        self.com_name = com_name
        self.quantity = quantity  # 进货数量
        self.unit_price = unit_price  # 单价（每斤的价格）
        self.supplier = supplier
        self.stock_date = stock_date if stock_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.remarks = remarks
        self.stock_unit = stock_unit  # 进货单位（斤）
    
    def to_list(self):
        """转换为列表格式，用于Excel存储"""
        return [
            self.stock_id, self.com_id, self.com_name, self.quantity,
            self.unit_price, self.supplier, self.stock_date, self.remarks, self.stock_unit
        ]
    
    @classmethod
    def from_series(cls, series):
        """从pandas Series创建实例"""
        return cls(
            stock_id=series.get('进货编号', ''),
            com_id=series.get('商品编号', ''),
            com_name=series.get('商品名称', ''),
            quantity=series.get('进货数量', 0),
            unit_price=series.get('进货单价', 0.0),
            supplier=series.get('供应商', ''),
            stock_date=series.get('进货日期', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            remarks=series.get('备注', ''),
            stock_unit=series.get('进货单位', '斤')
        )