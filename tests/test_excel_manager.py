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


class TestExcelManagerFlush:
    """测试 flush() 方法不会写入重复表头"""

    def test_flush_does_not_write_duplicate_header_after_write_sheet(
        self, test_excel_file, sample_product
    ):
        from excel_manager import ExcelManager
        import pandas as pd

        mgr = ExcelManager(filename=test_excel_file)

        mgr.add_commodity(list(sample_product))

        updated_name = "铁观音升级版"
        result = mgr.update_commodity(sample_product[0], {"商品名称": updated_name})
        assert result['success'] is True

        mgr.flush()

        raw_df = pd.read_excel(test_excel_file, sheet_name="商品信息", engine='openpyxl')
        raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]

        first_header = raw_df.columns[0]
        for _, row in raw_df.iterrows():
            assert str(row[first_header]) != str(first_header), (
                f"发现重复表头行！第1列值为 '{row[first_header]}'，"
                f"与列名 '{first_header}' 相同。"
            )

        commodity = mgr.get_commodity_by_id(sample_product[0])
        assert commodity is not None
        assert commodity['商品名称'] == updated_name

        mgr.clear_cache()

    def test_flush_no_duplicate_header_with_multiple_operations(
        self, test_excel_file, sample_product
    ):
        from excel_manager import ExcelManager
        import pandas as pd

        mgr = ExcelManager(filename=test_excel_file)

        sample2 = list(sample_product)
        sample2[0] = "T202401010000009999"
        sample2[4] = "铁观音二号"

        mgr.add_commodity(list(sample_product))
        mgr.add_commodity(sample2)

        mgr.update_commodity(sample_product[0], {"零售价": 450.0})
        mgr.update_commodity(sample2[0], {"零售价": 500.0})

        mgr.flush()

        raw_df = pd.read_excel(test_excel_file, sheet_name="商品信息", engine='openpyxl')
        raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]

        first_header = raw_df.columns[0]
        for idx, row in raw_df.iterrows():
            assert str(row[first_header]) != str(first_header), (
                f"第 {idx} 行：发现重复表头行！值为 '{row[first_header]}'"
            )

        assert len(raw_df) == 2, f"预期 2 条记录，实际 {len(raw_df)} 条"

        mgr.clear_cache()

    def test_flush_no_duplicate_header_across_sheets(
        self, test_excel_file, sample_product, sample_customer
    ):
        from excel_manager import ExcelManager
        import pandas as pd

        mgr = ExcelManager(filename=test_excel_file)
        mgr.add_commodity(list(sample_product))
        mgr.add_customer(list(sample_customer))

        mgr.update_commodity(sample_product[0], {"商品名称": "更新名称"})
        mgr.update_customer(
            sample_customer[0], {"客户名称": "更新客户名"}
        )
        mgr.flush()

        for sheet_name in ["商品信息", "客户信息"]:
            raw_df = pd.read_excel(test_excel_file, sheet_name=sheet_name, engine='openpyxl')
            raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]
            if raw_df.empty:
                continue
            first_header = raw_df.columns[0]
            for idx, row in raw_df.iterrows():
                assert str(row[first_header]) != str(first_header), (
                    f"工作表 '{sheet_name}' 第 {idx} 行发现重复表头！"
                )

        mgr.clear_cache()


class TestExcelManagerCustomer:
    def test_add_customer(self, excel_manager, sample_customer):
        result = excel_manager.add_customer(sample_customer)
        assert result['success'] is True

    def test_get_all_customers(self, excel_manager, sample_customer):
        excel_manager.add_customer(sample_customer)
        customers = excel_manager.get_all_customers()
        assert len(customers) > 0