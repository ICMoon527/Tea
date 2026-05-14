import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from excel_manager import ExcelManager
from shopping_cart import ShoppingCart


@pytest.fixture
def test_excel_file(tmp_path):
    file_path = tmp_path / "test_inventory.xlsx"
    return str(file_path)


@pytest.fixture
def excel_manager(test_excel_file):
    mgr = ExcelManager(filename=test_excel_file)
    yield mgr
    mgr.clear_cache()


@pytest.fixture
def shopping_cart(excel_manager):
    return ShoppingCart(excel_manager)


@pytest.fixture
def sample_product():
    return [
        "T202401010000001234", "乌龙茶", "铁观音", "测试公司", "福建",
        "铁观音一级", "500g", 200.0, 400.0, "2024-01-01",
        24, 100.0, "香气浓郁", 2024, "一级", "斤"
    ]


@pytest.fixture
def sample_customer():
    return [
        "C202401010000001234", "测试客户", "13800000000",
        "test@test.com", "测试地址", 0.0, 0, None, "普通", "", "2024-01-01"
    ]