from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultSetChannel, ResultUnsetChannel, ResultCheck
from wattpad.utils.datautil import DataUtil

class ChannelImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.channelimpl"
        self.logger= BaseLogger().loggger_init()

    async def set_channel(self, guildId: str, channelId: str) -> ResultSetChannel:
        try:
            self.logger.info("%s.set_channel method invoked for server: %s, channel: %s", self.filePrefix, guildId, channelId)

            dataUtil = DataUtil()

            #get channels
            channels = await dataUtil.get_channels()

            #prepare the channel data
            channelData = [channelId]

            if not channels or guildId not in channels:
                channels[guildId] = channelData
                result = await dataUtil.update_channels(channels)
                if result:
                    return ResultSetChannel(True, "channel set success")
                else:
                    return ResultSetChannel(False, "channel set success", UnknownError= True)

            else:
                filteredChannels = dict(filter(lambda x: x[0] == guildId, channels.items()))

                for guild, channel in filteredChannels:
                    if channelId in channel:
                        #channel already exists
                        return ResultSetChannel(True, "Channel already exists", AlreadyExists= True)
                    else:
                        #return success
                        channels[guildId] = channelData
                        result = await dataUtil.update_channels(channels)
                        if result:
                            return ResultSetChannel(True, "channel set success")
                        else:
                            return ResultSetChannel(False, "channel set success", UnknownError= True)

            return ResultSetChannel(False, "channel set success", UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_channel method for server: %s, channel: %s", self.filePrefix, guildId, channelId, exc_info=1)
            raise e
        
    async def unset_channel(self, guildId: str) -> ResultUnsetChannel:
        try:
            self.logger.info("%s.unset_channel method invoked for server: %s", self.filePrefix, guildId)

            dataUtil = DataUtil()

            #get channels
            channels = await dataUtil.get_channels()

            filteredChannels = dict(filter(lambda x: x[0] == guildId, channels.items()))

            if not filteredChannels:
                return ResultUnsetChannel(False, "No channel set for the guild", NoChannel= True)

            else:
                for guild in filteredChannels.keys():
                    if guild == guildId:
                        channels[guildId] = []
                        result = await dataUtil.update_channels(channels)
                        if result:
                            return ResultUnsetChannel(True, "channel unset for the guild")
                        else:
                            return ResultUnsetChannel(True, "unknown error", UnknownError= True)

            return ResultUnsetChannel(True, "unknown error", UnknownError= True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.unset_channel method invoked for server: %s", self.filePrefix, guildId, exc_info=1)
            raise e
        
    async def check_channels(self, guildId: str) -> ResultCheck:
        try:
            self.logger.info("%s.check_channels method invoked for server: %s", self.filePrefix, guildId)

            #get channels
            channels = await DataUtil().get_channels()

            filteredChannels =  [channel for guild, channel in channels.items() if guild == guildId]

            return ResultCheck(True, "check channels success", Data= filteredChannels)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_channels method for server: %s", self.file_prefix, guildId,exc_info=1)
            raise e
        