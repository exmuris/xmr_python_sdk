from enum import Enum
import logging
# from pprint import pprint


LOGGER_ROOT_NAME = "xmr"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def get_logger(name: str = "__main__", level: LogLevel = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    )
    logger = logging.getLogger("%s.%s" % (LOGGER_ROOT_NAME, name))
    # streamHandler = logging.StreamHandler()
    # streamHandler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # streamHandler.setFormatter(formatter)
    # logger.setLevel(logging.DEBUG)
    return logger


# class LoggerWrapper:
#     def __init__(self):
#         super(LoggerWrapper, self).__init__()
#         self.__print = pprint

#     def __getattr__(self, name):
#         return self._print

#     def _print(self, params):
#         self.__print(params)

#     def __get__(self, sender, cls):
#         case = (sender, "logger")
#         return getattr(*case) if hasattr(*case) and getattr(*case) else self
