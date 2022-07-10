from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.meta.models.result import Result
from wattpad.db.models.channel import Channel
from wattpad.db.models.server import Server
from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.logger.baselogger import BaseLogger

class ChannelExec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.commandsexec.channelexec"
        self.logger= BaseLogger().loggger_init
        self.serverRepo= ServerRepo()
        self.channelRepo= ChannelRepo()

    async def set_channel(self, guildid:str, channelid:str) -> Result:
        try:
            self.logger.info("%s.set_channel method invoked for server: %s, channel: %s", self.file_prefix, guildid, channelid)

            #get the data from server table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            #insert the data in to server table if no data is found
            if not serverid:
                server=Server(GuildId=guildid, IsActive=1)
                serverid= await self.serverRepo.insert_server_data(server)

            if serverid:
                #insert the data in to channel table
                channel= Channel(channel=channelid, ServerId=serverid, IsActive=1, IsCustomChannel=0)
                
                channel_result= await self.channelRepo.insert_channel_data(channel)

                if channel_result:
                    return Result(True, "Success")

                else:
                    return Result(False, "Error with inserting channels data")
            
            else:
                return Result(False, "Error in inserting server data")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_channel method invoked for server: %s, channel: %s", self.file_prefix, guildid, channelid, exc_info=1)
            raise e
        
