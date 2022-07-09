from wattpad.db.models.author import Author
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.db import DBConfig
from wattpad.meta.mapping.map import Map
import cx_Oracle

class AuthorRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.authorrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()
        self.map= Map()

    #region insert
    async def insert_author_data(self, author:Author) -> str:
        try:
            self.logger.info("%s.insert_author_data method invoked for author: %s, server id: %s", self.file_prefix, author.Url, author.ServerId)

            sql="""INSERT INTO STORIES
                    (Url, ServerId, IsActive)
                    VALUES
                    (:Url, :ServerId, :IsActive)
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        curs.execute(sql,[author.Url, author.ServerId, author.IsActive])
                        conn.commit()

                        id= curs.lastrowid()

            return id
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_author_data method invoked for author: %s, server id: %s", self.file_prefix, author.Url, author.ServerId,exc_info=1)
            raise e

    #endregion
        