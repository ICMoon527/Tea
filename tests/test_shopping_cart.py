import pytest


class TestShoppingCart:
    def test_add_item(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        result = shopping_cart.add_item(sample_product[0], 5, "斤")
        assert result['success'] is True
        assert len(shopping_cart.get_items()) == 1

    def test_add_item_insufficient_stock(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        result = shopping_cart.add_item(sample_product[0], 200, "斤")
        assert result['success'] is False

    def test_add_item_not_found(self, shopping_cart):
        result = shopping_cart.add_item("NONEXISTENT", 1, "斤")
        assert result['success'] is False

    def test_update_existing_item(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 5, "斤")
        result = shopping_cart.add_item(sample_product[0], 10, "斤")
        assert result['success'] is True
        assert len(shopping_cart.get_items()) == 1

    def test_remove_item(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 5, "斤")
        assert shopping_cart.remove_item(sample_product[0]) is True
        assert shopping_cart.is_empty()

    def test_remove_nonexistent(self, shopping_cart):
        assert shopping_cart.remove_item("NONEXISTENT") is False

    def test_clear_cart(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 5, "斤")
        shopping_cart.clear()
        assert shopping_cart.is_empty()

    def test_get_total_amount(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 2, "斤")
        assert shopping_cart.get_total_amount() == 800.0

    def test_get_total_cost(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 2, "斤")
        assert shopping_cart.get_total_cost() == 400.0

    def test_ke_unit_pricing(self, shopping_cart, excel_manager, sample_product):
        excel_manager.add_commodity(sample_product)
        shopping_cart.add_item(sample_product[0], 500, "克")
        assert abs(shopping_cart.get_total_amount() - 400.0) < 0.01