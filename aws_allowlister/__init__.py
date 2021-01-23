# pylint: disable=missing-module-docstring
import logging
from logging import NullHandler

# Set default handler when aws_allowlister is used as library to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())


def set_stream_logger(name='aws_allowlister', level=logging.DEBUG, format_string=None):
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all aws_allowlister messages to ``stdout``.
        >>> import aws_allowlister
        >>> aws_allowlister.set_stream_logger('aws_allowlister.database.build', logging.INFO)
    :type name: string
    :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """
    # remove existing handlers. since NullHandler is added by default
    handlers = logging.getLogger(name).handlers
    for handler in handlers:
        logging.getLogger(name).removeHandler(handler)
    if format_string is None:
        format_string = "%(name)s [%(levelname)s] %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
