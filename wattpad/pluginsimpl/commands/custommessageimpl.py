from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import Result, ResultSetCustomChannel, ResultUnsetCustomChannel, ResultCheckCustomChannel
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.msgutil import MsgUtil

class CustomMessageImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.custommessageimpl"
        self.logger= BaseLogger().loggger_init()
        self.prefix = "wattpad.com"

    async def set_custom_message_for_story(self, guildId: str, url: str = "", message: str = "") -> ResultSetCustomChannel:
        try:
            self.logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", self.filePrefix, guildId, url, message)

            dataUtil = DataUtil()
            storyUrls = []
            storyName = ""

            #if there is a url, custom msg needs to be setup for individual stories
            if url:
                #load stories
                stories = await dataUtil.get_stories()

                filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

                if self.prefix not in url:
                    storyUrls = [story["url"] for story in filteredStories[guildId] if url in story["url"]]

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
                        for guild, storylist in filteredStories.items():
                            for story in storylist:
                                if storyUrls[0] == story["url"]:
                                    story["CustomMsg"] = message

                                    #update the orginal stories json data
                                    stories[guildId] = storylist

                                    result = await dataUtil.update_stories(stories)

                                    if self.prefix in url:
                                        storyName = await WattpadUtil().get_story_title_from_url(url)
                                    else:
                                        storyName = url

                                    if result:
                                        return ResultSetCustomChannel(True, "custom msg set success", StoryName= storyName)

                                    else:
                                        return ResultSetCustomChannel(False, "Error occured while updating stories", UnknownError= True)

            #if there is no url set custom msg for whole story category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                if guildId in messages:
                    if "story" in messages[guildId]:
                        messages[guildId]["story"] = message

                    else:
                        messages[guildId] = {
                            "story" : message,
                            "announcement" : ""
                        }

                else:
                    messages[guildId] = {
                        "story" : message,
                        "announcement" : ""
                    }

                result = await dataUtil.update_messages(messages)

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
            authorName = ""

            #if there is a url, custom msg needs to be setup for individual authors
            if url:
                #load authors
                authors = await dataUtil.get_authors()

                filteredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                if self.prefix not in url:
                    authorUrls = [author["url"] for author in filteredAuthors[guildId] if url in author["url"]]

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
                        for guild, authorlist in filteredAuthors.items():
                            for author in authorlist:
                                if authorUrls[0] == author["url"]:
                                    author["CustomMsg"] = message

                                    #update the orginal stories json data
                                    authors[guildId] = authorlist

                                    result = await dataUtil.update_authors(authors)

                                    if self.prefix in url:
                                        authorName = await WattpadUtil().get_author_name(url)
                                    else:
                                        authorName = url

                                    if result:
                                        return ResultSetCustomChannel(True, "custom msg set success", AuthorName= authorName)

                                    else:
                                        return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            #if there is no url set custom msg for whole author category
            else:
                #get messages
                messages = await dataUtil.get_messages()

                if guildId in messages:
                    if "announcement" in messages[guildId]:
                        messages[guildId]["announcement"] = message

                    else:
                        messages[guildId] = {
                            "story" : "",
                            "announcement" : message
                        }

                else:
                    messages[guildId] = {
                        "story" : "",
                        "announcement" : message
                    }

                result = await dataUtil.update_messages(messages)

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
            storyName = ""

            #if there is a url, custom msg needs to be setup for individual stories
            if url:
                #load stories
                stories = await dataUtil.get_stories()

                filteredStories = dict(filter(lambda x: x[0] == guildId, stories.items()))

                if self.prefix not in url:
                    storyUrls = [story["url"] for story in filteredStories[guildId] if url in story["url"]]

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
                        for guild, storylist in filteredStories.items():
                            for story in storylist:
                                if storyUrls[0] == story["url"]:
                                    story["CustomMsg"] = ""

                                    #update the orginal stories json data
                                    stories[guildId] = storylist

                                    result = await dataUtil.update_stories(stories)

                                    if self.prefix in url:
                                        storyName = await WattpadUtil().get_story_title_from_url(url)
                                    else:
                                        storyName = url

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
            authorName = ""

            #if there is a url, custom msg needs to be setup for individual authors
            if url:
                #load authors
                authors = await dataUtil.get_authors()

                filteredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                if self.prefix not in url:
                    authorUrls = [author["url"] for author in filteredAuthors[guildId] if url in author["url"]]

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
                        for guild, authorlist in filteredAuthors.items():
                            for author in authorlist:
                                if authorUrls[0] == author["url"]:
                                    author["CustomMsg"] = ""

                                    #update the orginal authors json data
                                    authors[guildId] = authorlist

                                    result = await dataUtil.update_authors(authors)

                                    if self.prefix in url:
                                        authorName = await WattpadUtil().get_author_name(url)
                                    else:
                                        authorName = url

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

                if result:
                    return ResultSetCustomChannel(True, "custom msg unset success", AuthorName= authorName)

                else:
                    return ResultSetCustomChannel(False, "Error occured while updating authors", UnknownError= True)

            return ResultSetCustomChannel(False, "unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.author method invoked for server: %s, author: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e
        
    async def check_custom_messages(self, guildId:str, category:str) -> ResultCheckCustomChannel:
        try:
            self.logger.info("%s.check_custom_messages method invoked for server: %s, category: %s", self.filePrefix, guildId, category)

            isauthor=False
            isstory=False
            isStoryEmpty= False
            isAuthorEmpty= False
            authorMsgResult = ""
            storyMsgResult = ""
            authorCategoryMsg = ""
            storyCategoryMsg = ""

            dataUtil = DataUtil()
            msgUtil = MsgUtil()

            messages = await dataUtil.get_messages()

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

                customMsgStories = [story for story in guildStories[guildId] if "CustomMsg" in story and story["CustomMsg"]]
                
                if guildId in messages:
                    storyCategoryMsg = messages[guildId]["story"]

                storyMsgResult = await msgUtil.build_check_custom_messages_msg(customMsgStories, isStory= True)

                if not storyMsgResult and not storyCategoryMsg:
                    isStoryEmpty = True

            if isauthor:
                #get authors
                authors = await dataUtil.get_authors()

                guildAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

                customMsgStories = [author for author in guildAuthors[guildId] if "CustomMsg" in author and author["CustomMsg"]]

                if guildId in messages:
                    authorCategoryMsg = messages[guildId]["announcement"]

                authorMsgResult = await msgUtil.build_check_custom_messages_msg(customMsgStories, isAuthor= True)

                if not authorMsgResult and not authorCategoryMsg:
                    isAuthorEmpty = True

            if isStoryEmpty and isAuthorEmpty:
                return ResultCheckCustomChannel(False, "No custom msgs set", IsEmpty= True)

            if isauthor and isAuthorEmpty and not isstory:
                return ResultCheckCustomChannel(False, "No custom msgs set for Author", IsEmpty= True)

            if isstory and isStoryEmpty and not isauthor:
                return ResultCheckCustomChannel(False, "No custom msgs set for stories", IsEmpty= True)


            return ResultCheckCustomChannel(True, "check custom msgs success", AuthorMsg= authorMsgResult, StoryMsg= storyMsgResult, AuthorCategoryMsg= authorCategoryMsg, StoryCategoryMsg= storyCategoryMsg)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_custom_messages method invoked for server: %s, category: %s", self.filePrefix, guildId, category, exc_info=1)
            raise e
        