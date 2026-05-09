import pytest
import os
import pandas as pd
from operation_logger import OperationLogger


@pytest.fixture
def log_file(tmp_path):
    return str(tmp_path / "test_operation_logs.xlsx")


@pytest.fixture
def logger(log_file):
    lg = OperationLogger(log_file=log_file)
    yield lg
    if os.path.exists(log_file):
        os.remove(log_file)


class TestOperationLoggerInit:
    def test_creates_log_file(self, log_file):
        assert not os.path.exists(log_file)
        OperationLogger(log_file=log_file)
        assert os.path.exists(log_file)

    def test_default_log_level(self, logger):
        assert logger.log_level is not None

    def test_with_custom_log_level(self, log_file):
        lg = OperationLogger(log_file=log_file, log_level="DEBUG")
        from logging import DEBUG
        assert lg.log_level == DEBUG


class TestOperationLoggerSetLogLevel:
    def test_valid_level(self, logger):
        logger.set_log_level("DEBUG")
        from logging import DEBUG
        assert logger.log_level == DEBUG

    def test_invalid_level_keeps_current(self, logger):
        original = logger.log_level
        logger.set_log_level("INVALID")
        assert logger.log_level == original

    def test_case_insensitive(self, logger):
        logger.set_log_level("debug")
        from logging import DEBUG
        assert logger.log_level == DEBUG


class TestOperationLoggerLogOperation:
    def test_log_operation(self, logger):
        log_id = logger.log_operation(
            operation_type="新增",
            module="商品管理",
            details="测试添加商品"
        )
        assert log_id.startswith("L")

    def test_log_unknown_type_falls_back(self, logger):
        log_id = logger.log_operation(
            operation_type="未知类型",
            module="测试模块",
            details="测试"
        )
        df = logger.get_all_logs()
        assert len(df) == 1
        assert df.iloc[0]["操作类型"] == "其他"

    def test_log_with_data(self, logger):
        logger.log_operation(
            operation_type="新增",
            module="商品管理",
            details="添加商品",
            data='{"name": "测试"}'
        )
        df = logger.get_all_logs()
        assert len(df) == 1

    def test_log_custom_operator(self, logger):
        logger.log_operation(
            operation_type="修改",
            module="销售管理",
            details="修改销售记录",
            operator="张三"
        )
        df = logger.get_all_logs()
        assert df.iloc[0]["操作人"] == "张三"


class TestOperationLoggerGetLogs:
    def test_get_all_empty(self, logger):
        df = logger.get_all_logs()
        assert df.empty

    def test_get_all_after_logging(self, logger):
        logger.log_operation("新增", "商品管理", "添加商品")
        logger.log_operation("修改", "销售管理", "修改销售")
        df = logger.get_all_logs()
        assert len(df) == 2

    def test_filter_by_type(self, logger):
        logger.log_operation("新增", "商品管理", "添加商品")
        logger.log_operation("修改", "销售管理", "修改销售")
        df = logger.get_logs(operation_type="新增")
        assert len(df) == 1
        assert df.iloc[0]["操作类型"] == "新增"

    def test_filter_by_module(self, logger):
        logger.log_operation("新增", "商品管理", "添加商品")
        logger.log_operation("修改", "销售管理", "修改销售")
        df = logger.get_logs(module="商品管理")
        assert len(df) == 1

    def test_filter_by_date_range(self, logger):
        logger.log_operation("新增", "商品管理", "添加商品")
        df = logger.get_logs(start_date="2020-01-01", end_date="2099-12-31")
        assert len(df) == 1

    def test_limit_results(self, logger):
        for i in range(5):
            logger.log_operation("新增", "商品管理", f"操作{i}")
        df = logger.get_logs(limit=3)
        assert len(df) == 3

    def test_sorted_descending(self, logger):
        import time
        logger.log_operation("新增", "商品管理", "操作1")
        time.sleep(0.1)
        logger.log_operation("新增", "商品管理", "操作2")
        df = logger.get_all_logs()
        if len(df) >= 2:
            assert df.iloc[0]["操作时间"] >= df.iloc[1]["操作时间"]


class TestOperationLoggerRecentLogs:
    def test_get_recent_logs(self, logger):
        for i in range(10):
            logger.log_operation("新增", "商品管理", f"操作{i}")
        df = logger.get_recent_logs(5)
        assert len(df) == 5


class TestOperationLoggerModules:
    def test_get_modules(self, logger):
        logger.log_operation("新增", "商品管理", "添加商品")
        logger.log_operation("修改", "销售管理", "修改销售")
        modules = logger.get_modules()
        assert "商品管理" in modules
        assert "销售管理" in modules

    def test_get_modules_empty(self, logger):
        modules = logger.get_modules()
        assert modules == []


class TestOperationLoggerClearOldLogs:
    def test_clear_old_logs(self, logger):
        logger.log_operation("新增", "商品管理", "旧操作")
        deleted = logger.clear_old_logs(days_to_keep=365)
        assert deleted == 0

    def test_keep_recent_logs(self, logger):
        logger.log_operation("新增", "商品管理", "当前操作")
        deleted = logger.clear_old_logs(days_to_keep=365)
        df = logger.get_all_logs()
        assert len(df) == 1


class TestOperationLoggerExport:
    def test_export_logs(self, logger, tmp_path):
        logger.log_operation("新增", "商品管理", "添加商品")
        export_path = str(tmp_path / "exported_logs.xlsx")
        result = logger.export_logs(export_path)
        assert result is True
        assert os.path.exists(export_path)

    def test_export_with_dataframe(self, logger, tmp_path):
        logger.log_operation("新增", "商品管理", "添加商品")
        df = logger.get_all_logs()
        export_path = str(tmp_path / "exported_logs2.xlsx")
        result = logger.export_logs(export_path, logs_df=df)
        assert result is True
        assert os.path.exists(export_path)


class TestOperationLoggerTypes:
    def test_get_operation_types(self, logger):
        types = logger.get_operation_types()
        assert "新增" in types
        assert "修改" in types
        assert "删除" in types