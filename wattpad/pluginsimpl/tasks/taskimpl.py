import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.datautil import DataUtil
from wattpad.utils.wattpadutil import WattpadUtil
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

            #load stories
            stories = await dataUtil.get_stories()

            filteredStories = {guild: story for guild, story in stories.items() if story}

            for guild, storyList in filteredStories.items():
                nonEmptyStories = [rec for rec in storyList if rec["url"]]

                for storyRec in nonEmptyStories[0]:
                    #check if any custom channels are set for this story
                    customChannel = storyRec["CustomChannel"]
                    channel = customChannel

                    if not customChannel:
                        #load channels
                        channels = await dataUtil.get_channels()
                        defaultChannel = channels[guild][0]

                        channel = defaultChannel

                    #check for updates of the story only if there is a channel setup for updates
                    if channel:
                        #check for the chapter update for story
                        update = await scraper.get_new_chapter(storyRec["url"], storyRec["lastupdated"])

                        if update.IsSuccess:
                            #check if any custom msg were set for this story
                            customMsg = storyRec["CustomChannel"]
                            msg = customMsg

                            #if no custom msgs set get default msg
                            if not customMsg:
                                language = await config.get_language(guild)
                                msgs = await config.get_messages(language)

                                msg = msgs['new:chapter:msg']

                            
                            #get story title
                            title = await wattpadUtil.get_story_title_from_url(storyRec["url"])

                            response = msg.format(f"{title}")
                            response= response + "\n" + update.NewUpdate

                            await plugin.bot.rest.create_message(channel, response)

                    else:
                        self.logger.error("Error: no channel for updates is setup for server: %s, story: %s", guild, storyRec["url"])
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_chapters method", self.filePrefix, exc_info=1)
            raise e
        