from utils import (
    convert_units, convert_to_jin, convert_to_ke,
    calculate_cost, is_expired, days_until_expire,
    format_date, format_currency, format_number
)
from datetime import datetime, timedelta
import pytest


class TestUnitConversion:
    def test_same_unit(self):
        assert convert_units(100, "斤", "斤") == 100

    def test_jin_to_ke(self):
        assert convert_units(1, "斤", "克") == 500

    def test_ke_to_jin(self):
        assert convert_units(500, "克", "斤") == 1

    def test_unsupported_conversion(self):
        with pytest.raises(ValueError):
            convert_units(1, "斤", "磅")


class TestConvertToJin:
    def test_from_jin(self):
        assert convert_to_jin(5, "斤") == 5

    def test_from_ke(self):
        assert convert_to_jin(1000, "克") == 2.0


class TestConvertToKe:
    def test_from_jin(self):
        assert convert_to_ke(1, "斤") == 500

    def test_from_ke(self):
        assert convert_to_ke(500, "克") == 500


class TestCalculateCost:
    def test_jin_unit(self):
        assert calculate_cost(2, "斤", 200) == 400

    def test_ke_unit(self):
        assert calculate_cost(1000, "克", 200) == 400


class TestIsExpired:
    def test_expired(self):
        past_date = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
        assert is_expired(past_date, 12) is True

    def test_not_expired(self):
        future_date = (datetime.now() + timedelta(days=400)).strftime("%Y-%m-%d")
        assert is_expired(future_date, 24) is False

    def test_invalid_date(self):
        assert is_expired("invalid-date", 12) is False


class TestDaysUntilExpire:
    def test_future(self):
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        assert days_until_expire(future_date, 1) >= 0

    def test_past(self):
        past_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        assert days_until_expire(past_date, 1) < 0

    def test_invalid_date(self):
        assert days_until_expire("invalid-date", 12) == -999


class TestFormatFunctions:
    def test_format_date_valid(self):
        assert format_date("2024-01-15") == "2024-01-15"

    def test_format_date_invalid(self):
        assert format_date("invalid") == "invalid"

    def test_format_currency(self):
        assert format_currency(123.456) == "123.46"

    def test_format_number(self):
        assert format_number(3.14159, 2) == "3.14"