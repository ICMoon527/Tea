import pytest
import os
import json
from config_manager import ConfigManager


@pytest.fixture
def config_file(tmp_path):
    return str(tmp_path / "test_config.json")


@pytest.fixture
def config_manager(config_file):
    mgr = ConfigManager(config_file=config_file)
    yield mgr
    if os.path.exists(config_file):
        os.remove(config_file)


class TestConfigManagerInit:
    def test_creates_default_config(self, config_file):
        assert not os.path.exists(config_file)
        mgr = ConfigManager(config_file=config_file)
        assert os.path.exists(config_file)

    def test_loads_defaults(self, config_manager):
        assert config_manager.get("app.name") == "茶叶进销存管理系统"
        assert config_manager.get("app.version") == "6.0"


class TestConfigManagerGet:
    def test_top_level_key(self, config_manager):
        assert isinstance(config_manager.get("app"), dict)
        assert config_manager.get("app")["name"] == "茶叶进销存管理系统"

    def test_nested_key(self, config_manager):
        assert config_manager.get("alerts.low_stock_threshold") == 1.0

    def test_nonexistent_key_with_default(self, config_manager):
        assert config_manager.get("nonexistent.key", "default") == "default"

    def test_nonexistent_key_no_default(self, config_manager):
        assert config_manager.get("nonexistent.key") is None


class TestConfigManagerSet:
    def test_set_top_level(self, config_manager):
        assert config_manager.set("new_key", "new_value")
        assert config_manager.get("new_key") == "new_value"

    def test_set_nested(self, config_manager):
        assert config_manager.set("alerts.low_stock_threshold", 5.0)
        assert config_manager.get("alerts.low_stock_threshold") == 5.0

    def test_persists_to_file(self, config_file):
        mgr = ConfigManager(config_file=config_file)
        mgr.set("app.name", "新名称")
        mgr2 = ConfigManager(config_file=config_file)
        assert mgr2.get("app.name") == "新名称"


class TestConfigManagerGetAll:
    def test_returns_copy(self, config_manager):
        all_config = config_manager.get_all()
        all_config["modified"] = True
        assert "modified" not in config_manager.get_all()


class TestConfigManagerReset:
    def test_reset_to_default(self, tmp_path):
        config_file = str(tmp_path / "reset_test.json")
        mgr = ConfigManager(config_file=config_file)
        mgr.set("app.name", "修改过的名称")
        assert mgr.get("app.name") == "修改过的名称"
        success = mgr.reset_to_default()
        assert success
        assert mgr.get("app.name") == "茶叶进销存管理系统"


class TestConfigManagerReload:
    def test_reload_from_disk(self, tmp_path):
        config_file = str(tmp_path / "reload_test.json")
        mgr = ConfigManager(config_file=config_file)
        mgr.set("app.name", "旧名称")
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["app"]["name"] = "直接修改的名称"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        assert mgr.get("app.name") == "旧名称"
        mgr.reload()
        assert mgr.get("app.name") == "直接修改的名称"


class TestConfigManagerWindowSize:
    def test_save_and_load(self, config_manager):
        config_manager.save_window_size("test_window", 800, 600)
        w, h = config_manager.load_window_size("test_window", 1024, 768)
        assert w == 800
        assert h == 600

    def test_load_nonexistent_returns_default(self, config_manager):
        w, h = config_manager.load_window_size("nonexistent", 1024, 768)
        assert w == 1024
        assert h == 768

    def test_reset_window_sizes(self, config_manager):
        config_manager.save_window_size("win1", 100, 200)
        config_manager.reset_window_sizes()
        w, h = config_manager.load_window_size("win1", 500, 500)
        assert w == 500
        assert h == 500


class TestConfigManagerBackup:
    def test_backup_creates_file(self, config_manager, config_file):
        backup_path = config_manager.backup_config()
        assert backup_path != ""
        assert os.path.exists(backup_path)
        assert backup_path.endswith(".bak")


class TestConfigManagerHelperMethods:
    def test_get_app_info(self, tmp_path):
        mgr = ConfigManager(config_file=str(tmp_path / "helper_test.json"))
        info = mgr.get_app_info()
        assert info["name"] == "茶叶进销存管理系统"
        assert info["version"] == "6.0"

    def test_get_data_config(self, config_manager):
        data = config_manager.get_data_config()
        assert "excel_file" in data
        assert "backup_dir" in data

    def test_get_alert_config(self, tmp_path):
        mgr = ConfigManager(config_file=str(tmp_path / "alert_test.json"))
        alerts = mgr.get_alert_config()
        assert alerts["low_stock_threshold"] == 1.0

    def test_get_ui_config(self, config_manager):
        ui = config_manager.get_ui_config()
        assert ui["window_width"] == 1200

    def test_get_export_config(self, config_manager):
        export = config_manager.get_export_config()
        assert export["default_format"] == "excel"