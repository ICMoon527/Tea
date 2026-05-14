import re
from datetime import datetime
from typing import Optional, Tuple


class ValidationResult:
    def __init__(self, is_valid: bool, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid

    @classmethod
    def success(cls):
        return cls(True)

    @classmethod
    def failure(cls, message: str):
        return cls(False, message)


def validate_required(value, field_name: str = "此项") -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.failure(f"{field_name}不能为空")
    return ValidationResult.success()


def validate_numeric(value, field_name: str = "此项", min_val: Optional[float] = None, max_val: Optional[float] = None) -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.failure(f"{field_name}不能为空")
    try:
        num = float(str(value).replace(",", "").replace("，", ""))
        if min_val is not None and num < min_val:
            return ValidationResult.failure(f"{field_name}不能小于{min_val}")
        if max_val is not None and num > max_val:
            return ValidationResult.failure(f"{field_name}不能大于{max_val}")
        return ValidationResult.success()
    except (ValueError, TypeError):
        return ValidationResult.failure(f"{field_name}必须为有效数字")


def validate_integer(value, field_name: str = "此项", min_val: Optional[int] = None, max_val: Optional[int] = None) -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.failure(f"{field_name}不能为空")
    try:
        num = int(float(str(value).replace(",", "").replace("，", "")))
        if min_val is not None and num < min_val:
            return ValidationResult.failure(f"{field_name}不能小于{min_val}")
        if max_val is not None and num > max_val:
            return ValidationResult.failure(f"{field_name}不能大于{max_val}")
        return ValidationResult.success()
    except (ValueError, TypeError):
        return ValidationResult.failure(f"{field_name}必须为有效整数")


def validate_date(value, field_name: str = "此项", date_format: str = "%Y-%m-%d") -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.failure(f"{field_name}不能为空")
    try:
        datetime.strptime(str(value).strip(), date_format)
        return ValidationResult.success()
    except ValueError:
        return ValidationResult.failure(f"{field_name}格式必须为{date_format}，例如：2024-01-01")


def validate_phone(value, field_name: str = "电话") -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.success()
    pattern = r'^[\d\-\(\)\s\+]{7,20}$'
    if not re.match(pattern, str(value).strip()):
        return ValidationResult.failure(f"{field_name}格式不正确")
    return ValidationResult.success()


def validate_email(value, field_name: str = "邮箱") -> ValidationResult:
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ValidationResult.success()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, str(value).strip()):
        return ValidationResult.failure(f"{field_name}格式不正确")
    return ValidationResult.success()


def validate_length(value, field_name: str = "此项", min_len: int = 0, max_len: Optional[int] = None) -> ValidationResult:
    if value is None:
        value = ""
    length = len(str(value).strip())
    if length < min_len:
        return ValidationResult.failure(f"{field_name}长度不能少于{min_len}个字符")
    if max_len is not None and length > max_len:
        return ValidationResult.failure(f"{field_name}长度不能超过{max_len}个字符")
    return ValidationResult.success()


def highlight_entry_error(entry) -> None:
    try:
        entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)
    except Exception:
        pass


def clear_entry_highlight(entry) -> None:
    try:
        entry.configure(highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
    except Exception:
        pass


def validate_entry(entry, validators, field_name: str = "此项") -> Optional[str]:
    value = entry.get() if hasattr(entry, 'get') else entry
    if not isinstance(validators, (list, tuple)):
        validators = [validators]
    for validator in validators:
        result = validator(value if hasattr(validator, '__call__') and not isinstance(validator, type(lambda: None))
                          else value)
        if callable(validator):
            result = validator(value)
        if not result:
            highlight_entry_error(entry)
            return result.error_message
    clear_entry_highlight(entry)
    return None