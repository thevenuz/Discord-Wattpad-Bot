from wattpad.db.repository.channelrepo import ChannelRepo
from wattpad.meta.models.result import Result, ResultCheck, ResultUnset
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
        
    async def unset_channel(self, guildId:str) -> ResultUnset:
        try:
            self.logger.info("%s.unset_channel method invoked for server: %s", self.file_prefix, guildId)

            #get the server id
            serverid= await self.serverRepo.get_serverid_from_server(guildId)

            if serverid:
                #get the channel id from server id
                channel_id= await self.channelRepo.get_channel_id_from_server_id(serverid, 1)

                if channel_id:
                    #inactivate channel
                    inactivate_result= await self.channelRepo.inactivate_channel_by_channel_id(channel_id)

                    if inactivate_result:
                        return ResultUnset(True, "success")
                    
                    else:
                        return ResultUnset(False, "error while inactivating channel")

                else:
                    #no channel set
                    return ResultUnset(False, "No channel setup", NoChannelFound=True)
            else:
                return ResultUnset(False, "Error while getting serverid")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_channel method invoked for server: %s", self.file_prefix, guildId,exc_info=1)
            raise e
        
    async def check_channels(self, guildId: str) -> ResultCheck:
        try:
            self.logger.info("%s.check_channels method invoked for server: %s", self.file_prefix, guildId)

            #get serverid
            serverid= await self.serverRepo.get_serverid_from_server(guildId)

            if serverid:
                #get channels with this server id
                channel_result= await self.channelRepo.get_channels_from_server_id(serverid, 1, 0)

                if channel_result:
                    return ResultCheck(True, "success", Data=channel_result)

                else:
                    return ResultCheck(False, "No Channels found", IsEmpty=True)

            else:
                return ResultCheck(False, "Error occured while getting server id")

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_channels method invoked for server: %s", self.file_prefix, guildId,exc_info=1)
            raise e
        