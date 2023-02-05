import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.hikariutil import HikariUtil
from wattpad.scraper.scraper import Scraper
from wattpad.utils.config import Config

class TaskImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.tasks.tasksimpl"
        self.logger= BaseLogger().loggger_init()

    async def get_new_chapters(self, plugin: lightbulb.Plugin) -> None:
        try:
            self.logger.info("%s.get_new_chapters method invoked", self.filePrefix)

            dataUtil = DataUtil()
            scraper = Scraper()
            config = Config()
            wattpadUtil = WattpadUtil()
            channel = ""
            msg = ""
            customChannel = ""
            customMsg = ""
            hasSendPerms = False

            #load stories
            stories = await dataUtil.get_stories()

            filteredStories = {guild: story for guild, story in stories.items() if story}

            for guild, storyList in filteredStories.items():
                try:
                    nonEmptyStories = [rec for rec in storyList if rec["url"]]

                    for storyRec in nonEmptyStories:
                        #check if any custom channels are set for this story
                        if "CustomChannel" in storyRec:
                            customChannel = storyRec["CustomChannel"]
                            channel = customChannel

                        if not customChannel:
                            #load channels
                            channels = await dataUtil.get_channels()

                            if guild in channels and channels[guild]:
                                defaultChannel = channels[guild][0]

                                channel = defaultChannel

                        #check for updates of the story only if there is a channel setup for updates
                        if channel:
                            #check if the bot has send msg perms in this channel
                            hasSendPerms = await self.__has_send_perms(plugin, guild, channel)

                            if hasSendPerms:
                                #check for the chapter update for story
                                update = await scraper.get_new_chapter(storyRec["url"], storyRec["lastupdated"])

                                if update.IsSuccess:
                                    #check if any custom msg were set for this story
                                    if "CustomMsg" in storyRec:
                                        customMsg = storyRec["CustomMsg"]
                                        msg = customMsg

                                    # If specific custom msg is not found for story, check custom msgs for category
                                    if not customMsg:
                                        categoryCustomMsgs = await dataUtil.get_messages()

                                        if guild in categoryCustomMsgs and "story" in categoryCustomMsgs[guild]:
                                            msg = categoryCustomMsgs[guild]["story"]


                                    #if no custom msgs set get default msg
                                    if not msg:
                                        language = await config.get_language(guild)
                                        msgs = await config.get_messages(language)

                                        msg = msgs['new:chapter:msg']

                                    
                                    #get story title
                                    title = await wattpadUtil.get_story_title_from_url(storyRec["url"])

                                    response = msg.format(f"{title}")
                                    response= response + "\n" + update.NewUpdate

                                    await plugin.bot.rest.create_message(channel, response)

                                    #update lastupdated in stories
                                    for eachStory in stories[guild]:
                                        if eachStory["url"] == storyRec["url"]:
                                            eachStory["lastupdated"] = update.UpdatedDate.strftime("%Y-%m-%d %H:%M:%S")

                                            updateResult = await dataUtil.update_stories(stories)

                                            if not updateResult:
                                                self.logger.error("%s.get_new_chapters Error while updating stories for server: %s, story: %s", self.filePrefix, guild, storyRec["url"])

                            else:
                                self.logger.error("Error %s.get_new_chapters method: no send permissions for channel: %s, server: %s, story: %s", self.filePrefix, channel, guild, storyRec["url"])

                        else:
                            self.logger.error("Error %s.get_new_chapters: no channel for updates is setup for server: %s, story: %s", self.filePrefix, guild, storyRec["url"])
                
                except Exception as e:
                    self.logger.error("Error occured in %s.get_new_chapters method", self.filePrefix, exc_info=1)
                    pass

            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_chapters method", self.filePrefix, exc_info=1)
            return False

    async def get_new_announcements(self, plugin: lightbulb.Plugin) -> None:
        try:
            self.logger.info("%s.get_new_announcements method invoked", self.filePrefix) 

            dataUtil = DataUtil()
            scraper = Scraper()
            config = Config()
            wattpadUtil = WattpadUtil()
            channel = ""
            msg = ""
            customChannel = ""
            customMsg = ""

            #load authors
            authors = await dataUtil.get_authors()

            filteredAuthors = {guild: author for guild, author in authors.items() if author}

            for guild, authorList in filteredAuthors.items():
                try:
                    nonEmptyAuthors = [rec for rec in authorList if rec["url"]]

                    for authorRec in nonEmptyAuthors:
                        #check if any custom channels are set for this author
                        if "CustomChannel" in authorRec:
                            customChannel = authorRec["CustomChannel"]
                            channel = customChannel

                        if not customChannel:
                            #load channels
                            channels = await dataUtil.get_channels()
                            if guild in channels and channels[guild]:
                                defaultChannel = channels[guild][0]

                                channel = defaultChannel

                        #check for updates of the author only if there is a channel setup for updates
                        if channel:
                            #check if the bot has send msg perms in this channel
                            hasSendPerms = await self.__has_send_perms(plugin, guild, channel)

                            if hasSendPerms:
                                #check for the announcement update for author
                                update = await scraper.get_new_announcement(authorRec["url"], authorRec["lastupdated"])

                                if update.IsSuccess:
                                    #check if any custom msg were set for this author
                                    if "CustomMsg" in authorRec:
                                        customMsg = authorRec["CustomMsg"]
                                        msg = customMsg

                                    # If specific custom msg is not found for announcement, check custom msgs for category
                                    if not customMsg:
                                        categoryCustomMsgs = await dataUtil.get_messages()

                                        if guild in categoryCustomMsgs and "announcement" in categoryCustomMsgs[guild]:
                                            msg = categoryCustomMsgs[guild]["announcement"]

                                    #if no custom msgs set get default msg
                                    if not msg:
                                        language = await config.get_language(guild)
                                        msgs = await config.get_messages(language)

                                        msg = msgs['new:announcement:msg']

                                    #get story title
                                    title = await wattpadUtil.get_author_name(authorRec["url"])

                                    response = msg.format(f"{title}")
                                    #response= response + "\n" + update.NewUpdate

                                    em = hikari.Embed(title='Announcement:', description=f'{update.NewUpdate}', color=0Xff500a)

                                    await plugin.bot.rest.create_message(channel, response, embed = em)

                                    #update lastupdated in authors
                                    for eachAuthor in authors[guild]:
                                        if eachAuthor["url"] == authorRec["url"]:
                                            eachAuthor["lastupdated"] = update.UpdatedDate.strftime("%Y-%m-%d %H:%M:%S")

                                            updateResult = await dataUtil.update_authors(authors)

                                            if not updateResult:
                                                self.logger.error("%s.get_new_chapters Error while updating authors for server: %s, author: %s", self.filePrefix, guild, authorRec["url"])

                            else:
                                self.logger.error("Error in %s.get_new_announcements method: no send permissions for channel: %s, server: %s, author: %s", self.filePrefix, channel, guild, authorRec["url"])
                        else:
                            self.logger.error("Error in %s.get_new_announcements method: no channel for updates is setup for server: %s, author: %s", self.filePrefix, guild, authorRec["url"])

                except Exception as e:
                    self.logger.error("Error occured in %s.get_new_announcements method", self.filePrefix, exc_info=1)
                    pass

            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_announcements invoked", self.filePrefix, exc_info=1)
            return False
        
    async def __has_send_perms(self, plugin: lightbulb.Plugin, guild: str, channel: str) -> bool:
        try:
            self.logger.info("%s.__has_send_perms method invoked for channel: %s", self.filePrefix, channel)

            try:
                channelobj= await plugin.bot.rest.fetch_channel(channel)
                guildObj = await plugin.bot.rest.fetch_guild(guild)
                bot_member = guildObj.get_member(plugin.bot.get_me())
                # bot_member= plugin.bot.cache.get_member(guild, plugin.bot.get_me())

                perms= lightbulb.utils.permissions_in(channelobj, bot_member)

                if perms:
                    if hikari.Permissions.SEND_MESSAGES in perms:
                        return True

                return False

            except Exception as e:
                return False
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__has_send_perms method for channel: %s", self.filePrefix, channel, exc_info=1)
            raise e
        