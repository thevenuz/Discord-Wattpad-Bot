from typing import Dict
import aiofiles
import json
from wattpad.logger.baselogger import BaseLogger

class Config:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.utils.config"
        self.logger= BaseLogger().loggger_init()

    async def get_messages(self, language:str="en") ->Dict:
        try:
            self.logger.info("%s.get_messages method invoked for language: %s", self.file_prefix, language)

            filepath="lang/en.json" #TODO: make this dynamic

            async with aiofiles.open(filepath, mode="r") as f:
                result=json.loads(await f.read())

            return result

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_messages method invoked for language: %s", self.file_prefix, language, exc_info=1)
            raise e
        