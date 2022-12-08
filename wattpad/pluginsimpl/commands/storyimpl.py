from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultFollow, ResultUnfollow, ResultCheck
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.datautil import DataUtil
from datetime import datetime

class StoryImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.storyimpl"
        self.logger= BaseLogger().loggger_init()

    async def follow_story(self, guildId: str, url: str) -> ResultFollow:
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
        
    async def unfollow_story(self, guildId: str, url: str) -> ResultUnfollow:
        try:
            self.logger.info("%s.unfollow_story method invoked for server: %s, story: %s", self.filePrefix, guildId, url)

            isStoryName = False
            dataUtil = DataUtil()
            storyUrl = url
        
            if "/story/" not in url:
                isStoryName = True

            #get stories
            stories = await dataUtil.get_stories()

            #filter the stories of the particular guild
            filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

            for guild, story in filteredStories:
                if guild == guildId:
                    #get url if entered input is story name
                    if isStoryName:
                        if any(url in (foundurl := rec["url"]) for rec in story):
                            storyUrl = foundurl

                        else:
                            #url with the story name not found
                            return ResultUnfollow(False, "Url with Story name not found", StoryNameNotFound= True)

                    if any(storyUrl == rec["url"] for rec in story):
                        for rec in story:
                            if storyUrl == rec["url"]:
                                story.remove(rec)

                                #update the original sories json data
                                stories[guildId] = story

                                #update the stories data to json file
                                result = await dataUtil.update_stories(stories)

                                if result:
                                    return ResultUnfollow(True, "Story unfollowed")

                                self.logger.error("%s.unfollow_story method: unknown error occured when updating stories", self.filePrefix)
                                return ResultUnfollow(False, "Unknown error", UnknownError= True)

                    else:
                        #no story found with the url
                        return ResultUnfollow(False, "Story not found", StoryNotFound= True)

                return ResultUnfollow(False, "Unknown error", UnknownError= True)
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unfollow_story methodfor server: %s, story: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e
        
    async def check_stories(self, guildId: str) -> ResultCheck:
        try:
            self.logger.info("%s.check_stories method invoked for server: %s", self.filePrefix, guildId)

            #get stories
            stories = await DataUtil().get_stories()

            filteredStories = [story for guild, story in stories.items() if guild == guildId]

            return ResultCheck(True, "check stories success", Data= filteredStories)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_stories method invoked for server: %s", self.filePrefix, guildId, exc_info=1)
            raise e
        