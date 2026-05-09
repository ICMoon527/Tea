import pytest
import os
from backup_manager import BackupManager


@pytest.fixture
def data_file(tmp_path):
    return str(tmp_path / "tea_inventory.xlsx")


@pytest.fixture
def backup_dir(tmp_path):
    return str(tmp_path / "backups")


@pytest.fixture
def backup_manager(data_file, backup_dir):
    from excel_manager import ExcelManager
    mgr = ExcelManager(filename=data_file)
    bm = BackupManager(data_file=data_file, backup_dir=backup_dir)
    yield bm


class TestBackupManagerInit:
    def test_creates_backup_dir(self, tmp_path):
        bd = str(tmp_path / "new_backups")
        BackupManager(data_file=str(tmp_path / "dummy.xlsx"), backup_dir=bd)
        assert os.path.exists(bd)

    def test_default_values(self, backup_manager):
        assert backup_manager.max_backups == 7


class TestBackupManagerCreateBackup:
    def test_create_without_description(self, backup_manager):
        path = backup_manager.create_backup()
        assert os.path.exists(path)
        assert "tea_inventory_backup_" in os.path.basename(path)

    def test_create_with_description(self, backup_manager):
        path = backup_manager.create_backup(description="测试备份")
        assert os.path.exists(path)
        assert "测试备份" in os.path.basename(path)

    def test_raises_on_missing_file(self, tmp_path):
        bm = BackupManager(
            data_file=str(tmp_path / "nonexistent.xlsx"),
            backup_dir=str(tmp_path / "backups")
        )
        with pytest.raises(FileNotFoundError):
            bm.create_backup()


class TestBackupManagerListBackups:
    def test_empty_initially(self, backup_manager):
        backups = backup_manager.list_backups()
        assert isinstance(backups, list)

    def test_lists_after_create(self, backup_manager):
        backup_manager.create_backup()
        backups = backup_manager.list_backups()
        assert len(backups) == 1
        assert "filename" in backups[0]
        assert "size" in backups[0]
        assert "created_time" in backups[0]
        assert "size_formatted" in backups[0]

    def test_sorted_by_time(self, backup_manager):
        import time
        backup_manager.create_backup(description="first")
        time.sleep(0.1)
        backup_manager.create_backup(description="second")
        backups = backup_manager.list_backups()
        assert len(backups) >= 2
        assert backups[0]["created_time"] >= backups[-1]["created_time"]


class TestBackupManagerRestore:
    def test_restore_success(self, backup_manager):
        path = backup_manager.create_backup(description="预恢复")
        result = backup_manager.restore_backup(path)
        assert result is True

    def test_restore_nonexistent_file(self, backup_manager, tmp_path):
        with pytest.raises(FileNotFoundError):
            backup_manager.restore_backup(str(tmp_path / "nonexistent.xlsx"))


class TestBackupManagerDelete:
    def test_delete_existing(self, backup_manager):
        path = backup_manager.create_backup()
        assert os.path.exists(path)
        result = backup_manager.delete_backup(path)
        assert result is True
        assert not os.path.exists(path)

    def test_delete_nonexistent(self, backup_manager, tmp_path):
        result = backup_manager.delete_backup(str(tmp_path / "nonexistent.xlsx"))
        assert result is False


class TestBackupManagerFormatSize:
    def test_bytes(self, backup_manager):
        assert "B" in backup_manager._format_size(500)

    def test_kb(self, backup_manager):
        assert "KB" in backup_manager._format_size(2048)

    def test_mb(self, backup_manager):
        assert "MB" in backup_manager._format_size(2 * 1024 * 1024)


class TestBackupManagerSetMaxBackups:
    def test_valid_value(self, backup_manager):
        backup_manager.set_max_backups(3)
        assert backup_manager.max_backups == 3

    def test_invalid_value(self, backup_manager):
        with pytest.raises(ValueError):
            backup_manager.set_max_backups(0)

    def test_invalid_value_negative(self, backup_manager):
        with pytest.raises(ValueError):
            backup_manager.set_max_backups(-1)


class TestBackupManagerCleanup:
    def test_cleanup_removes_old(self, backup_manager):
        backup_manager.set_max_backups(2)
        for i in range(5):
            import time
            backup_manager.create_backup(description=f"backup_{i}")
            time.sleep(0.01)
        backups = backup_manager.list_backups()
        assert len(backups) <= 2