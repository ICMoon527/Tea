
from datetime import datetime, timedelta


def convert_units(amount: float, from_unit: str, to_unit: str) -> float:
    """单位转换：斤与克之间的转换"""
    if from_unit == to_unit:
        return amount
    elif from_unit == "斤" and to_unit == "克":
        return amount * 500
    elif from_unit == "克" and to_unit == "斤":
        return amount / 500
    else:
        raise ValueError(f"不支持的单位转换: {from_unit} -&gt; {to_unit}")


def convert_to_jin(quantity: float, unit: str) -> float:
    """将任意单位转换为斤"""
    return convert_units(quantity, unit, "斤")


def convert_to_ke(quantity: float, unit: str) -> float:
    """将任意单位转换为克"""
    return convert_units(quantity, unit, "克")


def calculate_cost(quantity: float, unit: str, cost_price_per_jin: float) -> float:
    """计算成本

    Args:
        quantity: 数量
        unit: 单位（斤/克）
        cost_price_per_jin: 每斤成本价

    Returns:
        总成本
    """
    quantity_in_jin = convert_to_jin(quantity, unit)
    return quantity_in_jin * cost_price_per_jin


def is_expired(production_date: str, shelf_life_months: int) -> bool:
    """判断是否过期

    Args:
        production_date: 生产日期 (YYYY-MM-DD)
        shelf_life_months: 保质期（月）

    Returns:
        bool: 是否过期
    """
    try:
        prod_date = datetime.strptime(production_date, "%Y-%m-%d")
        expire_date = prod_date + timedelta(days=shelf_life_months * 30)
        return datetime.now() > expire_date
    except (ValueError, TypeError):
        return False


def days_until_expire(production_date: str, shelf_life_months: int) -> int:
    """计算距离过期还有多少天

    Args:
        production_date: 生产日期 (YYYY-MM-DD)
        shelf_life_months: 保质期（月）

    Returns:
        int: 距离过期天数，负数表示已过期
    """
    try:
        prod_date = datetime.strptime(production_date, "%Y-%m-%d")
        expire_date = prod_date + timedelta(days=shelf_life_months * 30)
        delta = expire_date - datetime.now()
        return delta.days
    except (ValueError, TypeError):
        return -999


def format_date(date_str: str) -> str:
    """格式化日期字符串"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return date_str


def format_currency(amount: float) -> str:
    """格式化货币显示"""
    return f"{amount:.2f}"


def format_number(number: float, decimals: int = 2) -> str:
    """格式化数字显示"""
    return f"{number:.{decimals}f}"

