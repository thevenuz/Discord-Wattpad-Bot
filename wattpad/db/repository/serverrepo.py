from typing import List
from wattpad.logger.baselogger import BaseLogger
from wattpad.db.models.server import Server
from wattpad.utils.db import DBConfig
import cx_Oracle

class ServerRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.serverrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()


    #region insert
    async def insert_server_data(self, server:Server) -> str:
        try:
            self.logger.info("%s.insert_server_data method invoked for server : %s", self.file_prefix, server.GuildId)
            
            sql="""INSERT INTO SERVERS
                    (GuildId, IsActive)
                    VALUES
                    (:GuildId, :IsActive)
                    RETURNING ServerId INTO :ServerId
                """


            try:
                with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        serverid= curs.var(int)
                        curs.execute(sql,[server.GuildId, server.IsActive, serverid])

                        id= serverid.getvalue()
                        conn.commit()

                return id[0]
            
            except Exception as e:
                self.logger.fatal("Exception occured in %s.insert_server_data method while inserting data in to servers", self.file_prefix,exc_info=1)
                return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_server_data method invoked for server : %s", self.file_prefix, server.GuildId,exc_info=1)
            return None
        
    #endregion

    #region get
    async def get_serverid_from_server(self, guildid:str) -> str:
        try:
            self.logger.info("%s.get_serverid_from_server method invoked for guild: %s", self.file_prefix, guildid)

            sql="""SELECT ServerId FROM
                    SERVERS
                    WHERE
                    GuildId=:GuildId AND IsActive=:IsActive
                """

            try:
                with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        curs.prefetchrows = 2
                        curs.arraysize = 1

                        curs.execute(sql,[guildid, 1])
                        conn.commit()

                        result=curs.fetchone()
                
                return result[0]

            except Exception as e:
                self.logger.fatal("Exception occured in %s.get_serverid_from_server method",self.file_prefix,exc_info=1)
                raise e
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_serverid_from_server method invoked for guild: %s", self.file_prefix, guildid,exc_info=1)
            raise e
        
           
    #endregion

    #region update
    async def inactivate_server_from_guild_id(self, guildid: str) -> bool:
        try:
            self.logger.info("%s.inactivate_server_from_guild_id method invoked for server: %s", self.file_prefix, guildid)

            sql="""UPDATE SERVERS SET 
                    IsActive=:IsActive
                    WHERE
                    GuildId=:GuildId
                    AND
                    IsActive=:IsActive2
                """
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, guildid, 1])
                    conn.commit()
            
            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_server_from_guild_id method invoked for server: %s", self.file_prefix, guildid,exc_info=1)
            return False
        
    #endregion