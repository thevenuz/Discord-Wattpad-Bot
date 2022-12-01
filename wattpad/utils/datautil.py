from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.jsonutil import JsonUtil
from wattpad.models.author import Authors
from typing import Dict

class DataUtil:
    def __init__(self) -> None:
        self.filePrefix = "wattpad.utils.datautil"
        self.logger = BaseLogger().loggger_init()

    #read operations
    async def get_authors(self) -> Dict:
        try:
            self.logger.info("%s.get_authors method invoked", self.filePrefix)

            authors = await JsonUtil().read_from_json("config", "authors.json")

            return authors
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_authors method", self.filePrefix, exc_info=1)
            raise e

    async def get_stories(self) -> Dict:
        try:
            self.logger.info("%s.get_stories method invoked", self.filePrefix)

            stories = await JsonUtil().read_from_json("config", "stories.json")

            return stories
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_stories method", self.filePrefix, exc_info=1)
            raise e
        
    async def get_channels(self) -> Dict:
        try:
            self.logger.info("%s.get_channels method invoked", self.filePrefix)

            channels = await JsonUtil().read_from_json("config", "channels.json")

            return channels
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_channels method", self.filePrefix, exc_info=1)
            raise e

    async def get_messages(self) -> Dict:
        try:
            self.logger.info("%s.get_messages method invoked", self.filePrefix)

            channels = await JsonUtil().read_from_json("config", "messages.json")

            return channels
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_messages method", self.filePrefix, exc_info=1)
            raise e
    

    #write operations
    async def update_authors(self, authors: Dict) -> bool:
        try:
            self.logger.info("%s.update_authors method invoked", self.filePrefix)

            result = await JsonUtil().write_to_json("config", "authors.json", authors)

            if result:
                return True

            return False
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_authors method", self.filePrefix, exc_info=1)
            return False
    
    async def update_stories(self, stories: Dict) -> bool:
        try:
            self.logger.info("%s.update_stories method invoked", self.filePrefix)

            result = await JsonUtil().write_to_json("config", "stories.json", stories)

            if result:
                return True

            return False
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_stories method", self.filePrefix, exc_info=1)
            return False
        
    async def update_channels(self, channels: Dict) -> bool:
        try:
            self.logger.info("%s.update_channels method invoked", self.filePrefix)

            result = await JsonUtil().write_to_json("config", "channels.json", channels)

            if result:
                return True

            return False
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_channels method", self.filePrefix, exc_info=1)
            return False
    
    async def update_messages(self, messages: Dict) -> bool:
        try:
            self.logger.info("%s.update_messages method invoked", self.filePrefix)

            result = await JsonUtil().write_to_json("config", "messages.json", messages)

            if result:
                return True

            return False
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_messages method", self.filePrefix, exc_info=1)
            return False
    