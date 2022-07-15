from typing import Dict, List
from wattpad.db.models.author import Author
from wattpad.db.models.channel import Channel
from wattpad.db.models.custommsg import CustomMsg
from wattpad.logger.baselogger import BaseLogger
from wattpad.db.models.story import Story
from copy import deepcopy

class Map:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.meta.mapping.map"
        self.logger= BaseLogger().loggger_init()

    async def map_story_records_list(self, data, columns) -> List[Story]:
        """
            This method maps data from DB to class object
        """
        try:
            self.logger.info("%s.map_story_records method invoked", self.file_prefix)

            result=[]

            maps = [dict(zip(columns, row)) for row in data]

            if maps:
                for map in maps:
                    map_result = await self.__map_story_record(map = map)

                    if map_result:
                        result.append(deepcopy(map_result))

            if result:
                return result
            
            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.map_story_records invoked", self.file_prefix,exc_info=1)
            raise e
        
    async def __map_story_record(self, map:Dict) -> Story:
        try:
            self.logger.info("%s.__map_story_record method invoked", self.file_prefix)

            result= Story()

            if map:
                result.StoryId= map["storyid"]
                result.Url= map["url"]
                result.ServerId= map["serverid"]
                result.ChannelId= map["channelid"]
                result.IsActive= map["isactive"]
                result.LastUpdatedOn= map["lastupdatedon"]
                result.LastcheckedOn= map["lastcheckedon"]
                result.RegisteredOn= map["registeredon"]

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__map_story_record method invoked", self.file_prefix,exc_info=1)
            raise e
        
    async def map_author_records_list(self, data, columns) -> List[Story]:
        """
            This method maps data from DB to class object
        """
        try:
            self.logger.info("%s.map_author_records_list method invoked", self.file_prefix)

            result=[]

            maps = [dict(zip(columns, row)) for row in data]

            if maps:
                for map in maps:
                    map_result = await self.__map_author_record(map = map)

                    if map_result:
                        result.append(deepcopy(map_result))

            if result:
                return result
            
            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.map_author_records_list invoked", self.file_prefix,exc_info=1)
            raise e

    async def __map_author_record(self, map:Dict) -> Story:
        try:
            self.logger.info("%s.__map_author_record method invoked", self.file_prefix)

            result= Author()

            if map:
                result.AuthorId= map["authorid"]
                result.Url= map["url"]
                result.ServerId= map["serverid"]
                result.ChannelId= map["channelid"]
                result.IsActive= map["isactive"]
                result.LastUpdatedOn= map["lastupdatedon"]
                result.LastcheckedOn= map["lastcheckedon"]
                result.RegisteredOn= map["registeredon"]

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__map_author_record method invoked", self.file_prefix,exc_info=1)
            raise e

    async def map_channel_records_list(self, data, columns) -> List[Channel]:
        try:
            self.logger.info("%s.map_channel_records_list method invoked", self.file_prefix)

            result=[]

            maps = [dict(zip(columns, row)) for row in data]

            if maps:
                for map in maps:
                    map_result = await self.__map_channel_record(map = map)

                    if map_result:
                        result.append(deepcopy(map_result))

            if result:
                return result
            
            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.map_channel_records_list method invoked", self.file_prefix,exc_info=1)
            raise e
        
    async def __map_channel_record(self, map:Dict) -> Channel:
        try:
            self.logger.info("%s.__map_channel_record method invoked", self.file_prefix)

            result= Channel()

            if map:
                result.ChannelId= map["channelid"]
                result.Channel= map["channel"]
                result.ServerId= map["serverid"]
                result.IsActive= map["isactive"]
                result.IsCustomChannel= map["iscustomchannel"]
                result.RegisteredOn= map["registeredon"]

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__map_channel_record method invoked", self.file_prefix,exc_info=1)
            raise e

    async def map_custom_msg_records_list(self, data, columns) -> List[Channel]:
        try:
            self.logger.info("%s.map_custom_msg_records_list method invoked", self.file_prefix)

            result=[]

            maps = [dict(zip(columns, row)) for row in data]

            if maps:
                for map in maps:
                    map_result = await self.__map_cutsom_msg_record(map = map)

                    if map_result:
                        result.append(deepcopy(map_result))

            if result:
                return result
            
            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.map_custom_msg_records_list method invoked", self.file_prefix,exc_info=1)
            raise e     
        
    async def __map_cutsom_msg_record(self, map:Dict) -> Channel:
        try:
            self.logger.info("%s.__map_cutsom_msg_record method invoked", self.file_prefix)

            result= CustomMsg()

            if map:
                result.MsgId= map["msgid"]
                result.Type= map["type"]
                result.Message= map["message"]
                result.StoryId= map["storyid"]
                result.AuthorId= map["authorid"]
                result.ServerId= map["serverid"]
                result.IsActive= map["isactive"]
                result.RegisteredOn= map["registeredon"]

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__map_cutsom_msg_record method invoked", self.file_prefix,exc_info=1)
            raise e