from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import Result, ResultSetChannel
from wattpad.utils.datautil import DataUtil

class ChannelImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.channelimpl"
        self.logger= BaseLogger().loggger_init()

    async def set_channel(self, guildId: str, channelId: str) -> ResultSetChannel:
        try:
            self.logger.info("%s.set_channel method invoked for server: %s, channel: %s", self.filePrefix, guildId, channelId)

            #get channels
            channels = await DataUtil().get_channels()

            #prepare the channel data
            channelData = [channelId]

            if not channels or guildId not in channels:
                channels[guildId] = channelData
                ResultSetChannel(True, "channel set success")

            else:
                filteredChannels = dict(filter(lambda x: x[0] == guildId, channels.items()))

                for guild, channel in filteredChannels:
                    if channelId in channel:
                        #channel already exists
                        ResultSetChannel(True, "Channel already exists", AlreadyExists= True)
                    else:
                        #return success
                        channels[guildId] = channelData
                        ResultSetChannel(True, "channel set success")

            ResultSetChannel(False, "channel set success", UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.set_channel method invoked for server: %s, channel: %s", self.filePrefix, guildId, channelId, exc_info=1)
            raise e
        