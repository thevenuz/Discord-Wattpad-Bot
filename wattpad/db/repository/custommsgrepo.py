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
                    (Type, StoryId, AuthorId, Message, IsActive, RegisteredOn)
                    VALUES
                    (:Type, :StoryId, :AuthorId, :Message, :IsActive, :RegisteredOn)
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message, custommsg.IsActive, datetime.utcnow()])
                    conn.commit()
            
                    id= curs.lastrowid()

            return id
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_custom_msg_data method invoked for type: %s, story id: %s, author id: %s, message: %s", self.file_prefix, custommsg.Type, custommsg.StoryId, custommsg.AuthorId, custommsg.Message,exc_info=1)
            raise e
        

    #endregion