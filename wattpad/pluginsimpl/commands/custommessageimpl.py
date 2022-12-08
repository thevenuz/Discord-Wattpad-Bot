from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import Result, ResultSetCustomChannel
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil

class CustomMessageImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.customchannelimpl"
        self.logger= BaseLogger().loggger_init()
        self.prefix = "wattpad.com"

    async def set_custom_message_for_story(self, guildId: str, url: str = "", message: str = "") -> ResultSetCustomChannel:
        try:
            self.logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.filePrefix, guildId, url, message)

            dataUtil = DataUtil()
            storyUrls = []

            #if there is a url, custom msg needs to be setup for individual stories
            if url:
                #load stories
                stories = await dataUtil.get_stories()

                filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

                if self.filePrefix not in url:
                    storyUrls = [story["url"] for story in filteredStories[guildId] if self.prefix in story["url"]]

                else:
                    storyUrls.append(url)
                
                #not following any story with that name/url
                if not storyUrls:
                    if self.prefix in url:
                        return ResultSetCustomChannel(False, "No story found", NoStoryFound= True)

                    else:
                        return ResultSetCustomChannel(False, "No story found with the title", NoStoryNameFound= True)

                else:
                    if len(storyUrls) > 1:
                        return ResultSetCustomChannel(False, "Mutliple stories found with this name", MultipleStoriesFound= True)

                    else:
                        for guild, storylist in filteredStories:
                            for story in storylist:
                                if storyUrls[0] == story["url"]:
                                    story["CustomMsg"] = message

                                    #update the orginal stories json data
                                    stories[guildId] = story

                                    result = await dataUtil.update_stories(stories)

                                    storyName = await WattpadUtil().get_story_title_from_url(url)

                                    if result:
                                        return ResultSetCustomChannel(True, "custom msg set success", StoryName= storyName)

                                    else:
                                        return ResultSetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

            #if there is no url set custom msg for whole story category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                messages[guildId]["story"] = message

                result = await dataUtil.update_messages(messages)

                storyName = await WattpadUtil().get_story_title_from_url(url)

                if result:
                    return ResultSetCustomChannel(True, "custom msg set success", StoryName= storyName)

                else:
                    return ResultSetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

            return ResultSetCustomChannel(False, "unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.filePrefix, guildId, url, message, exc_info=1)
            raise e
        