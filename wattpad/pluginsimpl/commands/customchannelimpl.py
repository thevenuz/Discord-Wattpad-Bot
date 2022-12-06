from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultSetCustomChannel, ResultUnsetCustomChannel
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil

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
        
        