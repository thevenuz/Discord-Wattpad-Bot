from typing import List
from wattpad.db.repository.authorrepo import AuthorRepo
from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.checkcustomchannels import AuthorCustomChannel, StoryCustomChannel
from wattpad.meta.models.result import Result, ResultCheckCustomChannel, ResultCustomChannelSet, ResultCustomChannelUnset
from wattpad.db.models.server import Server
from wattpad.db.models.channel import Channel
from copy import deepcopy

class CustomChannlExec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.commandsexec.customchannelexec"
        self.logger= BaseLogger().loggger_init()
        self.serverRepo= ServerRepo()
        self.storyRepo= StoryRepo()
        self.channelRepo= ChannelRepo()
        self.authorRepo= AuthorRepo()
        self.prefix= "wattpad.com"


    async def set_custom_channel_for_story(self, guildid:str, channelid:str, storyurl: str) -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_channel_for_story method invokedfor server: %s, channel: %s, story url: %s", self.file_prefix, guildid, channelid, storyurl)

            story_urls=""            

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            if not story_urls:
                return ResultCustomChannelSet(False, "No story found with the title", IsInvalidTitle=True)
            
            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_channel(guildid, channelid, story_urls, isstory=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_channel_for_story method invokedfor server: %s, channel: %s, story url: %s", self.file_prefix, guildid, channelid, storyurl,exc_info=1)
            raise e
        
    async def set_custom_channel_for_author(self, guildid:str, channelid:str, authorurl: str) -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_channel_for_author method invokedfor server: %s, channel: %s, author url: %s", self.file_prefix, guildid, channelid, authorurl)

            author_urls=""            

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)

            if not author_urls:
                return ResultCustomChannelSet(False, "No author found with the title", IsInvalidTitle=True)
            
            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple authors found with this title", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_channel(guildid, channelid, author_urls, isauthor=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_channel_for_author method invokedfor server: %s, channel: %s, author url: %s", self.file_prefix, guildid, channelid, authorurl,exc_info=1)
            raise e

    async def unset_custom_channel_for_story(self, guildid:str, channelid:str, storyurl: str) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, story: %s", self.file_prefix, guildid, channelid, storyurl)
            
            story_urls=""            

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            if not story_urls:
                return ResultCustomChannelUnset(False, "No story found with the title", IsInvalidTitle=True)
            
            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelUnset(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_channel(guildid, channelid, story_urls, isstory=True)

                    if result.IsSuccess:
                        return ResultCustomChannelUnset(True, "success")

                    else:
                        self.logger.error("Error in %s.unset_custom_channel_for_story for guild id: %s, channelid: %s, story url: %s", self.file_prefix, guildid, channelid, storyurl)

                        if result.Notfound:
                            return ResultCustomChannelUnset(False, "No custom channel found for this story", Notfound=True)


                    
            return ResultCustomChannelUnset(False, "Unknown error", UnknownError=True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, story: %s", self.file_prefix, guildid, channelid, storyurl,exc_info=1)
            raise e
        
    async def unset_custom_channel_for_author(self, guildid:str, channelid:str, authorurl: str) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, author: %s", self.file_prefix, guildid, channelid, authorurl)
            
            author_urls=""            

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)

            if not author_urls:
                return ResultCustomChannelUnset(False, "No author found with the title", IsInvalidTitle=True)
            
            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelUnset(False, "Multiple authors found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_channel(guildid, channelid, author_urls, isauthor=True)

                    if result.IsSuccess:
                        return ResultCustomChannelUnset(True, "success")

                    else:
                        self.logger.error("Error in %s.unset_custom_channel_for_author for guild id: %s, channelid: %s, story url: %s", self.file_prefix, guildid, channelid, authorurl)

                        if result.Notfound:
                            return ResultCustomChannelUnset(False, "No custom channel found for this author", Notfound=True)


                    
            return ResultCustomChannelUnset(False, "Unknown error", UnknownError=True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, author: %s", self.file_prefix, guildid, channelid, authorurl,exc_info=1)
            raise e

    async def check_custom_channels(self, guildid: str, category:str) -> ResultCheckCustomChannel:
        try:
            self.logger.info("%s.check_custom_channels method invoked for server: %s, category: %s", self.file_prefix, guildid, category)

            isauthor=False
            isstory=False
            isempty= False

            story_custom_channels=[]
            author_custom_channels=[]


            if category.lower() == "author":
                isauthor = True
            elif category.lower() == "story":
                isstory = True
            else:    
                isauthor= True
                isstory= True

            #get server id
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                #get all the custom channels for this server id
                custom_channels= await self.channelRepo.get_channels_from_server_id(serverid, 1, 1)

                if custom_channels:
                    if isstory:
                        #get stories that are associated with this custom channel
                        for channel in custom_channels:
                            stories= self.storyRepo.get_story_urls_from_channel_id(channel.ChannelId, 1, 1)

                            story_custom_channel=StoryCustomChannel(channel.Channel, stories)

                            story_custom_channels.append(deepcopy(story_custom_channel))

                    if isauthor:
                        #get authors that are associated with this custom channel
                        for channel in custom_channels:
                            authors= self.authorRepo.get_author_urls_from_channel_id(channel.ChannelId, 1, 1)

                            author_custom_channel=AuthorCustomChannel(channel.Channel, authors)

                            author_custom_channels.append(deepcopy(author_custom_channel))
                else:
                    isempty= True

            else:
                return ResultCheckCustomChannel(False, "Error while getting server id")

            if isempty:
                return ResultCheckCustomChannel(False, "No custom channels found for this server", IsEmpty=True)  
            else:
                if isauthor and isstory:
                    return ResultCheckCustomChannel(True, "success", StoryCustomChannels=story_custom_channels, AuthorCustomChannels=author_custom_channels)
                elif isstory:
                    return ResultCheckCustomChannel(True, "success", StoryCustomChannels=story_custom_channels)
                elif isauthor:
                    return ResultCheckCustomChannel(True, "success", AuthorCustomChannels=author_custom_channels)
                    
            return ResultCheckCustomChannel(False, "unknown error")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_custom_channels method invoked for server: %s, category: %s", self.file_prefix, guildid, category,exc_info=1)
            raise e
        

    async def __set_custom_channel(self, guildid:str, channelid:str, url: str, isauthor: bool=False, isstory:bool= False) -> Result:
        try:
            self.logger.info("%s.__set_custom_channel method invoked for server: %s, channel: %s, url: %s, isauthor: %s, is story: %s", self.file_prefix, guildid, channelid, url, isauthor, isstory)

            #get the data from server table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            #insert the data in to server table if no data is found
            if not serverid:
                server=Server(GuildId=guildid, IsActive=1)
                serverid= await self.serverRepo.insert_server_data(server)

            if serverid:
                #insert the data in to channel table
                channel= Channel(channel=channelid, ServerId=serverid, IsActive=1, IsCustomChannel=1)

                channel_result= await self.channelRepo.insert_channel_data(channel)

                if channel_result:
                    if isstory:
                        #get the storyid
                        story_id= await self.storyRepo.get_story_id_from_server_and_url(url, serverid)
                        if not story_id:
                            return Result(False, "Error while getting story id from db")

                        else:
                            #update the story table with the custom channel id
                            update_result= await self.storyRepo.update_channel_id_for_stories(story_id, channel_result, 1)

                            if update_result:
                                return Result(True, "success")

                            else:
                                return Result(False, "Error while updating channel id to db")

                    else:
                        #get the author id
                        author_id= await self.authorRepo.get_author_id_from_server_and_url(url, serverid)

                        if not author_id:
                            return Result(False, "Error while getting author id from db")

                        else:
                            #update the author table with custom channel id
                            update_result= await self.authorRepo.update_channel_id_for_authors(author_id, channel_result, 1)

                            if update_result:
                                return Result(True, "success")

                            else:
                                return Result(False, "Error while updating channel id to db")


                else:
                    #unknown error
                    return Result(False, "Error while getting story id from db")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__set_custom_channel method invoked for server: %s, channel: %s, url: %s, isauthor: %s, is story: %s", self.file_prefix, guildid, channelid, url, isauthor, isstory, exc_info=1)
            raise e
        
    async def __unset_custom_channel(self, guildid:str, channelid:str, url: str, isauthor: bool=False, isstory:bool= False) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.__unset_custome_channel method invoked for server: %s, channel: %s, url: %s, isauthor: %s, isstory: %s", self.file_prefix, guildid, channelid, url, isauthor, isstory)

            #get the data from server table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                if isstory:
                    story_id= await self.storyRepo.get_story_id_with_custom_channel_from_server_and_url(url, serverid, 1, 1)

                    if story_id:
                        custom_channel_id= await self.storyRepo.get_custom_channel_id_from_story_id(story_id, url, 1)

                        if custom_channel_id:
                            #remove channel id from story and inactivate in channel table

                            story_inactivate_result= await self.storyRepo.inactivate_custom_channel_for_stories(storyid=story_id, channelid="", isactive=1)

                            if story_inactivate_result:
                                channel_inactivate_result= await self.channelRepo.inactivate_channel_by_channel_id(custom_channel_id)

                                if channel_inactivate_result:
                                    return ResultCustomChannelUnset(True, "success")
                                
                                else:
                                    return ResultCustomChannelUnset(False, "Error inactivating custom channel")
                            
                            else:
                                return  ResultCustomChannelUnset(False, "Error while updating channel in story table")
                        
                        else:
                            return ResultCustomChannelUnset(False, "Error while getting custom channel id", Notfound=True)

                else:
                    author_id= await self.authorRepo.get_author_id_with_custom_channel_from_server_and_url(serverid=serverid, url=url, isactive=1, iscustomchannel=1)

                    if author_id:
                        custom_channel_id= await self.authorRepo.get_custom_channel_id_from_author_id(author_id, url, 1)

                        if custom_channel_id:
                            #remove channel id from author and inactivate in channel table

                            author_inactivate_result= await self.authorRepo.inactivate_custom_channel_for_authors(author_id, "", 1, 0)

                            if author_inactivate_result:
                                channel_inactivate_result= await self.channelRepo.inactivate_channel_by_channel_id(custom_channel_id)

                                if channel_inactivate_result:
                                    return ResultCustomChannelUnset(True, "success")
                                
                                else:
                                    return ResultCustomChannelUnset(False, "Error inactivating custom channel")
                            
                            else:
                                return  ResultCustomChannelUnset(False, "Error while updating channel in author table")
                        
                        else:
                            return ResultCustomChannelUnset(False, "Error while getting custom channel id", Notfound=True)


            else:
                return ResultCustomChannelUnset(False, "Error while getting server id")
        
            return ResultCustomChannelUnset(False, "Unknown error")

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__unset_custome_channel method invoked for server: %s, channel: %s, url: %s, isauthor: %s, isstory: %s", self.file_prefix, guildid, channelid, url, isauthor, isstory,exc_info=1)
            raise e
        


    #region misc methods
    async def __get_story_url_from_title(self, title:str, server:str) -> List[str]:
        try:
            self.logger.info("%s.__get_story_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server)

            #first get server id
            serverid= await self.serverRepo.get_serverid_from_server(server)

            if serverid:
                format_title=f"%{title}%"
                story_urls= await self.storyRepo.get_story_url_from_title(format_title, serverid=serverid)

                return story_urls

            return title
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server, exc_info=1)
            raise e

    async def __get_author_url_from_title(self, title:str, server:str) -> List[str]:
        try:
            self.logger.info("%s.__get_author_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server)

            #first get server id
            serverid= await self.serverRepo.get_serverid_from_server(server)

            if serverid:
                format_title=f"%{title}%"
                author_urls= await self.authorRepo.get_author_url_from_title(format_title, serverid=serverid)

                return author_urls

            return title
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server, exc_info=1)
            raise e
    
    #endregion