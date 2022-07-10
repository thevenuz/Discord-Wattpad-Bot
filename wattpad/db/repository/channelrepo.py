from wattpad.db.models.channel import Channel
from wattpad.logger.baselogger import BaseLogger
import cx_Oracle

class ChannelRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.channelrepo"
        self.logger= BaseLogger().loggger_init

    async def insert_channel_data(self, channel:Channel) -> str:
        try:
            self.logger.info("%s.insert_channel_data method invoked", self.file_prefix)

            sql="""INSERT INTO CHANNELS
                    (Channel, ServerId, IsActive, IsCustomChannel)
                    VALUES
                    (:Channel, :ServerId, :IsActive, :IsCustomChannel)
                """

            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channel.Channel, channel.ServerId, channel.IsActive, channel.IsCustomChannel])
                    conn.commit()

                    id= curs.lastrowid()

            return id
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_channel_data method invoked", self.file_prefix,exc_info=1)
            raise e
        