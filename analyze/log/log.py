import logging
from logging.handlers import RotatingFileHandler

class Log(object):
    def __init__(self):
        rotate_handler=RotatingFileHandler(self.conf.log_path+'/web_proxy.log',maxBytes=10*1024*1024,backupCount=10)
        formatter=logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]')
        rotate_handler.setFormatter(formatter)
        self.logger=logging.getLogger("web_proxy")
        self.logger.addHandler(rotate_handler)
        self.logger.setLevel(self._get_log_level())

    def _get_log_level(self):
        levels={'debug':logging.DEBUG,
                'info':logging.INFO,
                'warning':logging.WARNING,
                'error':logging.ERROR,
                'critical':logging.CRITICAL}
        return levels.get(self.conf.log_level,logging.WARNING)

    @property
    def debug(self):
        return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warn(self):
        return self.logger.warning

    @property
    def error(self):
        return self.logger.error

    @property
    def critical(self):
        return self.logger.critical

LOG=Log()

