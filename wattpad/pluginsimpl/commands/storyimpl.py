from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import Result, ResultFollow
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.datautil import DataUtil
from datetime import datetime

class StoryImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.storyimpl"
        self.logger= BaseLogger().loggger_init()

    async def follow_story(self, guildId: str, url: str) -> Result:
        try:
            self.logger.info("%s.follow_story method invoked for story: %s", self.filePrefix, url)

            wattpadUtil = WattpadUtil()
            dataUtil = DataUtil()
            storyUrl = ""
            storyName = ""

            #check if the received url is valid
            validateStoryUrl = await wattpadUtil.validate_story_url(url)

            if not validateStoryUrl.IsSuccess:
                if validateStoryUrl.InvalidUrl:
                    return ResultFollow(False, "Story url pattern doesn't match", InvalidUrl=True, PatternMatched=False)

                else:
                    # try to get a url with pattern
                    storyUrl = await wattpadUtil.get_actual_story_url(url)

            else:
                storyUrl = url

            storyName = await wattpadUtil.get_story_title_from_url(storyUrl)

            #prepare story json data to insert
            storyData = {
                "url": storyUrl,
                "lastupdated": f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                "CustomChannel": "",
                "CustomMsg": "",
                "Error": {
                    "ErrorMsg": "",
                    "ErrorTime": ""
                }
            }

            #get stories data
            stories = await dataUtil.get_stories()

            if not stories or guildId not in stories:
                stories[guildId] = [
                    storyData
                ]
            
            else:
                for guild, story in stories:
                    if guild == guildId:
                        if any(storyUrl == data["url"] for data in story):

                            #Already following the story in the server
                            return ResultFollow(True, "Already following", InvalidUrl= False, AlreadyFollowing= True, storyName= storyName)

                        else:
                            #append new story data to existing data
                            story.append(storyData)
            
            #update the story data to json file
            result = await dataUtil.update_stories(stories)

            if result:
                return ResultFollow(True, "Story follow success", AlreadyFollowing= False, StoryName= storyName)

            return ResultFollow(UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_story method for story: %s", self.filePrefix, url, exc_info=1)
            raise e
        