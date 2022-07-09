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
        

    #region get
    async def get_author_url_from_title(self, title:str, serverid:str) -> str:
        try:
            self.logger.info("%s.get_author_url_from_title method invoked for author: %s, server id: %s", self.file_prefix, title, serverid)

            sql="""SELECT Url FROM 
                    AUTHORS
                    WHERE
                    ServerId=:ServerId AND
                    IsActive=:IsActive AND
                    Url LIKE :Url
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 6
                    curs.arraysize = 5

                    curs.execute(sql,[serverid, 1, title])
                    conn.commit()

                    result=curs.fetchmany()

            if len(result) == 1:
                return result[0]

            else:
                self.logger.error("Multiple authors were found with similar entered title: %s in server: %s", self.file_prefix, title, serverid)
                return ""
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_url_from_title method invoked for author: %s, server id: %s", self.file_prefix, title, serverid,exc_info=1)
            raise e
        
    async def get_author_id_from_server_and_url(self, url:str, serverid:str) -> str:
        try:
            self.logger.info("%s.get_author_id_from_server_and_url method invoked for url: %s, serverid: %s", self.file_prefix, url, serverid)

            sql="""SELECT StoryId FROM
                    AUTHORS
                    WHERE
                    ServerId=:ServerId AND
                    IsActive=:IsActive
                    AND
                    Url=:Url
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[serverid, 1, url])
                    conn.commit()

                    result=curs.fetchone()

            return result
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_id_from_server_and_url method invoked for url: %s, serverid: %s", self.file_prefix, url, serverid,exc_info=1)
            raise e
        

    #endregion


    #region update
    async def inactivate_author_by_id(self, authorid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_author_by_id method invoked for author id: %s", self.file_prefix, authorid)

            sql="""UPDATE AUTHORS 
                    SET IsActive=:IsActive
                    WHERE
                    StoryId=:StoryId
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, authorid])
                    conn.commit()

            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_author_by_id method invoked for author id: %s", self.file_prefix, authorid,exc_info=1)
            raise e
        

    #endregion