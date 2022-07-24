from typing import List
from unittest import result
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import Result, ResultCheck, ResultStory, ResultUnfollow
from wattpad.utils.storyutil import StoryUtil
from wattpad.db.models.story import Story
from wattpad.db.models.server import Server
from wattpad.db.repository.serverrepo import ServerRepo

class StoryExec:
    def __init__(self) -> None:
        self.file_prefix="wattpad.pluginsexecution.commandsexec.storyexec"
        self.logger= BaseLogger().loggger_init()
        self.storyUtil= StoryUtil()
        self.serverRepo= ServerRepo()
        self.storyRepo= StoryRepo()
        self.prefix= "wattpad.com"

    async def follow_story(self, url:str, guildid:str) -> ResultStory:
        try:
            self.logger.info("%s.follow_story method invoked for story: %s", self.file_prefix, url)

            #check if the entered URL is a proper story URL
            validate_story= await self.storyUtil.validate_story_url(url)

            if not validate_story.IsSuccess:
                if validate_story.IsInvalidUrl:
                    return ResultStory(False, "Invalid URL", IsInvalidUrl=True)
                    
                else:
                    #try to get a proper story URl from the entered URL
                    storyUrl= await self.storyUtil.get_actual_story_url(url)

            else:
                storyUrl= url

            #get the data from server table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            #insert the data in to server table if no data is found
            if not serverid:
                server=Server(GuildId=guildid, IsActive=1)
                serverid= await self.serverRepo.insert_server_data(server)

            if serverid:
                #check if this story already exists in following list
                story_exits= await self.storyRepo.get_story_id_from_server_and_url(url=storyUrl, serverid=serverid, isactive=1)

                if not story_exits:
                    #insert the data in to story table
                    story= Story(Url=storyUrl, ServerId=serverid)

                    story_result= await self.storyRepo.insert_stories(story)

                    if story_result:
                        return ResultStory(True, "Success")

                    else:
                        return ResultStory(False, "Error with inserting story data")
                else:
                    return ResultStory(False, "Already following this story", AlreadyFollowing=True)
            
            else:
                return ResultStory(False, "Error in inserting server data")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_story method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e

    async def unfollow_story(self, url:str, guildid:str) -> ResultUnfollow:
        try:
            self.logger.info("%s.unfollow_story method invoked for url: %s, server: %s", self.file_prefix, url, guildid)

            story_url= ""

            if self.prefix not in url:
                #try to get the full story url from title
                story_url= await self.__get_story_url_from_title(url, guildid)

            else:
                story_url = url

            if not story_url:
                #invalid title
                return ResultUnfollow(False, "Invalid Title", IsInvalidTitle=True)
                
            else:
                #for unfollowing just make inactive as true but we need to delete the records completely
                if len(story_url) > 1:
                    return ResultUnfollow(False, "Multiple stories with the same title", HasMultipleStories=True )
                
                else:
                    #get server id from guildid
                    serverid= await self.serverRepo.get_serverid_from_server(guildid)

                    if not serverid:
                        return ResultUnfollow(False, "Error while getting server id", UnknownError=True)

                
                    #get story id from server and story url
                    storyid= await self.storyRepo.get_story_id_from_server_and_url(url=story_url[0], serverid=serverid)

                    if not storyid:
                        return ResultUnfollow(False, "Not following the story", NotFollowing=True)

                    #inactivate story by id
                    inactivate_result= await self.storyRepo.inactivate_story_by_id(storyid)

                    if inactivate_result:
                        return ResultUnfollow(True, "Success")

            return ResultUnfollow(False, "Unknown Error", UnknownError=True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.unfollow_story method invoked for url: %s, server: %s", self.file_prefix, url, guildid,exc_info=1)
            raise e

    async def check_stories(self, guildid:str) -> ResultCheck:
        try:
            self.logger.info("%s.check_stories method invoked for server: %s", self.file_prefix, guildid)

            #get server id from servers table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if not serverid:
                return ResultCheck(False, "Error while getting server id")

            else:
                #get stories from the server id
                stories= await self.storyRepo.get_stories_from_server_id(serverid, 1)

                if stories:
                    return ResultCheck(True, "success", Data=stories)

                else:
                    return ResultCheck(False, "No stories found", IsEmpty=True)
            

            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_stories method invoked for server: %s", self.file_prefix, guildid,exc_info=1)
            raise e
        

    #region misc methods
    async def __get_story_url_from_title(self, title:str, server:str) -> List[str]:
        try:
            self.logger.info("%s.get_story_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server)

            #first get server id
            serverid= await self.serverRepo.get_serverid_from_server(server)

            if serverid:
                format_title=f"%{title}%"
                story_urls= await self.storyRepo.get_story_url_from_title(format_title.lower(), serverid=serverid)

                return story_urls

            return title
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server, exc_info=1)
            raise e
    
    #endregion