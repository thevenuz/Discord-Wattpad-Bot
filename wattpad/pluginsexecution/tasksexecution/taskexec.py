from datetime import datetime
import hikari
import lightbulb
from wattpad.db.models.story import Story
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import Result, ResultNewUpdate
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.db.repository.custommsgrepo import CustomMsgrepo
from wattpad.scraper.scraper import Scraper
from wattpad.utils.hikariutil import HikariUtil
from wattpad.utils.config import Config
from wattpad.utils.storyutil import StoryUtil

class TaskExec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.tasksexecution.taskexec"
        self.logger= BaseLogger().loggger_init()
        self.storyRepo= StoryRepo()
        self.channelRepo= ChannelRepo()
        self.customMsgRepo= CustomMsgrepo()
        self.scraper= Scraper()
        self.storyUtil= StoryUtil()

    async def get_new_chapters(self, plugin: lightbulb.Plugin) -> None:
        try:
            self.logger.info("%s.get_new_chapters method invoked", self.file_prefix)

            #get all the active stories
            stories= await self.storyRepo.get_active_stories(1)

            if stories:
                for story in stories:
                    #check for new chapters from this story
                    new_chapter_result= await self.scraper.get_new_chapter(story.Url, story.LastUpdatedOn)

                    if new_chapter_result.IsSuccess:
                        #trigger the update message
                        result= await self.__trigger_message_for_story(plugin, story, new_chapter_result)

                        if result:
                            #update the lastupdatedon datetime in db
                            update_result= await self.storyRepo.update_last_updated_date_for_story_id(story.StoryId, new_chapter_result.UpdatedDate)

                            if not update_result:
                                self.logger.fatal("Error occured in %s.get_new_chapters method while updating lastupdated date in stories for story id: %s, lastupdate: %s", self.file_prefix, story.StoryId, new_chapter_result.UpdatedDate)

                        else:
                            self.logger.fatal("Some error occured in %s.get_new_chapters while sending chapter update for story: %s, chapter: %s", self.file_prefix, story.Url, new_chapter_result.NewUpdate )

                    
                    #update the last checked date
                    update_last_checked= await self.storyRepo.update_last_checked_date_for_story_id(story.StoryId, datetime.utcnow())

                    if not update_last_checked:
                        self.logger.fatal("Error occured in %s.get_new_chapters method while updating last checked date in stories for story id: %s", self.file_prefix, story.StoryId)

                else:
                    self.logger.fatal("No active stories found")
            
            self.logger.info("get new chapters task ended")

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_chapters method", self.file_prefix, exc_info=1)
            pass

    async def __trigger_message_for_story(self, plugin:lightbulb.Plugin, story:Story, result:ResultNewUpdate) -> bool:
        try:
            self.logger.info("%s.__trigger_message_for_story method invoked for story: %s, new chapter: %s", self.file_prefix, story.Url, result.NewUpdate)

            has_custom_channel= 0

            #check if there is a custom channel for this story
            custom_channel_id= await self.storyRepo.get_custom_channel_id_from_story_id(storyid=story.StoryId, isactive= 1)

            if custom_channel_id:
                channel_id= custom_channel_id
                has_custom_channel= 1
            
            else:
                #get the common channel for this server id
                channel_id= await self.channelRepo.get_channel_id_from_server_id(story.ServerId, 1)

            if channel_id:
                #get the discord channel id
                channel= await self.channelRepo.get_channel_from_channel_id(channel_id, 1, has_custom_channel)

                #check if there are any custom msgs
                custom_msg= await self.customMsgRepo.get_custom_msg_from_story_id(story.StoryId, 1)

                if custom_msg:
                    msg= custom_msg

                else:
                    msgs= await Config().get_messages("en")
                    msg= msgs['new:chapter:msg']

                if channel:
                    story_title= await self.__get_story_title_from_url(story.Url)
                    msg_content= msg.format(f"{story_title}")

                    await plugin.bot.rest.create_message(channel, msg_content)

                    return True
                else:
                    self.logger.error("Unknown error occured while getting channel from channel id: %s", channel_id)

            else:
                self.logger.error("Error in %s.__trigger_message_for_story method - no channel id found for server: %s, story id: %s", self.file_prefix, story.ServerId, story.StoryId)

            return False

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__trigger_message_for_story method invoked for story: %s, new chapter: %s", self.file_prefix, story.Url, result.NewUpdate,exc_info=1)
            return False
        
        
    async def __get_story_title_from_url(self, url:str) -> str:
        try:
            self.logger.info("%s.__get_story_title_from_url method invoked for story: %s", self.file_prefix, url)

            if "utm" in url:
                url= await self.storyUtil.__get_story_url_from_utm(url)

            storytitle= str(url).split('/')
            title= storytitle[-1].split('-',1)
            title= title[-1].replace('-',' ')

            return title
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_title_from_url method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e
        