class StoryUtil:
    def __init__(self) -> None:
        self.file_prefix = "wattpad.utils.storyutil"

    async def validate_story_url(self, storyUrl:str) -> bool:
        try:
            self.logger.info("%s.validate_story_url method invoked for story: %s", self.file_prefix, storyUrl)

            #need to check the URL pattern here
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.validate_story_url method invoked for story: %s", self.file_prefix, storyUrl, exc_info=1)
            raise e


    async def get_actual_story_url(self, storyUrl: str) -> str:
        try:
            self.logger.info("%s.get_actual_story_url method invoked for story: %s", self.file_prefix, storyUrl)

            #get the story URLs from chapter urls or remove utm tags
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_story_url method invoked for story: %s", self.file_prefix, storyUrl,exc_info=1)
            raise e
        
        