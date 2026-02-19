from datetime import datetime


class SaleRecord:
    """销售记录类"""

    def __init__(self, sale_id="", com_id="", com_name="", quantity=0,
                 unit_price=0.0, total_amount=0.0, received_amount=0.0,
                 customer_name="", sale_date="", sale_unit="斤", is_void=False):
        self.sale_id = sale_id
        self.com_id = com_id
        self.com_name = com_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_amount = total_amount
        self.received_amount = received_amount
        self.customer_name = customer_name
        self.sale_date = sale_date if sale_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sale_unit = sale_unit
        self.is_void = is_void

    def to_list(self):
        """转换为列表格式，用于Excel存储"""
        return [
            self.sale_id, self.com_id, self.com_name, self.quantity,
            self.unit_price, self.total_amount, self.received_amount,
            self.customer_name, self.sale_date, self.sale_unit, self.is_void
        ]

    @classmethod
    def from_series(cls, series):
        """从pandas Series创建实例"""
        return cls(
            sale_id=series.get('销售编号', ''),
            com_id=series.get('商品编号', ''),
            com_name=series.get('商品名称', ''),
            quantity=series.get('销售数量', 0),
            unit_price=series.get('单价', 0.0),
            total_amount=series.get('应收金额', 0.0),
            received_amount=series.get('实收金额', 0.0),
            customer_name=series.get('客户名称', ''),
            sale_date=series.get('销售日期', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            sale_unit=series.get('销售单位', '斤'),
            is_void=series.get('是否作废', False)
        )