import pandas as pd
from typing import List, Dict, Any, Tuple, Optional


class CRUDManager:
    """通用CRUD操作管理器 - 为商品/供应商/客户提供统一的增删改查模式"""

    def __init__(self, excel_manager, sheet_name: str, prefix: str, id_column: str = None):
        self.excel_manager = excel_manager
        self.sheet_name = sheet_name
        self.prefix = prefix
        self.id_column = id_column or "编号"

    def generate_id(self) -> str:
        return self.excel_manager.generate_id(self.prefix, self.sheet_name, self.id_column)

    def add(self, data: List[Any]) -> Tuple[bool, str]:
        result = self.excel_manager.add_record(self.sheet_name, data)
        if result.get("success"):
            return True, "添加成功"
        return False, result.get("message", "添加失败")

    def get_all(self) -> pd.DataFrame:
        return self.excel_manager.read_sheet(self.sheet_name)

    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        df = self.excel_manager.read_sheet(self.sheet_name)
        if df.empty:
            return None
        mask = df[self.id_column].astype(str) == str(record_id)
        matches = df[mask]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def update(self, record_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        result = self.excel_manager.update_record(self.sheet_name, record_id, updates, self.id_column)
        if result.get("success"):
            return True, "更新成功"
        return False, result.get("message", "更新失败")

    def delete(self, record_id: str) -> Tuple[bool, str]:
        result = self.excel_manager.delete_record(self.sheet_name, record_id, self.id_column)
        if result.get("success"):
            return True, "删除成功"
        return False, result.get("message", "删除失败")

    def search(self, keyword: str, columns: Optional[List[str]] = None) -> pd.DataFrame:
        df = self.excel_manager.read_sheet(self.sheet_name)
        if df.empty:
            return df
        if columns is None:
            columns = [col for col in df.columns if df[col].dtype == object]
        mask = pd.Series([False] * len(df))
        for col in columns:
            if col in df.columns:
                mask |= df[col].astype(str).str.contains(keyword, na=False)
        return df[mask]