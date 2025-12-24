import logging
from rich.logging import RichHandler


def get_logger():
    """
    Function that builds a logger instance based on the configuration
        defined and returns it.
        NOTE: this version uses pretty-print stuff from rich.logging

    Returns:
        _logger (logging object): the actual logger instance
    """
    logger = logging.getLogger(__name__)
    FFORMAT = "%(module)s:%(name)s:%(funcName)s: %(message)s"
    DFORMAT = "%Y:%m:%d::%H:%M:%S"
    logging.basicConfig(
        level="INFO", format=FFORMAT, datefmt=DFORMAT, handlers=[RichHandler()]
    )
    _logger = logging.getLogger(__name__)
    return _logger
