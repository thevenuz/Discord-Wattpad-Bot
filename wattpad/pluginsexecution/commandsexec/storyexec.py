from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.storyutil import StoryUtil

class StoryExec:
    def __init__(self) -> None:
        self.file_prefix="wattpad.pluginsexecution.commandsexec.storyexec"
        self.logger= BaseLogger().loggger_init()
        self.storyUtil= StoryUtil()

    async def follow_story(self, url:str) -> str:
        try:
            self.logger.info("%s.follow_story method invoked for story: %s", self.file_prefix, url)

            #check if the entered URL is a proper story URL
            validate_story= await self.storyUtil.validate_story_url(url)

            if not validate_story:
                #try to get a proper story URl from the entered URL
                storyUrl= await self.storyUtil.get_actual_story_url(url)

            
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_story method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e
        

