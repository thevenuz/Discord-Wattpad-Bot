from wattpad.logger.baselogger import BaseLogger
from wattpad.models.settings import Settings
from wattpad.utils.jsonutil import JsonUtil
from typing import Dict
import aiofiles
import json

class Config:
    def __init__(self) -> None:
        self.filePrefix = "wattpad.utils.config"
        self.logger = BaseLogger().loggger_init()

    async def get_messages(self, language: str = "en") -> Dict:
        """
            get message responses from json file
        """
        try:
            self.logger.info("%s.get_messages method invoked for language: %s", self.filePrefix, language)

            jsonUtil = JsonUtil()

            filePath = jsonUtil.get_file_path("lang", f'{language}.json')

            async with aiofiles.open(filePath, mode="r") as f:
                result = json.loads(await f.read())

            return result

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_messages method for language: %s", self.filePrefix, language, exc_info=1)
            raise e

    async def get_language(self, guildId: str) -> str:
        """
            gets language of the server
        """
        try:
            self.logger.info("%s.get_language method invoked for server: %s", self.filePrefix, guildId)

            #TODO: implement this later

            return "en"
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_language method for server: %s", self.filePrefix, guildId, exc_info=1)
            raise e
        

    def load_settings(self) -> Dict:
        try:
            self.logger.info("%s.load_settings method invoked", self.filePrefix)

            with open("config/settings.json") as f:
                result = json.load(f)

            settings = Settings(result)

            return settings
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.load_settings method", self.filePrefix, exc_info=1)
            raise e
        


# Config.load_settings()