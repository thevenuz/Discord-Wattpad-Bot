from unittest import result
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import Result, ResultStory
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
                #insert the data in to story table
                story= Story(Url=storyUrl, ServerId=serverid)

                story_result= await self.storyRepo.insert_stories(story)

                if story_result:
                    return ResultStory(True, "Success")

                else:
                    return ResultStory(False, "Error with inserting story data")
            
            else:
                return ResultStory(False, "Error in inserting server data")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_story method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e
        

