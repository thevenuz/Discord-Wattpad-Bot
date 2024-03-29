from wattpad.logger.baselogger import BaseLogger
from typing import List

class MsgUtil:
    def __init__(self) -> None:
        self.filePrefix = "wattpad.utils.msgutil"
        self.logger = BaseLogger().loggger_init()

    async def build_check_authors_msg(self, authors: List) -> str:
        try:
            self.logger.info("%s.build_check_authors_msg method invoked", self.filePrefix)

            response = ""

            for index, author in enumerate(authors):
                response= f"{response}{index + 1}. {author['url']}\n"

            return response
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_authors_msg method", self.filePrefix, exc_info=1)
            raise e

    async def build_check_stories_msg(self, stories: List) -> str:
        try:
            self.logger.info("%s.build_check_stories_msg method invoked", self.filePrefix)

            response = ""

            for index, story in enumerate(stories):
                response= f"{response}{index + 1}. {story['url']}\n"

            return response
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_stories_msg method", self.filePrefix, exc_info=1)
            raise e

    async def build_check_channels_msg(self, channels: List) -> str:
        try:
            self.logger.info("%s.build_check_channels_msg method invoked", self.filePrefix)

            response = ""

            for index, channel in enumerate(channels):
                response= f"{response}{index + 1}. <#{channel}>\n"

            return response
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_channels_msg method", self.filePrefix, exc_info=1)
            raise e
        
    async def build_check_custom_channel_msg(self, data: List, isAuthor: bool = False, isStory: bool = False) -> str:
        try:
            self.logger.info("%s.build_check_custom_channel_msg method invoked", self.filePrefix)

            response = ""
            newLine = "\n"

            # if isAuthor:
            #     response = "ANNOUNCEMENTS:\n"
            
            # else:
            #     response = "STORIES:\n"

            for index, record in enumerate(data):
                response = f"{response}{index+1}. <#{record['CustomChannel']}> : {record['url']}{newLine}"


            return response
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_custom_channel_msg method", self.filePrefix, exc_info=1)
            raise e

    async def build_check_custom_messages_msg(self, data: List, isAuthor: bool = False, isStory: bool = False) -> str:
        try:
            self.logger.info("%s.build_check_custom_messages_msg method invoked", self.filePrefix)

            response = ""
            newLine = "\n"

            # if isAuthor:
            #     response = "ANNOUNCEMENTS:\n"
            
            # else:
            #     response = "STORIES:\n"

            for index, record in enumerate(data):
                response = f"{response}{index+1}. {record['url']} : {record['CustomMsg']}{newLine}"


            return response
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_custom_messages_msg method", self.filePrefix, exc_info=1)
            raise e
        