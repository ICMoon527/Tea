import os
from datetime import datetime
from typing import List, Optional, Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class OperationLogger:
    """操作日志记录器"""

    LOG_FILE = "operation_logs.xlsx"

    LOG_COLUMNS = [
        "日志编号",
        "操作时间",
        "操作类型",
        "操作模块",
        "操作详情",
        "操作数据",
        "操作人"
    ]

    OPERATION_TYPES = [
        "新增",
        "修改",
        "删除",
        "查询",
        "导入",
        "导出",
        "备份",
        "恢复",
        "其他"
    ]

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, log_file: str = None, log_level: str = "INFO"):
        self.log_file = log_file or self.LOG_FILE
        self.log_level = self.LOG_LEVELS.get(log_level.upper(), logging.INFO)
        self._init_log_file()

    def set_log_level(self, level: str):
        """设置日志级别

        Args:
            level: 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        """
        if level.upper() in self.LOG_LEVELS:
            self.log_level = self.LOG_LEVELS[level.upper()]
        else:
            logger.warning(f"未知的日志级别: {level}，保持当前级别")
    
    def _init_log_file(self) -> None:
        """初始化日志文件"""
        if not os.path.exists(self.log_file):
            df = pd.DataFrame(columns=self.LOG_COLUMNS)
            df.to_excel(self.log_file, index=False, engine='openpyxl')
    
    def log_operation(
        self,
        operation_type: str,
        module: str,
        details: str,
        data: Optional[str] = None,
        operator: str = "系统"
    ) -> str:
        """记录操作日志
        
        Args:
            operation_type: 操作类型（新增/修改/删除等）
            module: 操作模块（商品管理/销售管理等）
            details: 操作详情描述
            data: 操作相关数据（JSON字符串）
            operator: 操作人
            
        Returns:
            日志编号
        """
        log_id = self._generate_log_id()
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if operation_type not in self.OPERATION_TYPES:
            operation_type = "其他"
        
        log_data = {
            "日志编号": log_id,
            "操作时间": log_time,
            "操作类型": operation_type,
            "操作模块": module,
            "操作详情": details,
            "操作数据": data or "",
            "操作人": operator
        }
        
        try:
            df = pd.read_excel(self.log_file, engine='openpyxl')
            new_row = pd.DataFrame([log_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_excel(self.log_file, index=False, engine='openpyxl')
        except Exception as e:
            logger.error(f"记录日志失败: {e}")
        
        return log_id
    
    def _generate_log_id(self) -> str:
        """生成日志编号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        import random
        random_part = f"{random.randint(1000, 9999)}"
        return f"L{timestamp}{random_part}"
    
    def get_logs(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        operation_type: Optional[str] = None,
        module: Optional[str] = None,
        limit: int = 100
    ) -> pd.DataFrame:
        """查询操作日志
        
        Args:
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            operation_type: 操作类型过滤
            module: 操作模块过滤
            limit: 返回记录数量限制
            
        Returns:
            日志DataFrame
        """
        try:
            df = pd.read_excel(self.log_file, engine='openpyxl')
            
            if df.empty:
                return df
            
            if start_date:
                df = df[df['操作时间'] >= start_date]
            
            if end_date:
                df = df[df['操作时间'] <= end_date + " 23:59:59"]
            
            if operation_type:
                df = df[df['操作类型'] == operation_type]
            
            if module:
                df = df[df['操作模块'] == module]
            
            df = df.sort_values('操作时间', ascending=False)
            
            if limit > 0:
                df = df.head(limit)
            
            return df
        except Exception as e:
            logger.error(f"查询日志失败: {e}")
            return pd.DataFrame(columns=self.LOG_COLUMNS)

    def get_all_logs(self) -> pd.DataFrame:
        """获取所有操作日志
        
        Returns:
            所有日志DataFrame
        """
        try:
            df = pd.read_excel(self.log_file, engine='openpyxl')
            df = df.sort_values('操作时间', ascending=False)
            return df
        except Exception as e:
            logger.error(f"获取日志失败: {e}")
            return pd.DataFrame(columns=self.LOG_COLUMNS)
    
    def get_recent_logs(self, count: int = 50) -> pd.DataFrame:
        """获取最近的操作日志
        
        Args:
            count: 返回记录数量
            
        Returns:
            最近的日志DataFrame
        """
        df = self.get_all_logs()
        return df.head(count) if not df.empty else df
    
    def get_operation_types(self) -> List[str]:
        """获取所有操作类型
        
        Returns:
            操作类型列表
        """
        return self.OPERATION_TYPES.copy()
    
    def get_modules(self) -> List[str]:
        """获取所有操作模块
        
        Returns:
            操作模块列表
        """
        try:
            df = pd.read_excel(self.log_file, engine='openpyxl')
            if not df.empty and '操作模块' in df.columns:
                return sorted(df['操作模块'].unique().tolist())
            return []
        except Exception as e:
            logger.error(f"获取模块列表失败: {e}")
            return []
    
    def clear_old_logs(self, days_to_keep: int = 30) -> int:
        """清理旧的操作日志
        
        Args:
            days_to_keep: 保留天数
            
        Returns:
            删除的日志数量
        """
        try:
            df = pd.read_excel(self.log_file, engine='openpyxl')
            
            if df.empty:
                return 0
            
            cutoff_date = datetime.now() - pd.Timedelta(days=days_to_keep)
            df['操作时间_dt'] = pd.to_datetime(df['操作时间'])
            df_filtered = df[df['操作时间_dt'] >= cutoff_date]
            df_filtered = df_filtered.drop(columns=['操作时间_dt'])
            
            deleted_count = len(df) - len(df_filtered)
            
            if deleted_count > 0:
                df_filtered.to_excel(self.log_file, index=False, engine='openpyxl')
            
            return deleted_count
        except Exception as e:
            logger.error(f"清理旧日志失败: {e}")
            return 0
    
    def export_logs(self, export_path: str, logs_df: Optional[pd.DataFrame] = None) -> bool:
        """导出操作日志
        
        Args:
            export_path: 导出文件路径
            logs_df: 要导出的日志DataFrame，None则导出所有
            
        Returns:
            是否导出成功
        """
        try:
            if logs_df is None:
                logs_df = self.get_all_logs()
            
            logs_df.to_excel(export_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            logger.error(f"导出日志失败: {e}")
            return False
