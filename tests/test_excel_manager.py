import pandas as pd
import os


class TestExcelManagerInit:
    def test_creates_file(self, test_excel_file):
        from excel_manager import ExcelManager
        mgr = ExcelManager(filename=test_excel_file)
        assert os.path.exists(test_excel_file)

    def test_creates_sheets(self, excel_manager):
        df = excel_manager.read_sheet("商品信息")
        assert df is not None
        assert "商品编号" in df.columns


class TestExcelManagerCommodity:
    def test_add_commodity(self, excel_manager, sample_product):
        result = excel_manager.add_commodity(sample_product)
        assert result['success'] is True

    def test_get_commodity_by_id(self, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        commodity = excel_manager.get_commodity_by_id(sample_product[0])
        assert commodity is not None

    def test_get_commodity_not_found(self, excel_manager):
        commodity = excel_manager.get_commodity_by_id("T_NONEXISTENT")
        assert commodity is None

    def test_update_commodity(self, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        result = excel_manager.update_commodity(
            sample_product[0], {"商品名称": "铁观音升级版"}
        )
        assert result['success'] is True

    def test_delete_commodity(self, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        result = excel_manager.delete_commodity(sample_product[0])
        assert result['success'] is True

    def test_generate_unique_id(self, excel_manager):
        id1 = excel_manager.generate_id("T", "商品信息", "商品编号")
        id2 = excel_manager.generate_id("T", "商品信息", "商品编号")
        assert id1 != id2
        assert id1.startswith("T")


class TestExcelManagerCustomer:
    def test_add_customer(self, excel_manager, sample_customer):
        result = excel_manager.add_customer(sample_customer)
        assert result['success'] is True

    def test_get_all_customers(self, excel_manager, sample_customer):
        excel_manager.add_customer(sample_customer)
        customers = excel_manager.get_all_customers()
        assert len(customers) > 0