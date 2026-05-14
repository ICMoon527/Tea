import logging
import os
from datetime import datetime
from typing import Optional


class AppLogger:
    _instance: Optional["AppLogger"] = None

    def __init__(self):
        self._logger = logging.getLogger("TeaInventory")
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    @classmethod
    def get_instance(cls) -> "AppLogger":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def exception(self, message: str):
        self._logger.exception(message)


def get_logger() -> AppLogger:
    return AppLogger.get_instance()