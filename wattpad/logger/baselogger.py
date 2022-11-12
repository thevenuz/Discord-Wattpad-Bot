import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class BaseLogger:
    def __init__(self) -> None:
        self.file_prefix="wattpad.logger.baselogger"

    def loggger_init(self):
        try:
            logger=logging.getLogger()
            if (logger.hasHandlers()):
                logger.handlers.clear()

            logger.setLevel(logging.DEBUG)

            formatter=logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

            logname = f"logs\log_{datetime.utcnow().strftime('%Y%m%d')}.txt"
            handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
            handler.suffix = "%Y%m%d"
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            logger.propagate = False

            return logger
        
        except Exception as e:
            raise e
        
        