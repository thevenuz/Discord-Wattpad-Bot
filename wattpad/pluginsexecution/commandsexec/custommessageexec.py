from copy import deepcopy
from typing import List
from wattpad.db.models.custommsg import CustomMsg
from wattpad.db.repository.authorrepo import AuthorRepo
from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.checkcustomchannels import CheckCustomMsgAuthor, CheckCustomMsgStory, StoryCustomChannel
from wattpad.meta.models.result import Result, ResultCheck, ResultCheckCustomChannel, ResultCheckCustomMsg, ResultCustomChannelSet, ResultCustomChannelUnset
from wattpad.db.repository.custommsgrepo import CustomMsgrepo
from wattpad.meta.models.enum import CustomMsgType

class CustomMessageExec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.commandsexec.custommessageexec"
        self.logger= BaseLogger().loggger_init()
        self.serverRepo= ServerRepo()
        self.storyRepo= StoryRepo()
        self.channelRepo= ChannelRepo()
        self.authorRepo= AuthorRepo()
        self.customMsgRepo= CustomMsgrepo()
        self.prefix= "wattpad.com"

    async def set_custom_message_for_story(self, guildid: str, storyurl:str, message:str) -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.file_prefix, guildid, storyurl, message)

            story_urls=""            

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            if not story_urls:
                return ResultCustomChannelSet(False, "No story found with the title", IsInvalidTitle=True)

            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_message(guildid, story_urls, message, isstory=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.file_prefix, guildid, storyurl, message,exc_info=1)
            raise e

    async def set_custom_message_for_author(self, guildid: str, authorurl:str, message:str) -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", self.file_prefix, guildid, authorurl, message)

            author_urls=""            

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)

            if not author_urls:
                return ResultCustomChannelSet(False, "No Author found with the name", IsInvalidTitle=True)

            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple authors found with this name", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_message(guildid, author_urls, message, isauthor=True, isstory=False)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_author method invoked for author: %s, story: %s, msg: %s", self.file_prefix, guildid, authorurl, message,exc_info=1)
            raise e

    async def unset_custom_message_for_story(self, guildid: str, storyurl:str) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.unset_custom_message_for_story method invoked for server: %s, story: %s", self.file_prefix, guildid, storyurl)

            story_urls=""            

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            if not story_urls:
                return ResultCustomChannelSet(False, "No story found with the title", IsInvalidTitle=True)

            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_message(guildid, story_urls, isstory=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    elif result.Notfound:
                        return ResultCustomChannelUnset(False, "Error while fetching the story id", Notfound=True)

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_message_for_story method invoked for server: %s, story: %s", self.file_prefix, guildid, storyurl,exc_info=1)
            raise e

    async def unset_custom_message_for_author(self, guildid: str, authorurl:str) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.author method invoked for server: %s, author: %s", self.file_prefix, guildid, authorurl)

            author_urls=""            

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)

            if not author_urls:
                return ResultCustomChannelSet(False, "No author found with the title", IsInvalidTitle=True)

            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple authors found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_message(guildid, author_urls, isstory=False, isauthor=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    elif result.Notfound:
                        return ResultCustomChannelUnset(False, "Error while fetching the author id", Notfound=True)

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.author method invoked for server: %s, author: %s", self.file_prefix, guildid, authorurl,exc_info=1)
            raise e       

    async def check_custom_messages(self, guildid:str, category:str) -> ResultCheckCustomMsg:
        try:
            self.logger.info("%s.check_custom_messages method invoked for server: %s, category: %s", self.file_prefix, guildid, category)

            isauthor=False
            isstory=False
            isempty= False

            story_custom_msgs=[]
            author_custom_msgs=[]


            if category.lower() == "announcements":
                isauthor = True
            elif category.lower() == "story":
                isstory = True
            else:    
                isauthor= True
                isstory= True

            #get server id
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                #get all the custom msgs for this server id
                custom_msgs= await self.customMsgRepo.get_custom_msgs_from_server_id(serverid, 1)

                if custom_msgs:
                    if isstory:
                        #get stories that are associated with this custom msg
                        for msg in custom_msgs:
                            if msg.StoryId:
                                story= self.storyRepo.get_story_url_from_story_id(msg.StoryId, 1)

                                story_custom_msg= CheckCustomMsgStory(story, msg.Message)

                                story_custom_msgs.append(deepcopy(story_custom_msg))

                    if isauthor:
                        #get Authors that are associated with this custom msg
                        for msg in custom_msgs:
                            if msg.AuthorId:
                                author= self.authorRepo.get_author_url_from_author_id(msg.AuthorId, 1)

                                author_custom_msg= CheckCustomMsgAuthor(author, msg.Message)

                                author_custom_msgs.append(deepcopy(author_custom_msg))

                    else:
                        isempty= True

            else:
                return ResultCheckCustomMsg(False, "Error while getting server id")

            if isempty:
                return ResultCheckCustomMsg(False, "No custom msgs found for this server", IsEmpty=True)  
            else:
                if isauthor and isstory:
                    return ResultCheckCustomMsg(True, "success", StoryCustomMsgs=story_custom_msgs, AuthorCustomMsgs=author_custom_msgs)
                elif isstory:
                    return ResultCheckCustomMsg(True, "success", StoryCustomMsgs=story_custom_msgs)
                elif isauthor:
                    return ResultCheckCustomMsg(True, "success", AuthorCustomMsgs=author_custom_msgs)
                    
            return ResultCheckCustomMsg(False, "unknown error")

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_custom_messages method invoked for server: %s, category: %s", self.file_prefix, guildid, category,exc_info=1)
            raise e
        

    async def __unset_custom_message(self, guildid: str, url: str, isstory:bool= True, isauthor:bool= False) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.__unset_custom_message method invoked for server: %s, url: %s, is story: %s, is author: %s", self.file_prefix, guildid, url, isstory, isauthor)
            
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                if isauthor:#get story id
                    authorid= await self.authorRepo.get_author_id_from_server_and_url(url, serverid, 1)
                    if authorid:
                        #get custom msg id for this story id
                        custom_msg_id= await self.customMsgRepo.get_custom_msg_id_from_author_id(authorid, 1)

                        if len(custom_msg_id) > 1:
                            return ResultCustomChannelUnset(False, "Multiple custom msgs were found for same author id", HasMultipleResults=True)

                        else:
                            #delete custom msg id
                            delete_result= await self.customMsgRepo.delete_custom_msg_by_id(custom_msg_id)

                            if delete_result:
                                return ResultCustomChannelUnset(True, "success")
                            else:
                                return ResultCustomChannelUnset(False, "error while deleting custom msg")

                    else:
                        return ResultCustomChannelUnset(False, "Error while fetching the author id", Notfound=True) #return author not found
                else:
                    #get story id
                    storyid= await self.storyRepo.get_story_id_from_server_and_url(url, serverid, 1)
                    if storyid:
                        #get custom msg id for this story id
                        custom_msg_id= await self.customMsgRepo.get_custom_msg_id_from_story_id(storyid, 1)

                        if len(custom_msg_id) > 1:
                            return ResultCustomChannelUnset(False, "Multiple custom msgs were found for same story id", HasMultipleResults=True)

                        else:
                            #delete custom msg id
                            delete_result= await self.customMsgRepo.delete_custom_msg_by_id(custom_msg_id)

                            if delete_result:
                                return ResultCustomChannelUnset(True, "success")
                            else:
                                return ResultCustomChannelUnset(False, "error while deleting custom msg")

                    else:
                        return ResultCustomChannelUnset(False, "Error while fetching the story id", Notfound=True) #return story not found

            else:
                return ResultCustomChannelUnset(False, "Error while fetching the server id")

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__unset_custom_message method invoked for server: %s, url: %s, is story: %s, is author: %s", self.file_prefix, guildid, url, isstory, isauthor,exc_info=1)
            raise e
        

    async def __set_custom_message(self, guildid: str, url: str, message: str, isstory:bool= True, isauthor:bool= False) -> Result:
        try:
            self.logger.info("%s.__set_custom_message method invoked for server: %s, url: %s, msg: %s, is story: %s, is author: %s", self.file_prefix, guildid, url, message, isstory, isauthor)

            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                if isauthor:
                    authorid= await self.authorRepo.get_author_id_from_server_and_url(url, serverid, 1)

                    if authorid:
                        custommsg= CustomMsg(Type=CustomMsgType.Author, StoryId=0, AuthorId=authorid, ServerId=serverid, IsActive=1, Message=message)
                        result= await self.customMsgRepo.insert_custom_msg_data(custommsg)
                        if result:
                            return Result(True, "success")
                        else:
                            return Result(False, "Error while inserting the custom msg data")
                    else:
                        return Result(False, "Error while fetching the author id") #return story not found

                else:
                    #get the story id
                    storyid= await self.storyRepo.get_story_id_from_server_and_url(url, serverid, 1)

                    if storyid:
                        custommsg= CustomMsg(Type=CustomMsgType.Story, StoryId=storyid, AuthorId=0, ServerId=serverid, IsActive=1, Message=message)
                        result= await self.customMsgRepo.insert_custom_msg_data(custommsg)
                        if result:
                            return Result(True, "success")
                        else:
                            return Result(False, "Error while inserting the custom msg data")
                    else:
                        return Result(False, "Error while fetching the story id") #return story not found
            
            else:
                return Result(False, "Error while fetching the server id")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__set_custom_message method invoked for server: %s, url: %s, msg: %s, is story: %s, is author: %s", self.file_prefix, guildid, url, message, isstory, isauthor,exc_info=1)
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
        