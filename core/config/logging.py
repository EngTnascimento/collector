import logging


def basic_logger(name, level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(f"BASIC::{name}")

    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
