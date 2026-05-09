import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class AlertManager:
    """预警管理器 - 库存预警和保质期提醒"""
    
    def __init__(self, excel_manager):
        self.excel_manager = excel_manager
        self.default_low_stock_threshold = 1.0
        self.default_expiry_warning_days = 30
    
    def check_low_stock(
        self,
        threshold: Optional[float] = None
    ) -> pd.DataFrame:
        """检查库存不足的商品
        
        Args:
            threshold: 库存阈值，默认为1.0斤
            
        Returns:
            库存不足的商品DataFrame
        """
        if threshold is None:
            threshold = self.default_low_stock_threshold
        
        df = self.excel_manager.get_all_commodities()
        
        if df.empty:
            return df
        
        low_stock_df = df[df['当前库存'] < threshold].copy()
        
        if not low_stock_df.empty:
            low_stock_df['预警级别'] = low_stock_df['当前库存'].apply(
                lambda x: '紧急' if x <= 0 else '警告'
            )
            low_stock_df = low_stock_df.sort_values('当前库存', ascending=True)
        
        return low_stock_df
    
    def check_expiry(
        self,
        warning_days: Optional[int] = None
    ) -> pd.DataFrame:
        """检查即将过期的商品
        
        Args:
            warning_days: 预警天数，默认为30天
            
        Returns:
            即将过期的商品DataFrame
        """
        if warning_days is None:
            warning_days = self.default_expiry_warning_days
        
        df = self.excel_manager.get_all_commodities()
        
        if df.empty:
            return df
        
        today = datetime.now()
        warning_date = today + timedelta(days=warning_days)
        
        expiry_alerts = []
        
        for _, row in df.iterrows():
            try:
                production_date = pd.to_datetime(row['生产日期'])
                shelf_life = int(row['保质期(月)']) if pd.notna(row['保质期(月)']) else 0
                
                if shelf_life > 0:
                    expiry_date = production_date + pd.DateOffset(months=shelf_life)
                    days_until_expiry = (expiry_date - today).days
                    
                    if days_until_expiry <= warning_days:
                        alert_level = '紧急' if days_until_expiry <= 0 else '警告' if days_until_expiry <= 7 else '提醒'
                        
                        expiry_alerts.append({
                            '商品编号': row['商品编号'],
                            '商品名称': row['商品名称'],
                            '茶类': row['茶类'],
                            '品种': row['品种'],
                            '生产日期': row['生产日期'],
                            '保质期(月)': shelf_life,
                            '过期日期': expiry_date.strftime('%Y-%m-%d'),
                            '剩余天数': max(0, days_until_expiry),
                            '预警级别': alert_level,
                            '当前库存': row['当前库存']
                        })
            except (FileNotFoundError, PermissionError, ValueError, KeyError, OSError) as e:
                continue
        
        result_df = pd.DataFrame(expiry_alerts)
        
        if not result_df.empty:
            result_df = result_df.sort_values('剩余天数', ascending=True)
        
        return result_df
    
    def get_all_alerts(
        self,
        low_stock_threshold: Optional[float] = None,
        expiry_warning_days: Optional[int] = None
    ) -> Dict[str, pd.DataFrame]:
        """获取所有预警信息
        
        Args:
            low_stock_threshold: 库存阈值
            expiry_warning_days: 保质期预警天数
            
        Returns:
            包含库存预警和保质期预警的字典
        """
        return {
            'low_stock': self.check_low_stock(low_stock_threshold),
            'expiry': self.check_expiry(expiry_warning_days)
        }
    
    def get_alert_summary(
        self,
        low_stock_threshold: Optional[float] = None,
        expiry_warning_days: Optional[int] = None
    ) -> Dict:
        """获取预警摘要信息
        
        Args:
            low_stock_threshold: 库存阈值
            expiry_warning_days: 保质期预警天数
            
        Returns:
            预警摘要字典
        """
        alerts = self.get_all_alerts(low_stock_threshold, expiry_warning_days)
        
        low_stock_df = alerts['low_stock']
        expiry_df = alerts['expiry']
        
        summary = {
            'total_alerts': len(low_stock_df) + len(expiry_df),
            'low_stock_count': len(low_stock_df),
            'expiry_count': len(expiry_df),
            'low_stock_urgent': len(low_stock_df[low_stock_df['预警级别'] == '紧急']) if not low_stock_df.empty else 0,
            'expiry_urgent': len(expiry_df[expiry_df['预警级别'] == '紧急']) if not expiry_df.empty else 0,
            'has_alerts': (len(low_stock_df) + len(expiry_df)) > 0
        }
        
        return summary
    
    def get_low_stock_summary(self, threshold: Optional[float] = None) -> Dict:
        """获取库存预警摘要
        
        Args:
            threshold: 库存阈值
            
        Returns:
            库存预警摘要
        """
        low_stock_df = self.check_low_stock(threshold)
        
        if low_stock_df.empty:
            return {'count': 0, 'urgent': 0, 'warning': 0}
        
        return {
            'count': len(low_stock_df),
            'urgent': len(low_stock_df[low_stock_df['预警级别'] == '紧急']),
            'warning': len(low_stock_df[low_stock_df['预警级别'] == '警告'])
        }
    
    def get_expiry_summary(self, warning_days: Optional[int] = None) -> Dict:
        """获取保质期预警摘要
        
        Args:
            warning_days: 预警天数
            
        Returns:
            保质期预警摘要
        """
        expiry_df = self.check_expiry(warning_days)
        
        if expiry_df.empty:
            return {'count': 0, 'urgent': 0, 'warning': 0, 'reminder': 0}
        
        return {
            'count': len(expiry_df),
            'urgent': len(expiry_df[expiry_df['预警级别'] == '紧急']),
            'warning': len(expiry_df[expiry_df['预警级别'] == '警告']),
            'reminder': len(expiry_df[expiry_df['预警级别'] == '提醒'])
        }
    
    def set_low_stock_threshold(self, threshold: float) -> None:
        """设置默认库存预警阈值
        
        Args:
            threshold: 库存阈值
        """
        if threshold < 0:
            raise ValueError("库存阈值不能为负数")
        self.default_low_stock_threshold = threshold
    
    def set_expiry_warning_days(self, days: int) -> None:
        """设置默认保质期预警天数
        
        Args:
            days: 预警天数
        """
        if days < 1:
            raise ValueError("预警天数必须大于0")
        self.default_expiry_warning_days = days
    
    def get_category_low_stock(self, threshold: Optional[float] = None) -> pd.DataFrame:
        """按茶类统计库存预警
        
        Args:
            threshold: 库存阈值
            
        Returns:
            按茶类统计的DataFrame
        """
        low_stock_df = self.check_low_stock(threshold)
        
        if low_stock_df.empty:
            return pd.DataFrame(columns=['茶类', '商品数量', '预警级别'])
        
        category_stats = low_stock_df.groupby('茶类').agg({
            '商品编号': 'count',
            '预警级别': lambda x: ', '.join(x.unique())
        }).reset_index()
        
        category_stats.columns = ['茶类', '商品数量', '预警级别']
        category_stats = category_stats.sort_values('商品数量', ascending=False)
        
        return category_stats
