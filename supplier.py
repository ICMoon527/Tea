class Supplier:
    """供应商类"""
    def __init__(self, supplier_id="", name="", contact_person="", phone="", address="", remarks=""):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.address = address
        self.remarks = remarks
    
    def to_list(self):
        """转换为列表格式，用于Excel存储"""
        return [
            self.supplier_id, self.name, self.contact_person, 
            self.phone, self.address, self.remarks
        ]
    
    @classmethod
    def from_series(cls, series):
        """从pandas Series创建实例"""
        return cls(
            supplier_id=series.get('供应商编号', ''),
            name=series.get('供应商名称', ''),
            contact_person=series.get('联系人', ''),
            phone=series.get('联系电话', ''),
            address=series.get('地址', ''),
            remarks=series.get('备注', '')
        )