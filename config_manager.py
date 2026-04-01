import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigManager:
    """配置文件管理器"""
    
    DEFAULT_CONFIG = {
        "app": {
            "name": "茶叶进销存管理系统",
            "version": "6.0",
            "language": "zh_CN"
        },
        "data": {
            "excel_file": "tea_inventory.xlsx",
            "backup_dir": "backups",
            "max_backups": 7,
            "log_file": "operation_logs.xlsx"
        },
        "alerts": {
            "low_stock_threshold": 1.0,
            "expiry_warning_days": 30,
            "check_on_startup": True
        },
        "ui": {
            "theme": "default",
            "window_width": 1200,
            "window_height": 800,
            "show_status_bar": True
        },
        "window_sizes": {},
        "export": {
            "default_format": "excel",
            "export_dir": "exports"
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            配置字典
        """
        if not os.path.exists(self.config_file):
            config = self.DEFAULT_CONFIG.copy()
            self._save_config(config)
            return config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            config = self._merge_config(self.DEFAULT_CONFIG, config)
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并默认配置和用户配置
        
        Args:
            default: 默认配置
            user: 用户配置
            
        Returns:
            合并后的配置
        """
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """保存配置文件
        
        Args:
            config: 要保存的配置，None则保存当前配置
            
        Returns:
            是否保存成功
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点号分隔（如 "alerts.low_stock_threshold"）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值
        
        Args:
            key: 配置键，支持点号分隔
            value: 配置值
            
        Returns:
            是否设置成功
        """
        keys = key.split('.')
        config = self.config
        
        try:
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
            return self._save_config()
        except Exception as e:
            print(f"设置配置失败: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置
        
        Returns:
            完整配置字典
        """
        return self.config.copy()
    
    def reset_to_default(self) -> bool:
        """重置为默认配置
        
        Returns:
            是否重置成功
        """
        self.config = self.DEFAULT_CONFIG.copy()
        return self._save_config()
    
    def reload(self) -> None:
        """重新加载配置文件"""
        self.config = self._load_config()
    
    def backup_config(self) -> str:
        """备份当前配置文件
        
        Returns:
            备份文件路径
        """
        if not os.path.exists(self.config_file):
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{self.config_file}.{timestamp}.bak"
        
        try:
            import shutil
            shutil.copy2(self.config_file, backup_file)
            return backup_file
        except Exception as e:
            print(f"备份配置文件失败: {e}")
            return ""
    
    def get_app_info(self) -> Dict[str, str]:
        """获取应用信息
        
        Returns:
            应用信息字典
        """
        return {
            'name': self.get('app.name', '茶叶进销存管理系统'),
            'version': self.get('app.version', '1.0'),
            'language': self.get('app.language', 'zh_CN')
        }
    
    def get_data_config(self) -> Dict[str, Any]:
        """获取数据相关配置
        
        Returns:
            数据配置字典
        """
        return {
            'excel_file': self.get('data.excel_file', 'tea_inventory.xlsx'),
            'backup_dir': self.get('data.backup_dir', 'backups'),
            'max_backups': self.get('data.max_backups', 7),
            'log_file': self.get('data.log_file', 'operation_logs.xlsx')
        }
    
    def get_alert_config(self) -> Dict[str, Any]:
        """获取预警相关配置
        
        Returns:
            预警配置字典
        """
        return {
            'low_stock_threshold': self.get('alerts.low_stock_threshold', 1.0),
            'expiry_warning_days': self.get('alerts.expiry_warning_days', 30),
            'check_on_startup': self.get('alerts.check_on_startup', True)
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """获取UI相关配置
        
        Returns:
            UI配置字典
        """
        return {
            'theme': self.get('ui.theme', 'default'),
            'window_width': self.get('ui.window_width', 1200),
            'window_height': self.get('ui.window_height', 800),
            'show_status_bar': self.get('ui.show_status_bar', True)
        }
    
    def get_export_config(self) -> Dict[str, Any]:
        """获取导出相关配置
        
        Returns:
            导出配置字典
        """
        return {
            'default_format': self.get('export.default_format', 'excel'),
            'export_dir': self.get('export.export_dir', 'exports')
        }
    
    def save_window_size(self, window_id: str, width: int, height: int) -> bool:
        """保存窗口大小
        
        Args:
            window_id: 窗口唯一标识符
            width: 窗口宽度
            height: 窗口高度
            
        Returns:
            是否保存成功
        """
        try:
            if 'window_sizes' not in self.config:
                self.config['window_sizes'] = {}
            self.config['window_sizes'][window_id] = {
                'width': width,
                'height': height
            }
            return self._save_config()
        except Exception as e:
            print(f"保存窗口大小失败: {e}")
            return False
    
    def load_window_size(self, window_id: str, default_width: int, default_height: int) -> tuple:
        """加载窗口大小
        
        Args:
            window_id: 窗口唯一标识符
            default_width: 默认宽度
            default_height: 默认高度
            
        Returns:
            (width, height) 元组
        """
        try:
            window_sizes = self.get('window_sizes', {})
            if window_id in window_sizes:
                size = window_sizes[window_id]
                return (size.get('width', default_width), size.get('height', default_height))
        except Exception as e:
            print(f"加载窗口大小失败: {e}")
        
        return (default_width, default_height)
    
    def reset_window_sizes(self) -> bool:
        """重置所有窗口大小为默认值
        
        Returns:
            是否重置成功
        """
        try:
            self.config['window_sizes'] = {}
            return self._save_config()
        except Exception as e:
            print(f"重置窗口大小失败: {e}")
            return False
