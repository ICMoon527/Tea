import os
import shutil
from datetime import datetime
from typing import List, Optional
import pandas as pd
from logger import get_logger


class BackupManager:
    """数据备份与恢复管理器"""
    
    def __init__(self, data_file: str = "tea_inventory.xlsx", backup_dir: str = "backups"):
        self.logger = get_logger()
        self.data_file = data_file
        self.backup_dir = backup_dir
        self.max_backups = 7
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, description: str = "") -> str:
        """创建数据备份
        
        Args:
            description: 备份描述信息
            
        Returns:
            备份文件路径
        """
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"数据文件 {self.data_file} 不存在")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if description:
            backup_filename = f"tea_inventory_backup_{timestamp}_{description}.xlsx"
        else:
            backup_filename = f"tea_inventory_backup_{timestamp}.xlsx"
        
        backup_path = os.path.join(self.backup_dir, backup_filename)
        shutil.copy2(self.data_file, backup_path)
        
        self._cleanup_old_backups()
        
        return backup_path
    
    def _cleanup_old_backups(self) -> None:
        """清理旧的备份文件，保留最近max_backups个"""
        backup_files = self.list_backups()
        
        if len(backup_files) > self.max_backups:
            files_to_delete = backup_files[self.max_backups:]
            for file_info in files_to_delete:
                try:
                    os.remove(file_info['path'])
                except (FileNotFoundError, PermissionError, OSError) as e:
                    self.logger.error(f"删除旧备份文件失败: {e}")
    
    def list_backups(self) -> List[dict]:
        """列出所有可用的备份文件
        
        Returns:
            备份文件信息列表，按时间倒序排列
        """
        backup_files = []
        
        if not os.path.exists(self.backup_dir):
            return backup_files
        
        for filename in os.listdir(self.backup_dir):
            if filename.startswith("tea_inventory_backup_") and filename.endswith(".xlsx"):
                file_path = os.path.join(self.backup_dir, filename)
                file_stat = os.stat(file_path)
                
                backup_files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': file_stat.st_size,
                    'created_time': datetime.fromtimestamp(file_stat.st_mtime),
                    'size_formatted': self._format_size(file_stat.st_size)
                })
        
        backup_files.sort(key=lambda x: x['created_time'], reverse=True)
        return backup_files
    
    def restore_backup(self, backup_path: str) -> bool:
        """从备份恢复数据
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否恢复成功
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"备份文件 {backup_path} 不存在")
        
        try:
            if os.path.exists(self.data_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                pre_restore_backup = os.path.join(self.backup_dir, f"pre_restore_backup_{timestamp}.xlsx")
                shutil.copy2(self.data_file, pre_restore_backup)
            
            shutil.copy2(backup_path, self.data_file)
            return True
        except (FileNotFoundError, PermissionError, OSError) as e:
            self.logger.error(f"恢复备份失败: {e}")
            return False
    
    def delete_backup(self, backup_path: str) -> bool:
        """删除指定的备份文件
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否删除成功
        """
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
                return True
            return False
        except (FileNotFoundError, PermissionError, OSError) as e:
            self.logger.error(f"删除备份失败: {e}")
            return False
    
    def get_backup_info(self, backup_path: str) -> Optional[dict]:
        """获取备份文件的详细信息
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            备份文件信息字典
        """
        if not os.path.exists(backup_path):
            return None
        
        try:
            file_stat = os.stat(backup_path)
            return {
                'filename': os.path.basename(backup_path),
                'path': backup_path,
                'size': file_stat.st_size,
                'size_formatted': self._format_size(file_stat.st_size),
                'created_time': datetime.fromtimestamp(file_stat.st_mtime),
                'modified_time': datetime.fromtimestamp(file_stat.st_mtime)
            }
        except (FileNotFoundError, PermissionError, OSError) as e:
            self.logger.error(f"获取备份信息失败: {e}")
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            格式化后的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def get_total_backup_size(self) -> int:
        """获取所有备份文件的总大小
        
        Returns:
            总大小（字节）
        """
        total_size = 0
        backup_files = self.list_backups()
        for file_info in backup_files:
            total_size += file_info['size']
        return total_size
    
    def set_max_backups(self, max_backups: int) -> None:
        """设置最大保留备份数量
        
        Args:
            max_backups: 最大备份数量
        """
        if max_backups < 1:
            raise ValueError("最大备份数量必须大于等于1")
        self.max_backups = max_backups
        self._cleanup_old_backups()
