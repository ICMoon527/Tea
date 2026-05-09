import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime
import os


class DataExporter:
    """数据导出管理器"""
    
    EXPORT_FORMATS = {
        'excel': 'Excel文件 (*.xlsx)',
        'csv': 'CSV文件 (*.csv)',
        'json': 'JSON文件 (*.json)'
    }
    
    def __init__(self, excel_manager):
        self.excel_manager = excel_manager
    
    def export_commodities(
        self,
        export_path: str,
        format: str = 'excel',
        filters: Optional[Dict] = None
    ) -> bool:
        """导出商品数据
        
        Args:
            export_path: 导出文件路径
            format: 导出格式（excel/csv/json）
            filters: 过滤条件
            
        Returns:
            是否导出成功
        """
        try:
            df = self.excel_manager.get_all_commodities()
            
            if filters:
                if '茶类' in filters and filters['茶类']:
                    df = df[df['茶类'] == filters['茶类']]
                if '品种' in filters and filters['品种']:
                    df = df[df['品种'] == filters['品种']]
            
            return self._export_dataframe(df, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出商品数据失败: {e}")
            return False
    
    def export_sales(
        self,
        export_path: str,
        format: str = 'excel',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> bool:
        """导出销售数据
        
        Args:
            export_path: 导出文件路径
            format: 导出格式
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            是否导出成功
        """
        try:
            df = self.excel_manager.get_all_sales()
            
            if not df.empty:
                if start_date:
                    df = df[df['销售日期'] >= start_date]
                if end_date:
                    df = df[df['销售日期'] <= end_date]
            
            return self._export_dataframe(df, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出销售数据失败: {e}")
            return False
    
    def export_stocks(
        self,
        export_path: str,
        format: str = 'excel',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> bool:
        """导出进货数据
        
        Args:
            export_path: 导出文件路径
            format: 导出格式
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            是否导出成功
        """
        try:
            df = self.excel_manager.get_all_stocks()
            
            if not df.empty:
                if start_date:
                    df = df[df['进货日期'] >= start_date]
                if end_date:
                    df = df[df['进货日期'] <= end_date]
            
            return self._export_dataframe(df, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出进货数据失败: {e}")
            return False
    
    def export_suppliers(
        self,
        export_path: str,
        format: str = 'excel'
    ) -> bool:
        """导出供应商数据
        
        Args:
            export_path: 导出文件路径
            format: 导出格式
            
        Returns:
            是否导出成功
        """
        try:
            df = self.excel_manager.get_all_suppliers()
            return self._export_dataframe(df, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出供应商数据失败: {e}")
            return False
    
    def export_customers(
        self,
        export_path: str,
        format: str = 'excel'
    ) -> bool:
        """导出客户数据
        
        Args:
            export_path: 导出文件路径
            format: 导出格式
            
        Returns:
            是否导出成功
        """
        try:
            df = self.excel_manager.get_all_customers()
            return self._export_dataframe(df, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出客户数据失败: {e}")
            return False
    
    def export_statistics(
        self,
        export_path: str,
        statistics_data: pd.DataFrame,
        format: str = 'excel'
    ) -> bool:
        """导出统计数据
        
        Args:
            export_path: 导出文件路径
            statistics_data: 统计数据DataFrame
            format: 导出格式
            
        Returns:
            是否导出成功
        """
        try:
            return self._export_dataframe(statistics_data, export_path, format)
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出统计数据失败: {e}")
            return False
    
    def export_all_data(
        self,
        export_dir: str,
        format: str = 'excel'
    ) -> Dict[str, bool]:
        """导出所有数据
        
        Args:
            export_dir: 导出目录
            format: 导出格式
            
        Returns:
            各模块导出结果字典
        """
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        
        extension = self._get_extension(format)
        
        results['商品'] = self.export_commodities(
            os.path.join(export_dir, f"商品数据_{timestamp}.{extension}"),
            format
        )
        
        results['销售'] = self.export_sales(
            os.path.join(export_dir, f"销售数据_{timestamp}.{extension}"),
            format
        )
        
        results['进货'] = self.export_stocks(
            os.path.join(export_dir, f"进货数据_{timestamp}.{extension}"),
            format
        )
        
        results['供应商'] = self.export_suppliers(
            os.path.join(export_dir, f"供应商数据_{timestamp}.{extension}"),
            format
        )
        
        results['客户'] = self.export_customers(
            os.path.join(export_dir, f"客户数据_{timestamp}.{extension}"),
            format
        )
        
        return results
    
    def _export_dataframe(
        self,
        df: pd.DataFrame,
        export_path: str,
        format: str
    ) -> bool:
        """导出DataFrame到文件
        
        Args:
            df: 要导出的DataFrame
            export_path: 导出文件路径
            format: 导出格式
            
        Returns:
            是否导出成功
        """
        try:
            if format == 'excel':
                df.to_excel(export_path, index=False, engine='openpyxl')
            elif format == 'csv':
                df.to_csv(export_path, index=False, encoding='utf-8-sig')
            elif format == 'json':
                df.to_json(export_path, orient='records', force_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的导出格式: {format}")
            
            return True
        except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
            print(f"导出数据失败: {e}")
            return False
    
    def _get_extension(self, format: str) -> str:
        """获取文件扩展名
        
        Args:
            format: 格式名称
            
        Returns:
            文件扩展名
        """
        extensions = {
            'excel': 'xlsx',
            'csv': 'csv',
            'json': 'json'
        }
        return extensions.get(format, 'xlsx')
    
    def get_export_formats(self) -> Dict[str, str]:
        """获取支持的导出格式
        
        Returns:
            格式字典
        """
        return self.EXPORT_FORMATS.copy()
