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

            sql="""INSERT INTO CUSTOMMSGS
                    (Type, StoryId, AuthorId, Message, ServerId, IsActive, RegisteredOn)
                    VALUES
                    (:Type, :StoryId, :AuthorId, :Message, :ServerId, :IsActive, :RegisteredOn)
                    RETURNING MsgId INTO :MsgId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    msgid= curs.var(int)
                    curs.execute(sql,[custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message, custommsg.ServerId ,custommsg.IsActive, datetime.utcnow(), msgid])
                    
                    id=msgid.getvalue()

                    conn.commit()
            
            return id[0]
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_custom_msg_data method invoked for type: %s, story id: %s, author id: %s, message: %s", self.file_prefix, custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message,exc_info=1)
            raise e
        

    #endregion

    #region get
    async def get_custom_msg_id_from_story_id(self, storyid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_msg_id_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive)

            sql="""SELECT MsgId FROM 
                    CUSTOMMSGS
                    WHERE 
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[storyid, isactive])
                    conn.commit()
            
                    result=curs.fetchone()
            if result:
                return result[0]

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_id_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive,exc_info=1)
            raise e
    
    async def get_custom_msg_id_from_author_id(self, authorid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_msg_id_from_author_id method invoked for author id: %s, isactive: %s", self.file_prefix, authorid, isactive)

            sql="""SELECT MsgId FROM 
                    CUSTOMMSGS
                    WHERE 
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[authorid, isactive])
                    conn.commit()
            
                    result=curs.fetchone()

            if result:
                return result[0]

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_id_from_author_id method invoked for author id: %s, isactive: %s", self.file_prefix, authorid, isactive,exc_info=1)
            raise e

    async def get_custom_msgs_from_server_id(self, serverid:str, isactive:bool=1, type= "s") -> List[CustomMsg]:
        try:
            self.logger.info("%s.get_custom_msgs_from_server_id method invoked for server id: %s, is active: %s, type: %s", self.file_prefix, serverid, isactive, type)

            sql="""SELECT * FROM
                    CUSTOMMSGS
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
            self.logger.fatal("Exception occured in %s.get_custom_msgs_from_server_id method invoked for server id: %s, is active: %s, type: %s", self.file_prefix, serverid, isactive, type, exc_info=1)
            return None
        
    async def get_custom_msg_from_story_id(self, storyid:str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_custom_msg_from_story_id method invoked for story id: %s, is active: %s", self.file_prefix, storyid, isactive)

            sql="""SELECT Message FROM
                    CUSTOMMSGS
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
                return result[0]

            return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_from_story_id method invoked for story id: %s, is active: %s", self.file_prefix, storyid, isactive, exc_info=1)
            return None

    async def get_custom_msg_from_author_id(self, authorid:str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_custom_msg_from_author_id method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive)

            sql="""SELECT Message FROM
                    CUSTOMMSGS
                    WHERE 
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[authorid, isactive])
                    conn.commit()

                    result=curs.fetchone()

            if result:
                return result[0]

            return None
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_from_author_id method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive, exc_info=1)
            return None

    async def get_custom_msg_for_category(self, serverid: str, type: str= "s", isactive: bool=1) -> CustomMsg:
        try:
            self.logger.info("%s.get_custom_msg_for_category method invoked for server id: %s, type: %s, is active: %s", self.file_prefix, serverid, type, isactive)

            sql="""SELECT * FROM 
                    CUSTOMMSGS
                    WHERE
                    ServerId=:ServerId
                    Type=:Type
                    AND
                    IsActive=:IsActive
                    AND
                    StoryId=:StoryId
                    AND
                    AuthorId=:AuthorId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[serverid, type, isactive, "", ""])
                    conn.commit()
                    
                    db_result=curs.fetchall()

                    if db_result:
                        custom_msg_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and custom_msg_data:
                result= await self.map.map_custom_msg_records_list(custom_msg_data, column_names)

                return result[0]

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_msg_for_category method invoked for server id: %s, type: %s, is active: %s", self.file_prefix, serverid, type, isactive,exc_info=1)
            raise e
        
    #endregion

    #region update
    async def delete_custom_msg_by_id(self, custom_msg_id:str) -> bool:
        try:
            self.logger.info("%s.delete_custom_msg_by_id method invoked for custom msg id: %s", self.file_prefix, custom_msg_id)

            sql="""UPDATE CUSTOMMSGS SET
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
                    curs.execute(sql,[0, "", "", custom_msg_id, 1])
                    conn.commit()

            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.delete_custom_msg_by_id method invoked for custom msg id: %s", self.file_prefix, custom_msg_id,exc_info=1)
            raise e
        
    async def update_custom_msg_by_author_id(self, authorid: str, msg:str, isactive:bool=1) -> bool:
        try:
            self.logger.info("%s.update_custom_msg_by_author_id method invoked for author id: %s,  msg: %s", self.file_prefix, authorid, msg)

            sql="""UPDATE CUSTOMMSGS
                    SET
                    Message=:Message
                    WHERE
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[msg, authorid, isactive])
                    conn.commit()
            
            return True

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_custom_msg_by_author_id method invoked for author id: %s, msg: %s", self.file_prefix, authorid, msg, exc_info=1)
            raise e
        
    async def update_custom_msg_by_story_id(self, storyid: str, msg:str, isactive:bool=1) -> bool:
        try:
            self.logger.info("%s.update_custom_msg_by_story_id method invoked for storyid: %s,  msg: %s", self.file_prefix, storyid, msg)

            sql="""UPDATE CUSTOMMSGS
                    SET
                    Message=:Message
                    WHERE
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[msg, storyid, isactive])
                    conn.commit()
            
            return True

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_custom_msg_by_story_id method invoked for storyid: %s, msg: %s", self.file_prefix, storyid, msg, exc_info=1)
            raise e

    async def update_custom_msg_by_msg_id(self, msgid: str, msg:str, isactive:bool=1) -> bool:
        try:
            self.logger.info("%s.update_custom_msg_by_msg_id method invoked for msg id: %s,  msg: %s", self.file_prefix, msgid, msg)

            sql="""UPDATE CUSTOMMSGS
                    SET
                    Message=:Message
                    WHERE
                    MsgId=:MsgId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[msg, msgid, isactive])
                    conn.commit()
            
            return True

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_custom_msg_by_msg_id method invoked for msg id: %s, msg: %s", self.file_prefix, msgid, msg, exc_info=1)
            raise e
    #endregion
