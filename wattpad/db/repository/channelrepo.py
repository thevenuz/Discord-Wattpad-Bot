from typing import List
from wattpad.db.models.channel import Channel
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.db import DBConfig
import cx_Oracle
from wattpad.meta.mapping.map import Map

class ChannelRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.channelrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()
        self.map= Map()

    #region insert
    async def insert_channel_data(self, channel:Channel) -> str:
        try:
            self.logger.info("%s.insert_channel_data method invoked", self.file_prefix)

            sql="""INSERT INTO CHANNELS
                    (Channel, ServerId, IsActive, IsCustomChannel)
                    VALUES
                    (:Channel, :ServerId, :IsActive, :IsCustomChannel)
                    RETURNING ChannelId INTO :ChannelId
                """

            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    channelid= curs.var(int)
                    curs.execute(sql,[channel.Channel, channel.ServerId, channel.IsActive, channel.IsCustomChannel, channelid])

                    id=channelid.getvalue()

                    conn.commit()


            return id[0]
            
        
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
        
            return result[0]

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
                result= await self.map.map_channel_records_list(channel_data, column_names)

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_channels_from_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            raise e
        
    async def get_channel_from_channel_id(self, channelid:str, isactive:bool=1, iscustomchannel: bool=0) -> str:
        try:
            self.logger.info("%s.get_channel_from_channel_id method invoked for channel id: %s, isactive: %s, is custom channel: %s", self.file_prefix, channelid, isactive, iscustomchannel)

            sql="""SELECT Channel FROM 
                    CHANNELS
                    WHERE
                    ChannelId=:ChannelId
                    AND
                    IsActive=:IsActive
                    AND
                    IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[channelid, isactive, iscustomchannel])
                    conn.commit()

                    result= curs.fetchone()
                
            if result:
                return result

            return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_channel_from_channel_id method invoked for channel id: %s, isactive: %s, is custom channel: %s", self.file_prefix, channelid, isactive, iscustomchannel,exc_info=1)
            return None
        
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

    async def inactivate_all_channels_by_server_id(self, serverid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_all_channels_by_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""UPDATE CHANNELS 
                    SET 
                    IsActive=:IsActive
                    WHERE
                    ServerId=:ServerId
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, serverid])
                    conn.commit()

            
            return True
                    
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_all_channels_by_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            return False  

    async def update_channel_by_channel_id_and_server_id(self, channelid: str, serverid: str, channel: str, isactive: bool=1) -> bool:
        try:
            self.logger.info("%s.update_channel_by_channel_id_and_server_id method invoked for channel id: %s, server id: %s, channel: %s", self.file_prefix, channelid, serverid, channel)

            sql="""UPDATE CHANNELS SET 
                    Channel=:Channel
                    WHERE
                    ChannelId=:ChannelId
                    AND
                    ServerId=:ServerId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channel, channelid, serverid, isactive])
                    conn.commit()
            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_channel_by_channel_id_and_server_id method invoked for channel id: %s, server id: %s, channel: %s", self.file_prefix, channelid, serverid, channel,exc_info=1)
            return False
        

    #endregion