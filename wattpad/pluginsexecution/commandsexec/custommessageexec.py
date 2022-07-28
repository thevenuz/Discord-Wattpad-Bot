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
from wattpad.meta.models.enum import Category

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

    async def set_custom_message_for_story(self, guildid: str, storyurl:str= "", message:str="") -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.file_prefix, guildid, storyurl, message)

            if not storyurl:
                category_result= await self.__set_custom_message_for_category(guildid, message, isstory=True, isauthor=False)

                if category_result.IsSuccess:
                    return Result(True, "Success")
                
                return Result(False, category_result.ResultInfo)

            story_urls= []       

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            else:
                story_urls.append(storyurl)

            if not story_urls:
                return ResultCustomChannelSet(False, "No story found with the title", IsInvalidTitle=True)

            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_message(guildid, story_urls[0], message, isstory=True)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.file_prefix, guildid, storyurl, message,exc_info=1)
            raise e

    async def set_custom_message_for_author(self, guildid: str, authorurl:str, message:str) -> ResultCustomChannelSet:
        try:
            self.logger.info("%s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", self.file_prefix, guildid, authorurl, message)
            
            if not authorurl:
                category_result= await self.__set_custom_message_for_category(guildid, message, isstory=False, isauthor=True)

                if category_result.IsSuccess:
                    return Result(True, "Success")
                
                return Result(False, category_result.ResultInfo)

            author_urls= []         

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)

            else:
                author_urls.append(authorurl)

            if not author_urls:
                return ResultCustomChannelSet(False, "No Author found with the name", IsInvalidTitle=True)

            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple authors found with this name", HasMultipleResults=True)

                else:
                    result= await self.__set_custom_message(guildid, author_urls[0], message, isauthor=True, isstory=False)

                    if result.IsSuccess:
                        return ResultCustomChannelSet(True, "success")

                    
            return ResultCustomChannelSet(False, "Unknown error", UnknownError=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_author method invoked for author: %s, story: %s, msg: %s", self.file_prefix, guildid, authorurl, message,exc_info=1)
            raise e

    async def unset_custom_message_for_story(self, guildid: str, storyurl:str) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.unset_custom_message_for_story method invoked for server: %s, story: %s", self.file_prefix, guildid, storyurl)

            if not storyurl:
                category_result= await self.__unset_custom_message_for_category(guildid, isstory= True, isauthor= False)

                if category_result.IsSuccess:
                    return ResultCustomChannelSet(True, "success")

                elif category_result.Notfound:
                    return ResultCustomChannelUnset(False, "Custom msg not found for the story category", Notfound= True)

                return ResultCustomChannelUnset(False, "Unknown Error", UnknownError= True)


            story_urls= []     

            if self.prefix not in storyurl:
                story_urls= await self.__get_story_url_from_title(storyurl, guildid)

            else:
                story_urls.append(storyurl)

            if not story_urls:
                return ResultCustomChannelSet(False, "No story found with the title", IsInvalidTitle=True)

            else:
                if len(story_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple stories found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_message(guildid, story_urls[0], isstory=True)

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

            if not authorurl:
                category_result= await self.__unset_custom_message_for_category(guildid, isstory= False, isauthor= True)

                if category_result.IsSuccess:
                    return ResultCustomChannelSet(True, "success")

                elif category_result.Notfound:
                    return ResultCustomChannelUnset(False, "Custom msg not found for the author category", Notfound= True)

                return ResultCustomChannelUnset(False, "Unknown Error", UnknownError= True)

            author_urls= []       

            if self.prefix not in authorurl:
                author_urls= await self.__get_author_url_from_title(authorurl, guildid)
            
            else:
                author_urls.append(authorurl)

            if not author_urls:
                return ResultCustomChannelSet(False, "No author found with the title", IsInvalidTitle=True)

            else:
                if len(author_urls) > 1:
                    return ResultCustomChannelSet(False, "Multiple authors found with this title", HasMultipleResults=True)

                else:
                    result= await self.__unset_custom_message(guildid, author_urls[0], isstory=False, isauthor=True)

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

            if category:
                if category.lower() == Category.Announcements.value:
                    isauthor = True
                elif category.lower() == Category.Story.value:
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
                                story= await self.storyRepo.get_story_url_from_story_id(msg.StoryId, 1)

                                if story:
                                    story_custom_msg= CheckCustomMsgStory(story, msg.Message)

                                    story_custom_msgs.append(deepcopy(story_custom_msg))

                            elif not msg.AuthorId and msg.Type.lower() == CustomMsgType.Story.value.lower():
                                story_category_msg= CheckCustomMsgStory("Story Category:", msg.Message)

                                story_custom_msgs.append(deepcopy(story_category_msg))
                            
                        if not story_custom_msgs:
                            isempty= True

                    if isauthor:
                        #get Authors that are associated with this custom msg
                        for msg in custom_msgs:
                            if msg.AuthorId:
                                author= await self.authorRepo.get_author_url_from_author_id(msg.AuthorId, 1)

                                if author:
                                    author_custom_msg= CheckCustomMsgAuthor(author, msg.Message)

                                    author_custom_msgs.append(deepcopy(author_custom_msg))

                            elif not msg.StoryId and msg.Type.lower() == CustomMsgType.Author.value.lower():
                                author_category_msg= CheckCustomMsgStory("Announcement Category:", msg.Message)

                                author_custom_msgs.append(deepcopy(author_category_msg))
                            
                        if not story_custom_msgs and not author_custom_msgs:
                            isempty= True

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

                        # if len(custom_msg_id) > 1:
                        #     return ResultCustomChannelUnset(False, "Multiple custom msgs were found for same author id", HasMultipleResults=True)

                        # else:
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

                        # if len(custom_msg_id) > 1:
                        #     return ResultCustomChannelUnset(False, "Multiple custom msgs were found for same story id", HasMultipleResults=True)

                        # else:
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
                        #check if any custom msg exists for this author id
                        existing_custom_msg= await self.customMsgRepo.get_custom_msg_from_author_id(authorid, 1)

                        if existing_custom_msg:
                            #update the existing custom msg with the new one
                            update_result= await self.customMsgRepo.update_custom_msg_by_author_id(authorid, message, 1)

                            if update_result:
                                return Result(True, "success")
                            else:
                                return Result(False, "Error while updating the custom msg data")

                        else:
                            custommsg= CustomMsg(Type=CustomMsgType.Author.value, StoryId="", AuthorId=authorid, ServerId=serverid, IsActive=1, Message=message)

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
                        #check if any custom msg exists for this story id
                        existing_custom_msg= await self.customMsgRepo.get_custom_msg_from_story_id(storyid, 1)

                        if existing_custom_msg:
                            #update the existing custom msg with the new one
                            update_result= await self.customMsgRepo.update_custom_msg_by_story_id(storyid, message, 1)

                            if update_result:
                                return Result(True, "success")
                            else:
                                return Result(False, "Error while updating the custom msg data")

                        else:
                            custommsg= CustomMsg(Type=CustomMsgType.Story.value, StoryId=storyid, AuthorId="", ServerId=serverid, IsActive=1, Message=message)

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
        
    async def __set_custom_message_for_category(self, guildid: str, message: str, isstory: bool = True, isauthor: bool = False) -> Result:
        try:
            self.logger.info("%s.__set_custom_message_for_category method invoked for server: %s, msg: %s, is story: %s", self.file_prefix, guildid, message, isstory)
            
            #get server id for this server
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                if isauthor:
                    #check if there is a custom msg for this server
                    existing_custom_msg= await self.customMsgRepo.get_custom_msg_for_category(serverid, "a", 1)

                    if existing_custom_msg.Message:
                        #update the existing custom msg
                        update_result= await self.customMsgRepo.update_custom_msg_by_msg_id(existing_custom_msg.MsgId, message)

                        if update_result:
                                return Result(True, "success")
                        else:
                            return Result(False, "Error while updating the custom msg data")

                    else:
                        #insert custom msg data in to table
                        custommsg= CustomMsg(Type="a", Message=message, StoryId="", AuthorId="", ServerId=serverid, IsActive=1)

                        result= await self.customMsgRepo.insert_custom_msg_data(custommsg)

                        if result:
                            return Result(True, "success")
                        else:
                            return Result(False, "Error while inserting the custom msg data")

                else:
                    #check if there is a custom msg for this server
                    existing_custom_msg= await self.customMsgRepo.get_custom_msg_for_category(serverid, "s", 1)

                    if existing_custom_msg.Message:
                        #update the existing custom msg
                        update_result= await self.customMsgRepo.update_custom_msg_by_msg_id(existing_custom_msg.MsgId, message)

                        if update_result:
                                return Result(True, "success")
                        else:
                            return Result(False, "Error while updating the custom msg data")

                    else:
                        #insert custom msg data in to table
                        custommsg= CustomMsg(Type="s", Message=message, StoryId="", AuthorId="", ServerId=serverid, IsActive=1)

                        result= await self.customMsgRepo.insert_custom_msg_data(custommsg)

                        if result:
                            return Result(True, "success")
                        else:
                            return Result(False, "Error while inserting the custom msg data")

            else:
                return Result(False, "No server id found for the server")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__set_custom_message_for_category method invoked for server: %s, msg: %s, is story: %s", self.file_prefix, guildid, message, isstory,exc_info=1)
            raise e
        
    async def __unset_custom_message_for_category(self, guildid: str, isstory: bool= True, isauthor: bool= True) -> ResultCustomChannelUnset:
        try:
            self.logger.info("%s.__unset_custom_message_for_category method invoked for server: %s, is story: %s", self.file_prefix, guildid, isstory)

            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if serverid:
                if isauthor:
                    existing_custom_msg= await self.customMsgRepo.get_custom_msg_for_category(serverid, "a", 1)

                    if existing_custom_msg:
                        result= await self.customMsgRepo.delete_custom_msg_by_id(existing_custom_msg.MsgId)

                        if result:
                            return ResultCustomChannelUnset(True, "Success")

                        return ResultCustomChannelUnset(False, "Error while deleting custom msg", UnknownError= True)

                    else:
                        return ResultCustomChannelUnset(False, "Custom message not found for author category", Notfound= True)

                else:
                    existing_custom_msg= await self.customMsgRepo.get_custom_msg_for_category(serverid, "s", 1)

                    if existing_custom_msg:
                        result= await self.customMsgRepo.delete_custom_msg_by_id(existing_custom_msg.MsgId)

                        if result:
                            return ResultCustomChannelUnset(True, "Success")

                        return ResultCustomChannelUnset(False, "Error while deleting custom msg", UnknownError= True)

                    else:
                        return ResultCustomChannelUnset(False, "Custom message not found for story category", Notfound= True)

            else:
                return ResultCustomChannelUnset(False, "Error in getting server id")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__unset_custom_message_for_category method invoked for server: %s, is story: %s", self.file_prefix, guildid, isstory,exc_info=1)
            raise e
        


     #region misc methods
    async def __get_story_url_from_title(self, title:str, server:str) -> List[str]:
        try:
            self.logger.info("%s.__get_story_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server)

            #first get server id
            serverid= await self.serverRepo.get_serverid_from_server(server)

            if serverid:
                format_title=f"%{title}%"
                story_urls= await self.storyRepo.get_story_url_from_title(format_title.lower(), serverid=serverid)

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
                author_urls= await self.authorRepo.get_author_url_from_title(format_title.lower(), serverid=serverid)

                return author_urls

            return title
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server, exc_info=1)
            raise e
    
    #endregion
        