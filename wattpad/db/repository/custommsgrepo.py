from datetime import datetime
from typing import List
from wattpad.db.models.custommsg import CustomMsg
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.db import DBConfig
import cx_Oracle
from wattpad.meta.mapping.map import Map

class CustomMsgrepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.custommsgrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()
        self.map= Map()

    #region insert
    async def insert_custom_msg_data(self, custommsg:CustomMsg) -> str:
        try:
            self.logger.info("%s.insert_custom_msg_data method invoked for type: %s, story id: %s, author id: %s, message: %s", self.file_prefix, custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message)

            sql="""INSERT INTO CUSTOMMSG
                    (Type, StoryId, AuthorId, Message, ServerId IsActive, RegisteredOn)
                    VALUES
                    (:Type, :StoryId, :AuthorId, :Message, :ServerId, :IsActive, :RegisteredOn)
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message, custommsg.ServerId ,custommsg.IsActive, datetime.utcnow()])
                    conn.commit()
            
                    id= curs.lastrowid()

            return id
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_custom_msg_data method invoked for type: %s, story id: %s, author id: %s, message: %s", self.file_prefix, custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message,exc_info=1)
            raise e
        

    #endregion

    #region get
    async def get_custom_msg_id_from_story_id(self, storyid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_msg_id_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive)

            sql="""SELECT * FROM 
                    CUSTOMMSG
                    WHERE 
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[storyid, isactive])
                    conn.commit()
            
                    result=curs.fetchall()

            return result

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_id_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive,exc_info=1)
            raise e
    
    async def get_custom_msg_id_from_author_id(self, authorid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_msg_id_from_author_id method invoked for author id: %s, isactive: %s", self.file_prefix, authorid, isactive)

            sql="""SELECT * FROM 
                    CUSTOMMSG
                    WHERE 
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[authorid, isactive])
                    conn.commit()
            
                    result=curs.fetchall()

            return result

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_id_from_author_id method invoked for author id: %s, isactive: %s", self.file_prefix, authorid, isactive,exc_info=1)
            raise e

    async def get_custom_msgs_from_server_id(self, serverid:str, isactive:bool=1, type:str="a") -> List[CustomMsg]:
        try:
            self.logger.info("%s.get_custom_msgs_from_server_id method invoked for server id: %s, is active: %s, type: %s", self.file_prefix, serverid, isactive, type)

            sql="""SELECT * FROM
                    CUSTOMMSG
                    WHERE 
                    ServerId=:ServerId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[serverid, isactive])
                    conn.commit()

                    db_result=curs.fetchall()

                    if db_result:
                        custom_msg_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and custom_msg_data:
                result= await self.map.map_custom_msg_records_list(custom_msg_data, column_names)

                return result

            return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msgs_from_server_id method invoked for server id: %s, is active: %s, type: %s", self.file_prefix, serverid, isactive, type,exc_info=1)
            return None
        
    async def get_custom_msg_from_story_id(self, storyid:str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_custom_msg_from_story_id method invoked for story id: %s, is active: %s", self.file_prefix, storyid, isactive)

            sql="""SELECT Message FROM
                    CUSTOMMSG
                    WHERE 
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[storyid, isactive])
                    conn.commit()

                    result=curs.fetchone()

            if result:
                return result

            return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_from_story_id method invoked for story id: %s, is active: %s", self.file_prefix, storyid, isactive, exc_info=1)
            return None


    #endregion

    #region update
    async def delete_custom_msg_by_id(self, custom_msg_id:str) -> bool:
        try:
            self.logger.info("%s.delete_custom_msg_by_id method invoked for custom msg id: %s", self.file_prefix, custom_msg_id)

            sql="""UPDATE CUSTOMMSG SET
                    IsActive=:IsActive,
                    StoryId=:StoryId,
                    AuthorId=:AuthorId
                    WHERE
                    MsgId=:MsgId
                    And
                    IsActive=:IsActive2
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, 0, 0, custom_msg_id, 1])
                    conn.commit()

            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.delete_custom_msg_by_id method invoked for custom msg id: %s", self.file_prefix, custom_msg_id,exc_info=1)
            raise e
        

    #endregion
