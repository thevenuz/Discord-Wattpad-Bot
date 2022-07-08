from wattpad.logger.baselogger import BaseLogger
from wattpad.db.models.story import Story
from wattpad.utils.db import DBConfig
import cx_Oracle

class StoryRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.storyrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()

    #region insert
    async def insert_stories(self, story:Story) -> str:
        try:
            self.logger.info("%s.insert_stories method invoked for story: %s, server Id: %s", self.file_prefix, story.Url, story.ServerId)

            sql="""INSERT INTO STORIES
                    (Url, ServerId)
                    VALUES
                    (:Url, :ServerId)
                """

            try:
                with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        curs.execute(sql,[story.Url, story.ServerId])
                        conn.commit()

                        id= curs.lastrowid()

                return id
                
            
            except Exception as e:
                self.logger.fatal("Exception occured in %s.insert_stories method while inserting in to stories for story: %s", self.file_prefix, story.Url,exc_info=1)
                raise e
            

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_stories invoked for story: %s, server Id: %s", self.file_prefix, story.Url, story.ServerId,exc_info=1)
            raise e
        

    #endregion


    #region get
    async def get_story_url_from_title(self, title:str, serverid:str) -> str:
        try:
            self.logger.info("%s.get_story_url_from_title method invoked for server: %s, title: %s", self.file_prefix, serverid, title)

            sql="""SELECT Url FROM 
                    STORIES
                    WHERE
                    ServerId=:ServerId AND
                    Url LIKE :Url
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 6
                    curs.arraysize = 5

                    curs.execute(sql,[serverid, title])
                    conn.commit()

                    result=curs.fetchmany()

            if len(result) == 1:
                return result[0]

            else:
                self.logger.error("Multiple stories were found with similar entered title: %s in server: %s", self.file_prefix, title, serverid)
                return ""
  
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_url_from_title method invoked for server: %s, title: %s", self.file_prefix, serverid, title,exc_info=1)
            raise e
        
    async def get_story_id_from_server_and_url(self, url:str, serverid:str) -> str:
        try:
            self.logger.info("%s.get_story_id_from_server_and_url method invoked for url: %s, server: %s", self.file_prefix, url, serverid)

            sql="""SELECT StoryId FROM
                    STORIES
                    WHERE
                    ServerId=:ServerId
                    AND
                    Url=:Url
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[serverid, url])
                    conn.commit()

                    result=curs.fetchone()

            return result

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_id_from_server_and_url method invoked for url: %s, server: %s", self.file_prefix, url, serverid,exc_info=1)
            raise e
        

    #endregion


    #region update
    async def inactivate_story_by_id(self, storyid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_story_by_id method invoked for story id: %s", self.file_prefix, storyid)

            sql="""UPDATE STORIES 
                    SET IsActive=:IsActive
                    WHERE
                    StoryId=:StoryId
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, storyid])
                    conn.commit()

            
            return True
                    
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_story_by_id method invoked for story id: %s", self.file_prefix, storyid,exc_info=1)
            raise e
        
    async def inactivate_story_by_url_and_serverid(self, url:str, serverid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_story_by_url_and_serverid method invoked for url: %s, server id: %s", self.file_prefix, url, serverid)

            sql="""UPDATE STORIES 
                    SET IsActive=:IsActive
                    WHERE
                    Serverid=:Serverid
                    AND
                    Url=:Url
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, serverid, url])
                    conn.commit()

            
            return True            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_story_by_url_and_serverid method invoked for url: %s, server id: %s", self.file_prefix, url, serverid,exc_info=1)
            raise e
        

    #endregion
