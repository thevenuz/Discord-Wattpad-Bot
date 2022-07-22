from typing import List
from wattpad.logger.baselogger import BaseLogger
from wattpad.db.models.channel import Channel

class Channelutil:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.utils.channelutil"
        self.logger= BaseLogger().loggger_init()

    async def build_channel_data_msg(self, channels: List[Channel]) -> str:
        try:
            self.logger.info("%s.build_channel_data_msg method invoked", self.file_prefix)

            return_msg=""

            for index, channel in enumerate(channels):
                return_msg= f"{return_msg}{index + 1}. <#{channel.Channel}>\n"

            
            return return_msg
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_channel_data_msg method invoked", self.file_prefix,exc_info=1)
            raise e
        
