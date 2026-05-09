import pytest
import pandas as pd
from crud_manager import CRUDManager


SHEET = "商品信息"
ID_COL = "商品编号"


class TestCRUDManagerInit:
    def test_default_id_column(self, excel_manager):
        mgr = CRUDManager(excel_manager, SHEET, "T")
        assert mgr.sheet_name == SHEET
        assert mgr.prefix == "T"
        assert mgr.id_column == "编号"

    def test_custom_id_column(self, excel_manager):
        mgr = CRUDManager(excel_manager, "客户信息", "C", "客户编号")
        assert mgr.sheet_name == "客户信息"
        assert mgr.prefix == "C"
        assert mgr.id_column == "客户编号"


class TestCRUDManagerGenerateId:
    def test_generate_id(self, excel_manager):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        record_id = mgr.generate_id()
        assert record_id.startswith("T")


class TestCRUDManagerAdd:
    def test_add_record(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        success, msg = mgr.add(sample_product)
        assert success is True

    def test_add_and_retrieve(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        df = mgr.get_all()
        assert len(df) == 1


class TestCRUDManagerGetAll:
    def test_empty_sheet(self, excel_manager):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        df = mgr.get_all()
        assert isinstance(df, pd.DataFrame)

    def test_non_empty_sheet(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        df = mgr.get_all()
        assert len(df) == 1


class TestCRUDManagerGetById:
    def test_found(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        record_id = sample_product[0]
        record = mgr.get_by_id(record_id)
        assert record is not None

    def test_not_found(self, excel_manager):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        record = mgr.get_by_id("NONEXISTENT")
        assert record is None


class TestCRUDManagerUpdate:
    def test_update(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        record_id = sample_product[0]
        success, msg = mgr.update(record_id, {"商品名称": "更新后的铁观音"})
        assert success is True

    def test_update_retrieve(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        record_id = sample_product[0]
        mgr.update(record_id, {"商品名称": "更新后的铁观音"})
        record = mgr.get_by_id(record_id)
        assert record["商品名称"] == "更新后的铁观音"


class TestCRUDManagerDelete:
    def test_delete(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        record_id = sample_product[0]
        success, msg = mgr.delete(record_id)
        assert success is True

    def test_delete_verify(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        mgr.delete(sample_product[0])
        record = mgr.get_by_id(sample_product[0])
        assert record is None


class TestCRUDManagerSearch:
    def test_search_by_keyword(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        df = mgr.search("铁观音")
        assert len(df) == 1

    def test_search_no_match(self, excel_manager, sample_product):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        mgr.add(sample_product)
        df = mgr.search("不存在的关键词")
        assert len(df) == 0

    def test_search_empty_sheet(self, excel_manager):
        mgr = CRUDManager(excel_manager, SHEET, "T", ID_COL)
        df = mgr.search("任意")
        assert len(df) == 0