"""
This module contains the logging configuration for the application.
https://rennsax.github.io/posts/py-logging-best-practice/
"""

import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    class CustomFormatter(logging.Formatter):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        format_str = "[{asctime} | {name} | L{lineno} | {levelname}] {message}"

        FORMATS = {
            logging.DEBUG: grey + format_str + reset,
            logging.INFO: grey + format_str + reset,
            logging.WARNING: yellow + format_str + reset,
            logging.ERROR: red + format_str + reset,
            logging.CRITICAL: bold_red + format_str + reset,
        }

        def format(self, record: logging.LogRecord):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(
                log_fmt,
                datefmt="%Y-%m-%d %H:%M:%S",
                style="{",
            )

            return formatter.format(record)

    stream_handler.setFormatter(CustomFormatter())
    logger.addHandler(stream_handler)
    return logger