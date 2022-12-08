from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import Result, ResultSetCustomChannel, ResultUnsetCustomChannel
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
        
    async def set_custom_message_for_author(self, guildId: str, url: str = "", message: str = "") -> ResultSetCustomChannel:
        try:
            self.logger.info("%s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", self.filePrefix, guildId, url, message)

            dataUtil = DataUtil()
            authorUrls = []

            #if there is a url, custom msg needs to be setup for individual authors
            if url:
                #load authors
                authors = await dataUtil.get_authors()

                filterredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                if self.filePrefix not in url:
                    authorUrls = [author["url"] for author in filterredAuthors[guildId] if self.prefix in author["url"]]

                else:
                    authorUrls.append(url)
                
                #not following any author with that name/url
                if not authorUrls:
                    if self.prefix in url:
                        return ResultSetCustomChannel(False, "No author found", NoAuthorFound= True)

                    else:
                        return ResultSetCustomChannel(False, "No author found with the name", NoAuthorNameFound= True)

                else:
                    if len(authorUrls) > 1:
                        return ResultSetCustomChannel(False, "Mutliple stories found with this name", MultipleAuthorsFound= True)

                    else:
                        for guild, authorlist in filterredAuthors:
                            for author in authorlist:
                                if authorUrls[0] == author["url"]:
                                    author["CustomMsg"] = message

                                    #update the orginal stories json data
                                    authors[guildId] = author

                                    result = await dataUtil.update_authors(authors)

                                    authorName = await WattpadUtil().get_author_name(url)

                                    if result:
                                        return ResultSetCustomChannel(True, "custom msg set success", AuthorName= authorName)

                                    else:
                                        return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            #if there is no url set custom msg for whole author category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                messages[guildId]["announcement"] = message

                result = await dataUtil.update_messages(messages)

                authorName = await WattpadUtil().get_author_name(url)

                if result:
                    return ResultSetCustomChannel(True, "custom msg set success", AuthorName= authorName)

                else:
                    return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            return ResultSetCustomChannel(False, "unknown error", UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_custom_message_for_author method invoked for author: %s, story: %s, msg: %s", self.filePrefix, guildId, url, message, exc_info=1)
            raise e
        
    async def unset_custom_message_for_story(self, guildId: str, url:str) -> ResultUnsetCustomChannel:
        try:
            self.logger.info("%s.unset_custom_message_for_story method invoked for server: %s, story: %s", self.filePrefix, guildId, url)

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
                                    story["CustomMsg"] = ""

                                    #update the orginal stories json data
                                    stories[guildId] = story

                                    result = await dataUtil.update_stories(stories)

                                    storyName = await WattpadUtil().get_story_title_from_url(url)

                                    if result:
                                        return ResultUnsetCustomChannel(True, "custom msg unset success", StoryName= storyName)

                                    else:
                                        return ResultUnsetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

            #if there is no url set custom msg for whole story category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                messages[guildId]["story"] = ""

                result = await dataUtil.update_messages(messages)

                storyName = await WattpadUtil().get_story_title_from_url(url)

                if result:
                    return ResultUnsetCustomChannel(True, "custom msg unset success", StoryName= storyName)

                else:
                    return ResultUnsetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

            return ResultUnsetCustomChannel(False, "unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_custom_message_for_story method invoked for server: %s, story: %s", self.filePrefix, guildId, url,exc_info=1)
            raise e
        
    async def unset_custom_message_for_author(self, guildId: str, url:str) -> ResultUnsetCustomChannel:
        try:
            self.logger.info("%s.author method invoked for server: %s, author: %s", self.filePrefix, guildId, url)

            dataUtil = DataUtil()
            authorUrls = []

            #if there is a url, custom msg needs to be setup for individual authors
            if url:
                #load authors
                authors = await dataUtil.get_authors()

                filterredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                if self.filePrefix not in url:
                    authorUrls = [author["url"] for author in filterredAuthors[guildId] if self.prefix in author["url"]]

                else:
                    authorUrls.append(url)
                
                #not following any author with that name/url
                if not authorUrls:
                    if self.prefix in url:
                        return ResultSetCustomChannel(False, "No author found", NoAuthorFound= True)

                    else:
                        return ResultSetCustomChannel(False, "No author found with the name", NoAuthorNameFound= True)

                else:
                    if len(authorUrls) > 1:
                        return ResultSetCustomChannel(False, "Mutliple stories found with this name", MultipleAuthorsFound= True)

                    else:
                        for guild, authorlist in filterredAuthors:
                            for author in authorlist:
                                if authorUrls[0] == author["url"]:
                                    author["CustomMsg"] = ""

                                    #update the orginal stories json data
                                    authors[guildId] = author

                                    result = await dataUtil.update_authors(authors)

                                    authorName = await WattpadUtil().get_author_name(url)

                                    if result:
                                        return ResultSetCustomChannel(True, "custom msg unset success", AuthorName= authorName)

                                    else:
                                        return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            #if there is no url set custom msg for whole author category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                messages[guildId]["announcement"] = ""

                result = await dataUtil.update_messages(messages)

                authorName = await WattpadUtil().get_author_name(url)

                if result:
                    return ResultSetCustomChannel(True, "custom msg unset success", AuthorName= authorName)

                else:
                    return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            return ResultSetCustomChannel(False, "unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.author method invoked for server: %s, author: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e
        