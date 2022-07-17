from typing import Dict
import aiofiles
import json
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.settings import Settings

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
        
    def load_settings(self) -> Settings:
        try:
            self.logger.info("%s.load_settings method invoked", self.file_prefix)

            with open("settings.json") as f:
                result= json.load(f)

            settings= Settings()
            settings.Token= result["Token"]
            settings.PublicLogChannel= result["PublicLogChannel"]
            settings.LogChannel= result["LogChannel"]

            return settings
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.load_settings method", self.file_prefix, exc_info=1)
            raise e