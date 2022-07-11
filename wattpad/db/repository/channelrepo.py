from typing import List
from wattpad.db.models.channel import Channel
from wattpad.logger.baselogger import BaseLogger
import cx_Oracle

class ChannelRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.channelrepo"
        self.logger= BaseLogger().loggger_init()

    #region insert
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
    
    #endregion

    #region get
    async def get_channel_id_from_server_id(self, serverid: str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_channel_id_from_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""SELECT ChannelId FROM 
                    CHANNELS
                    WHERE
                    ServerId=:ServerId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[serverid, isactive])
                    conn.commit()
            
                    result=curs.fetchone()
        
            return result

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_channel_id_from_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            raise e

    async def get_channels_from_server_id(self, serverid: str, isactive: bool=1, iscustomchannel:bool=0) -> List[Channel]:
        try:
            self.logger.info("%s.get_channels_from_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""SELECT * FROM 
                    CHANNELS
                    WHERE
                    ServerId=:ServerId
                    AND 
                    IsActive=:IsActive
                    AND
                    IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[serverid, isactive, iscustomchannel])
                    conn.commit()

                    db_result=curs.fetchall()

                    if db_result:
                        channel_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and channel_data:
                result= await self.map.map_story_records_list(channel_data, column_names)

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_channels_from_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            raise e
        
    
    #endregion

    #region update
    async def inactivate_channel_by_channel_id(self, channelid: str) -> bool:
        try:
            self.logger.info("%s.inactivate_channel_by_channel_id method invoked for channel id: %s", self.file_prefix, channelid)

            sql="""UPDATE CHANNELS SET
                    IsActive=:IsActive
                    WHERE
                    ChannelId=:ChannelId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, channelid])
                    conn.commit()

            return True
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_channel_by_channel_id method invoked for channel id: %s", self.file_prefix, channelid,exc_info=1)
            raise e
        

    #endregion