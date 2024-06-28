import logging

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    logger: logging.Logger = logging.getLogger()
    items_logger: logging.Logger = logging.getLogger()

    def configure_logging(self, name: str):
        self.logger = logging.getLogger(f"general: {name}")
        self.items_logger = logging.getLogger(f"items: {name}")

        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
        )

        logger_handler = logging.FileHandler("logs/general.log")
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(formatter)
        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(logging.DEBUG)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logger_handler)
        self.logger.addHandler(logger_console_handler)

        items_handler = logging.FileHandler("logs/items.log")
        items_handler.setLevel(logging.DEBUG)
        items_handler.setFormatter(formatter)
        for handler in self.items_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.items_logger.removeHandler(handler)
        self.items_logger.setLevel(logging.DEBUG)
        self.items_logger.addHandler(items_handler)
