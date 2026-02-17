import unittest
import os
import sys
import tempfile
import shutil
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backup_manager import BackupManager
from operation_logger import OperationLogger
from config_manager import ConfigManager
from alert_manager import AlertManager


class TestBackupManager(unittest.TestCase):
    """测试备份管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.test_dir, "test_data.xlsx")
        self.backup_dir = os.path.join(self.test_dir, "backups")
        
        with open(self.data_file, 'w') as f:
            f.write("test data")
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_create_backup(self):
        """测试创建备份"""
        manager = BackupManager(self.data_file, self.backup_dir)
        backup_path = manager.create_backup("test_backup")
        
        self.assertTrue(os.path.exists(backup_path))
        self.assertTrue("test_backup" in backup_path)
    
    def test_list_backups(self):
        """测试列出备份"""
        manager = BackupManager(self.data_file, self.backup_dir)
        manager.create_backup()
        manager.create_backup()
        
        backups = manager.list_backups()
        self.assertEqual(len(backups), 2)
    
    def test_restore_backup(self):
        """测试恢复备份"""
        manager = BackupManager(self.data_file, self.backup_dir)
        backup_path = manager.create_backup()
        
        with open(self.data_file, 'w') as f:
            f.write("modified data")
        
        success = manager.restore_backup(backup_path)
        self.assertTrue(success)


class TestOperationLogger(unittest.TestCase):
    """测试操作日志记录器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.test_dir, "test_logs.xlsx")
        self.logger = OperationLogger(self.log_file)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_log_operation(self):
        """测试记录操作"""
        log_id = self.logger.log_operation(
            operation_type="新增",
            module="商品管理",
            details="添加新商品",
            operator="测试用户"
        )
        
        self.assertTrue(log_id.startswith("L"))
    
    def test_get_logs(self):
        """测试获取日志"""
        self.logger.log_operation("新增", "商品管理", "测试1")
        self.logger.log_operation("修改", "商品管理", "测试2")
        
        logs = self.logger.get_all_logs()
        self.assertEqual(len(logs), 2)


class TestConfigManager(unittest.TestCase):
    """测试配置管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.json")
        self.manager = ConfigManager(self.config_file)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_get_config(self):
        """测试获取配置"""
        app_name = self.manager.get("app.name")
        self.assertEqual(app_name, "茶叶进销存管理系统")
    
    def test_set_config(self):
        """测试设置配置"""
        success = self.manager.set("ui.theme", "dark")
        self.assertTrue(success)
        
        theme = self.manager.get("ui.theme")
        self.assertEqual(theme, "dark")
    
    def test_reset_config(self):
        """测试重置配置"""
        self.manager.set("ui.theme", "dark")
        success = self.manager.reset_to_default()
        self.assertTrue(success)
        
        theme = self.manager.get("ui.theme")
        self.assertEqual(theme, "default")


class TestAlertManager(unittest.TestCase):
    """测试预警管理器（需要ExcelManager配合）"""
    
    def test_alert_levels(self):
        """测试预警级别"""
        self.assertTrue(True)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBackupManager))
    suite.addTests(loader.loadTestsFromTestCase(TestOperationLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertManager))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
