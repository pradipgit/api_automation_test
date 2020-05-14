import os
import logging

LOGGING_DIR = os.getcwd()

class Logger(object):

    def __init__(self, name, filename, level):
        #name = name.replace('.log','')
        logger = logging.getLogger('log_namespace.%s' % name)    # log_namespace can be replaced with your namespace
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            if not os.path.exists(LOGGING_DIR):
                os.makedirs(LOGGING_DIR)
            file_name = os.path.join(LOGGING_DIR, '%s' % filename)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            if  (level == "debug"):
                handler.setLevel(logging.DEBUG)
            elif (level == "info"):
                handler.setLevel(logging.INFO)
            elif (level == "error"):
                handler.setLevel(logging.ERROR)
            elif (level == "warn"):
                handler.setLevel(logging.ERROR)
            logger.addHandler(handler)
        self._logger = logger
        self._level = level

    def get(self):
        return self._logger

    def log(self, message):
        if  (self._level == "debug"):
                self._logger.debug(message)
        elif (self._level == "info"):
                self._logger.info(message)
        elif (self._level == "error"):
                self._logger.error(message)
        elif (self._level == "warn"):
                self._logger.warn(message)
