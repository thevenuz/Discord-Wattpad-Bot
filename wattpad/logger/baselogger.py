import logging
import os
from pathlib import Path
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class BaseLogger:
    def __init__(self) -> None:
        self.filePrefix="wattpad.logger.baselogger"

    def loggger_init(self):
        try:
            logger=logging.getLogger()
            if (logger.hasHandlers()):
                return logger

            rootDirectory = os.path.dirname(__file__)
            configDirectory = Path(rootDirectory).parents[1]

            filePath = os.path.join(configDirectory, "config", "settings.json")

            with open(filePath) as f:
                result = json.load(f)
            
            logginglevel = result["LogLevel"]

            if not logginglevel:
                logginglevel = "ERROR"

            loglevel = logging.getLevelName(logginglevel)
            
            logger.setLevel(loglevel)

            formatter=logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

            filePath = os.path.join(configDirectory, "logs")

            logname = f"{filePath}/log_{datetime.utcnow().strftime('%Y%m%d')}.txt"
            handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
            handler.suffix = "%Y%m%d"
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            logger.propagate = False

            return logger
        
        except Exception as e:
            raise e
        
        