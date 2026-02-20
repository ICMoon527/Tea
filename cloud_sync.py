import os
import json
import shutil
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    print("警告: paramiko 库未安装，SFTP 功能不可用")


class CloudSyncManager:
    """云端数据同步管理器 - SFTP 版本
    
    通过 SFTP/SSH 协议直接连接到远程服务器进行数据同步
    """
    
    def __init__(self, config_file: str = "cloud_sync_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.ssh_client = None
        self.sftp_client = None
    
    def _load_config(self) -> Dict[str, Any]:
        """加载同步配置"""
        default_config = {
            "enabled": False,
            "server": {
                "host": "",
                "port": 22,
                "username": "",
                "password": "",
                "remote_path": ""
            },
            "device_id": self._generate_device_id(),
            "last_sync_time": None,
            "auto_sync": False,
            "sync_interval_minutes": 60,
            "data_version": 0
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    config = default_config.copy()
                    self._deep_update(config, loaded_config)
                    return config
            except Exception as e:
                print(f"加载同步配置失败: {e}")
                return default_config
        
        return default_config
    
    def _deep_update(self, target: Dict, source: Dict) -> None:
        """深度更新字典"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def _save_config(self) -> bool:
        """保存同步配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存同步配置失败: {e}")
            return False
    
    def _generate_device_id(self) -> str:
        """生成设备唯一标识"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"计算文件哈希失败: {e}")
            return ""
    
    def is_enabled(self) -> bool:
        """检查云同步是否已启用"""
        if not PARAMIKO_AVAILABLE:
            return False
        server_config = self.config.get("server", {})
        return (
            self.config.get("enabled", False) and
            server_config.get("host", "") and
            server_config.get("username", "")
        )
    
    def set_server_config(self, host: str, port: int, username: str, 
                         password: str, remote_path: str) -> bool:
        """设置服务器配置"""
        if not PARAMIKO_AVAILABLE:
            print("错误: paramiko 库未安装")
            return False
        
        self.config["server"] = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "remote_path": remote_path
        }
        self.config["enabled"] = True
        return self._save_config()
    
    def disable_sync(self) -> bool:
        """禁用云同步"""
        self.config["enabled"] = False
        self._disconnect()
        return self._save_config()
    
    def get_sync_status(self) -> Dict[str, Any]:
        """获取同步状态信息"""
        server_config = self.config.get("server", {})
        return {
            "enabled": self.is_enabled(),
            "paramiko_available": PARAMIKO_AVAILABLE,
            "host": server_config.get("host", ""),
            "port": server_config.get("port", 22),
            "username": server_config.get("username", ""),
            "remote_path": server_config.get("remote_path", ""),
            "device_id": self.config.get("device_id", ""),
            "last_sync_time": self.config.get("last_sync_time"),
            "auto_sync": self.config.get("auto_sync", False),
            "data_version": self.config.get("data_version", 0),
            "connected": self.ssh_client is not None and self.ssh_client.get_transport() and self.ssh_client.get_transport().is_active()
        }
    
    def _connect(self) -> bool:
        """建立 SFTP 连接"""
        if not PARAMIKO_AVAILABLE:
            return False
        
        if self.ssh_client and self.ssh_client.get_transport() and self.ssh_client.get_transport().is_active():
            return True
        
        try:
            server_config = self.config.get("server", {})
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.ssh_client.connect(
                hostname=server_config.get("host"),
                port=server_config.get("port", 22),
                username=server_config.get("username"),
                password=server_config.get("password"),
                timeout=30
            )
            
            self.sftp_client = self.ssh_client.open_sftp()
            return True
            
        except Exception as e:
            print(f"连接服务器失败: {e}")
            self._disconnect()
            return False
    
    def _disconnect(self) -> None:
        """断开 SFTP 连接"""
        try:
            if self.sftp_client:
                self.sftp_client.close()
                self.sftp_client = None
        except:
            pass
        
        try:
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
        except:
            pass
    
    def _ensure_remote_path_exists(self) -> bool:
        """确保远程路径存在"""
        if not self._connect():
            return False
        
        try:
            remote_path = self.config.get("server", {}).get("remote_path", "")
            if not remote_path:
                return False
            
            try:
                self.sftp_client.stat(remote_path)
            except FileNotFoundError:
                try:
                    self.sftp_client.mkdir(remote_path)
                except Exception as e:
                    print(f"创建远程目录失败: {e}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"检查远程路径失败: {e}")
            return False
    
    def upload_to_cloud(self, data_files: List[str]) -> Dict[str, Any]:
        """上传数据到云端
        
        Args:
            data_files: 需要同步的数据文件列表
            
        Returns:
            同步结果信息
        """
        result = {
            "success": False,
            "message": "",
            "version": 0,
            "uploaded_files": []
        }
        
        if not self.is_enabled():
            result["message"] = "云同步未启用，请先配置服务器连接"
            return result
        
        try:
            if not self._connect():
                result["message"] = "无法连接到服务器"
                return result
            
            if not self._ensure_remote_path_exists():
                result["message"] = "远程目录不存在且无法创建"
                return result
            
            remote_path = self.config.get("server", {}).get("remote_path", "")
            uploaded_files = []
            
            for local_file in data_files:
                if os.path.exists(local_file):
                    try:
                        file_name = os.path.basename(local_file)
                        remote_file = os.path.join(remote_path, file_name)
                        
                        self.sftp_client.put(local_file, remote_file)
                        uploaded_files.append(file_name)
                        print(f"成功上传: {file_name}")
                    except Exception as e:
                        print(f"上传文件 {local_file} 失败: {e}")
            
            if uploaded_files:
                self.config["data_version"] = self.config.get("data_version", 0) + 1
                self.config["last_sync_time"] = datetime.now().isoformat()
                self._save_config()
                
                result["success"] = True
                result["message"] = f"成功上传 {len(uploaded_files)} 个文件到云端"
                result["version"] = self.config["data_version"]
                result["uploaded_files"] = uploaded_files
            else:
                result["message"] = "没有找到可上传的文件"
            
        except Exception as e:
            result["message"] = f"同步失败: {str(e)}"
        finally:
            self._disconnect()
        
        return result
    
    def list_cloud_packages(self) -> List[Dict[str, Any]]:
        """列出所有云端文件"""
        if not self.is_enabled():
            return []
        
        packages = []
        
        try:
            if not self._connect():
                return []
            
            remote_path = self.config.get("server", {}).get("remote_path", "")
            
            try:
                files = self.sftp_client.listdir_attr(remote_path)
                
                for file_attr in files:
                    if file_attr.filename.endswith(('.xlsx', '.json')):
                        packages.append({
                            'filename': file_attr.filename,
                            'size': file_attr.st_size,
                            'size_formatted': self._format_size(file_attr.st_size),
                            'modified_time': datetime.fromtimestamp(file_attr.st_mtime),
                            'modified_time_str': datetime.fromtimestamp(file_attr.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        })
                
                packages.sort(key=lambda x: x['modified_time'], reverse=True)
                
            except Exception as e:
                print(f"列出远程文件失败: {e}")
            
        except Exception as e:
            print(f"获取云端文件列表失败: {e}")
        finally:
            self._disconnect()
        
        return packages
    
    def download_from_cloud(self, target_dir: str = ".") -> Dict[str, Any]:
        """从云端下载数据
        
        Args:
            target_dir: 目标恢复目录
            
        Returns:
            下载结果信息
        """
        result = {
            "success": False,
            "message": "",
            "version": 0,
            "restored_files": []
        }
        
        if not self.is_enabled():
            result["message"] = "云同步未启用，请先配置服务器连接"
            return result
        
        try:
            if not self._connect():
                result["message"] = "无法连接到服务器"
                return result
            
            remote_path = self.config.get("server", {}).get("remote_path", "")
            restored_files = []
            
            try:
                files = self.sftp_client.listdir(remote_path)
                
                for file_name in files:
                    if file_name.endswith(('.xlsx', '.json')):
                        try:
                            local_file = os.path.join(target_dir, file_name)
                            remote_file = os.path.join(remote_path, file_name)
                            
                            if os.path.exists(local_file):
                                backup_dir = os.path.join(target_dir, 'backups')
                                os.makedirs(backup_dir, exist_ok=True)
                                backup_file = f"{backup_dir}/{file_name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                                shutil.copy2(local_file, backup_file)
                            
                            self.sftp_client.get(remote_file, local_file)
                            restored_files.append(file_name)
                            print(f"成功下载: {file_name}")
                        except Exception as e:
                            print(f"下载文件 {file_name} 失败: {e}")
                
                if restored_files:
                    self.config["last_sync_time"] = datetime.now().isoformat()
                    self._save_config()
                    
                    result["success"] = True
                    result["message"] = f"成功从云端恢复 {len(restored_files)} 个文件"
                    result["restored_files"] = restored_files
                else:
                    result["message"] = "云端没有找到数据文件"
            
            except Exception as e:
                result["message"] = f"访问远程目录失败: {e}"
            
        except Exception as e:
            result["message"] = f"恢复数据失败: {str(e)}"
        finally:
            self._disconnect()
        
        return result
    
    def force_restore(self, target_dir: str = ".") -> Dict[str, Any]:
        """强制从云端恢复数据（与 download_from_cloud 相同，保持接口兼容）"""
        return self.download_from_cloud(target_dir)
    
    def test_connection(self) -> Dict[str, Any]:
        """测试服务器连接"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not PARAMIKO_AVAILABLE:
            result["message"] = "paramiko 库未安装，请运行: pip install paramiko"
            return result
        
        try:
            if self._connect():
                result["success"] = True
                result["message"] = "服务器连接成功！"
                self._disconnect()
            else:
                result["message"] = "服务器连接失败"
        except Exception as e:
            result["message"] = f"连接测试失败: {str(e)}"
        finally:
            self._disconnect()
        
        return result
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def set_auto_sync(self, enabled: bool, interval_minutes: int = 60) -> bool:
        """设置自动同步"""
        self.config["auto_sync"] = enabled
        self.config["sync_interval_minutes"] = interval_minutes
        return self._save_config()

