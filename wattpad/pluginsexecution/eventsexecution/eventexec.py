import hikari
from wattpad.db.models.server import Server
from wattpad.logger.baselogger import BaseLogger
from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.db.repository.storyrepo import StoryRepo
from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.db.repository.custommsgrepo import CustomMsgrepo
from wattpad.db.repository.authorrepo import AuthorRepo

class Eventexec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.tasksexecution.taskexec"
        self.logger= BaseLogger().loggger_init()
        self.serverRepo= ServerRepo()
        self.storyRepo= StoryRepo()
        self.authorRepo= AuthorRepo()
        self.channelRepo= ChannelRepo()
        self.customMsgRepo= CustomMsgrepo()

    async def guild_join_event(self, guildId: str) -> None:
        try:
            self.logger.info("%s.guild_join_event method invoked for server: %s", self.file_prefix, guildId)

            #on guild join insert data in to server table
            server=Server(GuildId=guildId, IsActive=1)  
            result= await self.serverRepo.insert_server_data(server)  

            if not result:
                self.logger.fatal("Exception occured in %s.guild_join_event while inserting server data for server: %s", self.file_prefix, guildId)

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", self.file_prefix, guildId,exc_info=1)
            raise e
        
    async def guild_leave_event(self, guildId: str) -> None:
        try:
            self.logger.info("%s.guild_join_event method invoked for server: %s", self.file_prefix, guildId)

            #on guild leave event, deactivate everything related to this server and eventually delete this
            server_inactivate_result= await self.serverRepo.inactivate_server_from_guild_id(guildId)

            if not server_inactivate_result:
                self.logger.error("Error occured while inactivating server: %s", serverid)

            serverid= await self.serverRepo.get_serverid_from_server(guildId)

            stories= await self.storyRepo.get_stories_from_server_id(serverid, 1)
            authors= await self.authorRepo.get_authors_from_server_id(serverid, 1)

            story_inactivate_result= await self.storyRepo.inactivate_all_stories_by_server_id(serverid)
            author_inactivate_result= await self.authorRepo.inactivate_all_authors_by_server_id(serverid)

            if not story_inactivate_result:
                self.logger.error("Error occured while inactivating stories for server: %s", serverid)

            if not author_inactivate_result:
                self.logger.error("Error occured while inactivating authors for server: %s", serverid)

            for story in stories:
                custom_msg_id= await self.customMsgRepo.get_custom_msg_id_from_story_id(story.StoryId, 1)
                story_custom_msg_inactivate_result= await self.customMsgRepo.delete_custom_msg_by_id(custom_msg_id)

                if not story_custom_msg_inactivate_result:
                    self.logger.error("Error occured while inactivating story custom msg: %s", custom_msg_id)


            for author in authors:
                custom_msg_id= await self.customMsgRepo.get_custom_msg_id_from_author_id(author.AuthorId, 1)
                author_custom_msg_inactivate_result= await self.customMsgRepo.delete_custom_msg_by_id(custom_msg_id)

                if not author_custom_msg_inactivate_result:
                    self.logger.error("Error occured while inactivating author custom msg: %s", custom_msg_id)

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", self.file_prefix, guildId,exc_info=1)
            raise e
        