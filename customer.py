
from datetime import datetime


class Customer:
    """客户类"""

    def __init__(self, customer_id="", name="", phone="", email="", address="",
                 total_purchases=0.0, total_orders=0, last_purchase_date="",
                 customer_level="普通客户", remarks="", create_date=""):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.total_purchases = total_purchases
        self.total_orders = total_orders
        self.last_purchase_date = last_purchase_date
        self.customer_level = customer_level
        self.remarks = remarks
        self.create_date = create_date if create_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_list(self):
        """转换为列表格式，用于Excel存储"""
        return [
            self.customer_id, self.name, self.phone, self.email,
            self.address, self.total_purchases, self.total_orders,
            self.last_purchase_date, self.customer_level, self.remarks, self.create_date
        ]

    def to_dict(self):
        """转换为字典格式"""
        return {
            '客户编号': self.customer_id,
            '客户名称': self.name,
            '联系电话': self.phone,
            '电子邮箱': self.email,
            '地址': self.address,
            '累计消费': self.total_purchases,
            '订单数': self.total_orders,
            '最后购买日期': self.last_purchase_date,
            '客户等级': self.customer_level,
            '备注': self.remarks,
            '创建日期': self.create_date
        }

    @classmethod
    def from_series(cls, series):
        """从pandas Series创建实例"""
        return cls(
            customer_id=series.get('客户编号', ''),
            name=series.get('客户名称', ''),
            phone=series.get('联系电话', ''),
            email=series.get('电子邮箱', ''),
            address=series.get('地址', ''),
            total_purchases=series.get('累计消费', 0.0),
            total_orders=series.get('订单数', 0),
            last_purchase_date=series.get('最后购买日期', ''),
            customer_level=series.get('客户等级', '普通客户'),
            remarks=series.get('备注', ''),
            create_date=series.get('创建日期', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    def add_purchase(self, amount, purchase_date=""):
        """添加购买记录，更新客户统计信息"""
        self.total_purchases += amount
        self.total_orders += 1
        self.last_purchase_date = purchase_date if purchase_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 更新客户等级
        self.update_customer_level()

    def update_customer_level(self):
        """根据累计消费更新客户等级"""
        if self.total_purchases >= 10000:
            self.customer_level = "VIP客户"
        elif self.total_purchases >= 5000:
            self.customer_level = "高级客户"
        elif self.total_purchases >= 2000:
            self.customer_level = "中级客户"
        else:
            self.customer_level = "普通客户"

