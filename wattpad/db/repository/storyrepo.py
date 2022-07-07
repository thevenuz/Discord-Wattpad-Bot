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