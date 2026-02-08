class TeaCommodity:
    """茶叶商品类"""
    def __init__(self, com_id="", tea_category="", variety="", company="", origin="", 
                 name="", specification="", cost_price=0.0, retail_price=0.0, 
                 production_date="", shelf_life=0, current_stock=0, 
                 quality_features="", year="", grade="", unit="斤"):
        self.com_id = com_id
        self.tea_category = tea_category  # 茶类：红茶、绿茶、乌龙茶等
        self.variety = variety           # 品种：如正山小种、铁观音等
        self.company = company          # 公司/品牌
        self.origin = origin            # 产区
        self.name = name               # 商品名称
        self.specification = specification  # 规格
        self.cost_price = cost_price    # 成本价（每斤价格）
        self.retail_price = retail_price  # 零售价（每斤价格）
        self.production_date = production_date  # 生产日期
        self.shelf_life = shelf_life    # 保质期(月)
        self.current_stock = current_stock  # 当前库存（以斤为单位）
        self.quality_features = quality_features  # 品质特征
        self.year = year               # 年份
        self.grade = grade             # 等级
        self.unit = unit               # 计量单位（斤或克）
    
    @staticmethod
    def convert_units(amount, from_unit, to_unit):
        """单位转换：斤与克之间的转换"""
        if from_unit == to_unit:
            return amount
        elif from_unit == "斤" and to_unit == "克":
            return amount * 500  # 1斤 = 500克
        elif from_unit == "克" and to_unit == "斤":
            return amount / 500  # 1克 = 0.002斤
        else:
            raise ValueError(f"不支持的单位转换: {from_unit} -> {to_unit}")
    
    def to_list(self):
        """转换为列表格式，用于Excel存储"""
        return [
            self.com_id, self.tea_category, self.variety, self.company, 
            self.origin, self.name, self.specification, self.cost_price, 
            self.retail_price, self.production_date, self.shelf_life, 
            self.current_stock, self.quality_features, self.year, self.grade, self.unit
        ]
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            '商品编号': self.com_id,
            '茶类': self.tea_category,
            '品种': self.variety,
            '公司': self.company,
            '产区': self.origin,
            '商品名称': self.name,
            '规格': self.specification,
            '成本价': self.cost_price,
            '零售价': self.retail_price,
            '生产日期': self.production_date,
            '保质期(月)': self.shelf_life,
            '当前库存': self.current_stock,
            '品质特征': self.quality_features,
            '年份': self.year,
            '等级': self.grade,
            '单位': self.unit
        }
    
    @classmethod
    def from_series(cls, series):
        """从pandas Series创建实例"""
        return cls(
            com_id=series.get('商品编号', ''),
            tea_category=series.get('茶类', ''),
            variety=series.get('品种', ''),
            company=series.get('公司', ''),
            origin=series.get('产区', ''),
            name=series.get('商品名称', ''),
            specification=series.get('规格', ''),
            cost_price=series.get('成本价', 0.0),
            retail_price=series.get('零售价', 0.0),
            production_date=series.get('生产日期', ''),
            shelf_life=series.get('保质期(月)', 0),
            current_stock=series.get('当前库存', 0),
            quality_features=series.get('品质特征', ''),
            year=series.get('年份', ''),
            grade=series.get('等级', ''),
            unit=series.get('单位', '斤')
        )