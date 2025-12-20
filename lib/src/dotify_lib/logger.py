from logging import INFO, Formatter, StreamHandler, getLogger

_logger = getLogger(__name__)
_logger.setLevel(INFO)

handler = StreamHandler()
formatter = Formatter("[%(asctime)s][%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
_logger.addHandler(handler)


def log_info(message: str):
    _logger.info(message)


def log_warning(message: str):
    _logger.warning(message)


def log_error(message: str):
    _logger.error(message)


def log_critical(message: str):
    _logger.critical(message)


def log_exception(message: str):
    log_critical(message)
    exit(-1)


def log_debug(message: str):
    _logger.debug(message)
