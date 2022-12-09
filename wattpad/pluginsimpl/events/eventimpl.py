from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.datautil import DataUtil

class EventImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.events.eventimpl"
        self.logger= BaseLogger().loggger_init()

    async def guild_join_event(self, guildId: str) -> bool:
        try:
            self.logger.info("%s.guild_join_event method invoked for server: %s", self.filePrefix, guildId)
            
            dataUtil = DataUtil()

            #load stories, channles, authors
            stories = await dataUtil.get_stories()
            authors = await dataUtil.get_authors()
            channels = await dataUtil.get_channels()

            stories[guildId] = []
            authors[guildId] = []
            channels[guildId] = []

            storyResult = await dataUtil.update_stories(stories)
            authorResult = await dataUtil.update_authors(authors)
            channelResult = await dataUtil.update_channels(channels)

            if not storyResult:
                self.logger("Error occured in %s.guild_join_event when updating stories for server: %s", self.filePrefix, guildId)
            
            if not authorResult:
                self.logger("Error occured in %s.guild_join_event when updating authors for server: %s", self.filePrefix, guildId)
            
            if not channelResult:
                self.logger("Error occured in %s.guild_join_event when updating channels for server: %s", self.filePrefix, guildId)

            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", self.filePrefix, guildId,exc_info=1)

    async def guild_leave_event(self, guildId: str) -> bool:
        try:
            self.logger.info("%s.guild_join_event method invoked for server: %s", self.filePrefix, guildId)

            dataUtil = DataUtil()

            #load stories, channles, authors
            stories = await dataUtil.get_stories()
            authors = await dataUtil.get_authors()
            channels = await dataUtil.get_channels()

            if guildId in stories:
                del stories[guildId]
                storyResult = await dataUtil.update_stories(stories)

                if not storyResult:
                    self.logger("Error occured in %s.guild_join_event when updating stories for server: %s", self.filePrefix, guildId)

            if guildId in authors:
                del authors[guildId]
                authorResult = await dataUtil.update_authors(authors)

                if not authorResult:
                    self.logger("Error occured in %s.guild_join_event when updating authors for server: %s", self.filePrefix, guildId)

            if guildId in channels:
                del channels[guildId]
                channelResult = await dataUtil.update_channels(channels)
                
                if not channelResult:
                    self.logger("Error occured in %s.guild_join_event when updating channels for server: %s", self.filePrefix, guildId)

            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", self.filePrefix, guildId, exc_info=1)
            raise e
        