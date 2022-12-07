from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultSetCustomChannel, ResultUnsetCustomChannel, ResultCheckCustomChannel
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.msgutil import MsgUtil

class CustomChannelImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.customchannelimpl"
        self.logger= BaseLogger().loggger_init()
        self.prefix = "wattpad.com"

    async def set_custom_channel_for_story(self, guildId: str, channelId: str, url: str) -> ResultSetCustomChannel:
        try:
            self.logger.info("%s.set_custom_channel_for_story method invoked for server: %s, channel: %s, story url: %s", self.filePrefix, guildId, channelId, url)
            
            dataUtil = DataUtil()
            storyUrls = []

            #get stories
            stories = await dataUtil.get_stories()

            filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))
            
            if self.filePrefix not in url:
                storyUrls = [story["url"] for story in filteredStories[guildId] if self.prefix in story["url"]]

            else:
                storyUrls.append(url)

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
                                story["CustomChannel"] = channelId

                                #update the orginal stories json data
                                stories[guildId] = story

                                result = await dataUtil.update_stories(stories)

                                storyName = await WattpadUtil().get_story_title_from_url(url)

                                if result:
                                    return ResultSetCustomChannel(True, "custom channel set success", StoryName= storyName)

                                else:
                                    return ResultSetCustomChannel(False, "Error occured while updating stories", UnknownError= True)


            return ResultSetCustomChannel(False, "Unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_channel_for_story method invokedfor server: %s, channel: %s, story url: %s", self.filePrefix, guildId, channelId, url, exc_info=1)
            raise e
        
    async def set_custom_channel_for_author(self, guildId: str, channelId: str, url: str) -> ResultSetCustomChannel:
        try:
            self.logger.info("%s.set_custom_channel_for_author method invoked for server: %s, channel: %s, author url: %s", self.filePrefix, guildId, channelId, url)

            dataUtil = DataUtil()
            authorUrls = []

            #get authors
            authors = await dataUtil.get_authors()

            filteredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

            if self.filePrefix not in url:
                authorUrls = [author["url"] for author in filteredAuthors[guildId] if self.prefix in author["url"]]

            else:
                authorUrls.append(url)

            if not authorUrls:
                if self.prefix in url:
                    return ResultSetCustomChannel(False, "No Author found", NoAuthorFound= True)

                else:
                    return ResultSetCustomChannel(False, "No Author found with the name", NoAuthorNameFound= True)

            else:
                if len(authorUrls) > 1:
                    return ResultSetCustomChannel(False, "Mutliple Authors found with this name", MultipleAuthorsFound= True)

                else:
                    for guild, authorList in filteredAuthors:
                        for author in authorList:
                            if authorUrls[0] == author["url"]:
                                author["CustomChannel"] = channelId

                                #update the orginal authors json data
                                authors[guildId] = author

                                result = await dataUtil.update_stories(authors)

                                authorName = await WattpadUtil().get_author_name(url)

                                if result:
                                    return ResultSetCustomChannel(True, "custom channel set success", AuthorName= authorName)

                                else:
                                    return ResultSetCustomChannel(False, "Error occured while updating Authors", UnknownError= True)


                    
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_channel_for_author method invokedfor server: %s, channel: %s, author url: %s", self.filePrefix, guildId, channelId, url, exc_info=1)
            raise e
        
    async def unset_custom_channel_for_story(self, guildId:str, channelId:str, url: str) -> ResultUnsetCustomChannel:
        try:
            self.logger.info("%s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, story: %s", self.filePrefix, guildId, channelId, url)

            dataUtil = DataUtil()
            storyUrls = []

            #get stories
            stories = await dataUtil.get_stories()

            filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

            if self.filePrefix not in url:
                storyUrls = [story["url"] for story in filteredStories[guildId] if self.prefix in story["url"]]

            else:
                storyUrls.append(url)

            if not storyUrls:
                if self.prefix in url:
                    return ResultUnsetCustomChannel(False, "No story found", NoStoryFound= True)
                else:
                    return ResultUnsetCustomChannel(False, "No story found with the title", NoStoryNameFound= True)

            else:
                if len(storyUrls) > 1:
                    return ResultUnsetCustomChannel(False, "Mutliple stories found with this name", MultipleStoriesFound= True)

                else:
                    for guild, storylist in filteredStories:
                        for story in storylist:
                            if storyUrls[0] == story["url"]:
                                story["CustomChannel"] = ""

                                #update the orginal stories json data
                                stories[guildId] = story

                                result = await dataUtil.update_stories(stories)

                                storyName = await WattpadUtil().get_story_title_from_url(url)

                                if result:
                                    return ResultSetCustomChannel(True, "custom channel set success", StoryName= storyName)

                                else:
                                    return ResultSetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, story: %s", self.filePrefix, guildId, channelId, url, exc_info=1)
            raise e

    async def unset_custom_channel_for_author(self, guildId:str, channelId:str, url: str) -> ResultUnsetCustomChannel:
        try:
            self.logger.info("%s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, author: %s", self.filePrefix, guildId, channelId, url)

            dataUtil = DataUtil()
            authorUrls = []

            #get authors
            authors = await dataUtil.get_authors()

            filteredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

            if self.filePrefix not in url:
                authorUrls = [author["url"] for author in filteredAuthors[guildId] if self.prefix in author["url"]]

            else:
                authorUrls.append(url)

            if not authorUrls:
                if self.prefix in url:
                    return ResultSetCustomChannel(False, "No Author found", NoAuthorFound= True)

                else:
                    return ResultSetCustomChannel(False, "No Author found with the name", NoAuthorNameFound= True)

            else:
                if len(authorUrls) > 1:
                    return ResultSetCustomChannel(False, "Mutliple Authors found with this name", MultipleAuthorsFound= True)

                else:
                    for guild, authorList in filteredAuthors:
                        for author in authorList:
                            if authorUrls[0] == author["url"]:
                                author["CustomChannel"] = ""

                                #update the orginal authors json data
                                authors[guildId] = author

                                result = await dataUtil.update_stories(authors)

                                authorName = await WattpadUtil().get_author_name(url)

                                if result:
                                    return ResultSetCustomChannel(True, "custom channel unset success", AuthorName= authorName)

                                else:
                                    return ResultSetCustomChannel(False, "Error occured while updating Authors", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, author: %s", self.filePrefix, guildId, channelId, url, exc_info=1)
            raise e
        
    async def check_custom_channels(self, guildId: str, category: str = "") -> ResultCheckCustomChannel:
        try:
            self.logger.info("%s.check_custom_channels method invoked for server: %s, category: %s", self.filePrefix, guildId, category)

            isauthor=False
            isstory=False
            isStoryEmpty= False
            isAuthorEmpty= False

            dataUtil = DataUtil()
            msgUtil = MsgUtil()

            if category:
                if category.lower() == "story":
                    isstory = True
                elif category.lower() == "announcements":
                    isauthor = True
                else:
                    isauthor= True
                    isstory= True

            else:
                isauthor= True
                isstory= True

            if isstory:
                #get stories
                stories = await dataUtil.get_stories()

                guildStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

                customChannelStories = [story for story in guildStories[guildId] if story["CustomChannel"]]

                storyMsgResult = await msgUtil.build_check_custom_channel_msg(customChannelStories, isStory= True)

                if not storyMsgResult:
                    isStoryEmpty = True

            if isauthor:
                #get authors
                authors = await dataUtil.get_authors()

                guildAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                customChannelStories = [author for author in guildAuthors[guildId] if author["CustomChannel"]]

                authorMsgResult = await msgUtil.build_check_custom_channel_msg(customChannelStories, isAuthor= True)

                if not authorMsgResult:
                    isAuthorEmpty = True

            if isStoryEmpty and isAuthorEmpty:
                return ResultCheckCustomChannel(False, "No custom channels set", IsEmpty= True)

            if isauthor and isAuthorEmpty:
                return ResultCheckCustomChannel(False, "No custom channels set for Author", IsEmpty= True)

            if isstory and isStoryEmpty:
                return ResultCheckCustomChannel(False, "No custom channels set for stories", IsEmpty= True)


            return ResultCheckCustomChannel(True, "check custom channel success", AuthorMsg= authorMsgResult, StoryMsg= storyMsgResult)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_custom_channels method invoked for server: %s, category: %s", self.filePrefix, guildId, category,exc_info=1)
            raise e
        
    