import traceback
import tkinter.messagebox as messagebox
from logger import get_logger

_logger = get_logger()


def setup_global_exception_handler():
    import sys
    original_excepthook = sys.excepthook

    def global_excepthook(exc_type, exc_value, exc_tb):
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        _logger.error(f"未捕获的异常:\n{error_msg}")
        original_excepthook(exc_type, exc_value, exc_tb)

    sys.excepthook = global_excepthook


def setup_tk_exception_handler(root):
    def tk_error_handler(exc_type, exc_value, exc_tb):
        error_detail = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        _logger.error(f"界面异常:\n{error_detail}")

        message = str(exc_value) if exc_value else "发生未知错误"
        messagebox.showerror("系统错误", f"操作出现异常:\n{message}\n\n详细信息已记录到日志文件。")

    root.report_callback_exception = tk_error_handler


def safe_call(func, *args, error_message="操作失败", **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        _logger.exception(f"{error_message}: {e}")
        messagebox.showerror("错误", f"{error_message}:\n{e}")
        return None