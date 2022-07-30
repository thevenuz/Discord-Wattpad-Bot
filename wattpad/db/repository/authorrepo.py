from datetime import datetime
from typing import List
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

            sql="""INSERT INTO AUTHORS
                    (Url, ServerId, IsActive)
                    VALUES
                    (:Url, :ServerId, :IsActive)
                    RETURNING AuthorId INTO :AuthorId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        authorid= curs.var(int)
                        curs.execute(sql,[author.Url, author.ServerId, author.IsActive, authorid])
                        id= authorid.getvalue()
                        conn.commit()

            return id[0]
        
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
                    lower(Url) LIKE :Url
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 6
                    curs.arraysize = 5

                    curs.execute(sql,[serverid, 1, title])
                    conn.commit()

                    db_result=curs.fetchmany()

                    if db_result:
                        result=list(map(lambda x: x, [r[0] for r in db_result]))

            if db_result and result:
                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_url_from_title method invoked for author: %s, server id: %s", self.file_prefix, title, serverid,exc_info=1)
            raise e
        
    async def get_author_id_from_server_and_url(self, url:str, serverid:str,isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_author_id_from_server_and_url method invoked for url: %s, serverid: %s", self.file_prefix, url, serverid)

            sql="""SELECT AuthorId FROM
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

                    curs.execute(sql,[serverid, isactive, url])
                    conn.commit()

                    result=curs.fetchone()

            if result:
                return result[0]
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_id_from_server_and_url method invoked for url: %s, serverid: %s", self.file_prefix, url, serverid,exc_info=1)
            raise e
        
    async def get_authors_from_server_id(self, serverid:str, isactive:bool=1) -> List[Author]:
        try:
            self.logger.info("%s.get_authors_from_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""SELECT * FROM
                    AUTHORS
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
                        story_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and story_data:
                result= await self.map.map_author_records_list(story_data, column_names)

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_authors_from_server_id method invoked for server id: %s", self.file_prefix, serverid, exc_info=1)
            raise e

    async def get_author_id_with_custom_channel_from_server_and_url(self, url:str, serverid:str, isactive: bool=1, iscustomchannel:bool=1) -> str:
        try:
            self.logger.info("%s.get_author_id_with_custom_channel_from_server_and_url method invoked for server id: %s, url: %s", self.file_prefix, serverid, url)

            sql="""SELECT AuthorId FROM
                    AUTHORS a 
                    JOIN 
                    CHANNELS c
                    ON
                    a.ChannelId= c.ChannelId
                    WHERE
                    a.ServerId=:ServerId 
                    AND
                    a.IsActive=:IsActive
                    AND
                    c.IsActive=:IsActivec
                    AND
                    a.Url=:Url
                    AND
                    c.IsCustomChannel=:IsCustomChannel
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[serverid, isactive, isactive, url, iscustomchannel])
                    conn.commit()

                    result=curs.fetchone()

            if result:
                return result[0]

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_id_with_custom_channel_from_server_and_url method invoked for server id: %s, url: %s", self.file_prefix, serverid, url,exc_info=1)
            raise e 

    async def get_custom_channel_id_from_author_id(self, authorid: str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_custom_channel_id_from_author_id method invoked for server id: %s", self.file_prefix, authorid)

            sql="""SELECT c.ChannelId from 
                    AUTHORS a JOIN CHANNELS c
                    ON
                    a.ChannelId = c.ChannelId
                    WHERE
                    a.AuthorId=:AuthorId
                    AND 
                    a.IsActive=:IsActive
                    AND
                    c.IsActive=:CIsActive
                    AND
                    c.IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[authorid, isactive, isactive, 1])
                    conn.commit()

                    result=curs.fetchone()

            if result:
                return result[0]

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_channel_id_from_author_id method invoked for server id: %s", self.file_prefix, authorid, exc_info=1)
            raise e

    async def get_custom_channel_ids_for_authors_by_server_id(self, serverid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_channel_ids_for_authors_by_server_id method invoked for server id: %s isactive: %s", self.file_prefix, serverid, isactive)

            sql="""SELECT ChannelId FROM 
                    AUTHORS
                    WHERE
                    ServerId=:ServerId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[serverid, isactive])
                    conn.commit()

                    result=curs.fetchall()

            if result:
                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_channel_ids_for_authors_by_server_id method invoked for server id: %s isactive: %s", self.file_prefix, serverid, isactive,exc_info=1)
            raise e
    
    async def get_author_urls_from_channel_id(self, channelid:str, isactive: bool=1, iscustomchannel: bool=0) -> List[str]:
        """Returns a list of author urls
        """
        try:
            self.logger.info("%s.get_author_urls_from_channel_id method invoked for channel id: %s, is active: %s, is custom channel: %s", self.file_prefix, channelid, isactive, iscustomchannel)

            sql="""SELECT Url FROM
                    AUTHORS a
                    JOIN 
                    CHANNELS c
                    ON a.ChannelId = c.ChannelId
                    WHERE
                    a.ChannelId=:ChannelId
                    AND
                    a.IsActive=:IsActive
                    AND
                    c.IsActive=:IsActiveC
                    AND
                    c.IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, isactive, isactive, iscustomchannel])
                    conn.commit()
            
                    db_result=curs.fetchall()
                    if db_result:
                        result= list(map(lambda x: x.lower(), [d[0] for d in db_result]))

            if db_result and result:
                return result


            return None

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_urls_from_channel_id method invoked for channel id: %s, is active: %s, is custom channel: %s", self.file_prefix, channelid, isactive, iscustomchannel,exc_info=1)
            raise e

    async def get_author_url_from_author_id(self, authorid: str, isactive: bool=1) -> str:
        try:
            self.logger.info("%s.get_author_url_from_author_id method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive)

            sql="""SELECT Url FROM
                    AUTHORS
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
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_url_from_author_id method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive,exc_info=1)
            raise e

    async def get_active_authors(self, isactive:bool =1) -> List[Author]:
        try:
            self.logger.info("%s.get_active_stories method invoked", self.file_prefix)

            sql="""SELECT * FROM
                    AUTHORS
                    WHERE
                    IsActive=:IsActive
                    ORDER BY
                    LastcheckedOn ASC
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[isactive])
                    conn.commit()

                    db_result=curs.fetchall()

                    if db_result:
                        author_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and author_data:
                result= await self.map.map_author_records_list(author_data, column_names)

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_active_stories method invoked", self.file_prefix,exc_info=1)
            return None

    async def get_server_id_from_authorid(self, authorid: str, isactive: bool=1) -> str:
        try:
            self.logger.info("%s.get_server_id_from_authorid method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive)

            sql="""SELECT ServerId FROM
                    AUTHORS
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
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_server_id_from_authorid method invoked for author id: %s, is active: %s", self.file_prefix, authorid, isactive,exc_info=1)
            raise e
    #endregion


    #region update
    async def inactivate_author_by_id(self, authorid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_author_by_id method invoked for author id: %s", self.file_prefix, authorid)

            sql="""UPDATE AUTHORS 
                    SET IsActive=:IsActive
                    WHERE
                    AuthorId=:AuthorId
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[0, authorid])
                    conn.commit()

            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_author_by_id method invoked for author id: %s", self.file_prefix, authorid,exc_info=1)
            raise e
        
    async def update_channel_id_for_authors(self, authorid: str, channelid:str, isactive:bool=1) -> bool:
        try:
            self.logger.info("%s.update_channel_id_for_stories method invoked for author id: %s, channel id: %s", self.file_prefix, authorid, channelid)

            sql="""UPDATE AUTHORS SET
                    ChannelId=:ChannelId
                    WHERE
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, authorid, isactive])
                    conn.commit()
                
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_channel_id_for_stories method invoked for author id: %s, channel id: %s", self.file_prefix, authorid, channelid,exc_info=1)
            raise e
        
    async def inactivate_custom_channel_for_authors(self, authorid: str, channelid: str="", isactive: bool=1) -> bool:
        try:
            self.logger.info("%s.inactivate_custom_channel_for_authors method invoked for authors id: %s, channel id: %s", self.file_prefix, authorid, channelid)

            sql="""UPDATE AUTHORS SET
                    ChannelId=:ChannelId,
                    IsActive=:IsActive
                    WHERE
                    AuthorId=:AuthorId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, 1, authorid, isactive])
                    conn.commit()
            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_custom_channel_for_authors method invoked for author id: %s, channel id: %s", self.file_prefix, authorid, channelid,exc_info=1)
            raise e
    
    async def update_last_updated_date_for_author_id(self, authorid:str, lastupdated:datetime= datetime.utcnow()) -> bool:
        try:
            self.logger.info("%s.update_last_updated_date_for_author_id method invoked for story id: %s, last updated: %s", self.file_prefix, authorid, lastupdated)

            sql="""UPDATE AUTHORS SET 
                    LastUpdatedOn=:LastUpdatedOn
                    WHERE
                    AuthorId=:AuthorId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[lastupdated, authorid])
                    conn.commit()
            
            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_last_updated_date_for_author_id method for story id: %s, last updated: %s", self.file_prefix, authorid, lastupdated,exc_info=1)
            return False

    async def update_last_checked_date_for_author_id(self, authorid:str, lastchecked:datetime= datetime.utcnow()) -> bool:
        try:
            self.logger.info("%s.update_last_checked_date_for_author_id method invoked for author id: %s, last checked: %s", self.file_prefix, authorid, lastchecked)

            sql="""UPDATE AUTHORS SET 
                    LastcheckedOn=:LastcheckedOn
                    WHERE
                    AuthorId=:AuthorId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[lastchecked, authorid])
                    conn.commit()
            
            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_last_checked_date_for_author_id method for author id: %s, last checked: %s", self.file_prefix, authorid, lastchecked,exc_info=1)
            return False
    
    async def inactivate_all_authors_by_server_id(self, serverid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_all_authors_by_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""UPDATE AUTHORS 
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
            self.logger.fatal("Exception occured in %s.inactivate_all_authors_by_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            return False
    
    #endregion