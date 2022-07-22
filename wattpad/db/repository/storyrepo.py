from datetime import datetime
from typing import List
from wattpad.db.models.channel import Channel
from wattpad.logger.baselogger import BaseLogger
from wattpad.db.models.story import Story
from wattpad.utils.db import DBConfig
from wattpad.meta.mapping.map import Map
import cx_Oracle

class StoryRepo:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.db.repository.storyrepo"
        self.logger= BaseLogger().loggger_init()
        self.connection_string=DBConfig().load_db_config()
        self.map= Map()

    #region insert
    async def insert_stories(self, story:Story) -> str:
        try:
            self.logger.info("%s.insert_stories method invoked for story: %s, server Id: %s", self.file_prefix, story.Url, story.ServerId)

            sql="""INSERT INTO STORIES
                    (Url, ServerId)
                    VALUES
                    (:Url, :ServerId)
                    RETURNING StoryId INTO :StoryId
                """

            try:
                with cx_Oracle.connect(self.connection_string) as conn:
                    with conn.cursor() as curs:
                        storyid= curs.var(int)
                        curs.execute(sql,[story.Url, story.ServerId, storyid])

                        id= storyid.getvalue()
                        conn.commit()

                if id:
                    return id[0]
                
            
            except Exception as e:
                self.logger.fatal("Exception occured in %s.insert_stories method while inserting in to stories for story: %s", self.file_prefix, story.Url,exc_info=1)
                raise e
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.insert_stories invoked for story: %s, server Id: %s", self.file_prefix, story.Url, story.ServerId,exc_info=1)
            raise e
        

    #endregion


    #region get
    async def get_story_url_from_title(self, title:str, serverid:str) -> List[str]:
        try:
            self.logger.info("%s.get_story_url_from_title method invoked for server: %s, title: %s", self.file_prefix, serverid, title)

            sql="""SELECT Url FROM 
                    STORIES
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

                    db_result=curs.fetchmany()

                    if db_result:
                        result=list(map(lambda x: x.lower(), [r[0] for r in db_result]))

            if result:
                return result

            return None
  
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_url_from_title method invoked for server: %s, title: %s", self.file_prefix, serverid, title,exc_info=1)
            raise e
        
    async def get_story_id_from_server_and_url(self, url:str, serverid:str, isactive: bool=1) -> str:
        try:
            self.logger.info("%s.get_story_id_from_server_and_url method invoked for url: %s, server: %s", self.file_prefix, url, serverid)

            sql="""SELECT StoryId FROM
                    STORIES
                    WHERE
                    ServerId=:ServerId 
                    AND
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
            self.logger.fatal("Exception occured in %s.get_story_id_from_server_and_url method invoked for url: %s, server: %s", self.file_prefix, url, serverid,exc_info=1)
            raise e
        
    async def get_stories_from_server_id(self, serverid:str, isactive:bool=1) -> List[Story]:
        try:
            self.logger.info("%s.get_stories_from_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""SELECT * FROM
                    STORIES
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
                result= await self.map.map_story_records_list(story_data, column_names)

                return result

            return None

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_stories_from_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            raise e
    
    async def get_custom_channel_id_from_story_id(self, storyid: str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_custom_channel_id_from_story_and_server method invoked for server id: %s,", self.file_prefix, storyid)

            sql="""SELECT c.ChannelId from 
                    STORIES s JOIN CHANNELS c
                    ON
                    s.ChannelId = c.ChannelId
                    WHERE
                    StoryId=:StoryId
                    AND 
                    s.IsActive=:IsActive
                    AND
                    c.IsActive=:CIsActive
                    AND
                    c.IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[storyid, isactive, isactive, 1])
                    conn.commit()

                    result=curs.fetchone()

            return result

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_custom_channel_id_from_story_and_server method invoked for server id: %s", self.file_prefix, storyid,exc_info=1)
            return None
        
    async def get_story_id_with_custom_channel_from_server_and_url(self, url:str, serverid:str, isactive: bool=1, iscustomchannel:bool=1) -> str:
        try:
            self.logger.info("%s.get_story_id_whith_custom_channel_from_server_and_url method invoked for server id: %s, url: %s", self.file_prefix, serverid, url)

            sql="""SELECT StoryId FROM
                    STORIES
                    WHERE
                    ServerId=:ServerId 
                    AND
                    IsActive=:IsActive
                    AND
                    Url=:Url
                    AND
                    IsCustomChannel=:IsCustomChannel
                """
            
            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.prefetchrows = 2
                    curs.arraysize = 1

                    curs.execute(sql,[serverid, 1, url, iscustomchannel])
                    conn.commit()

                    result=curs.fetchone()

            return result

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_id_whith_custom_channel_from_server_and_url method invoked for server id: %s, url: %s", self.file_prefix, serverid, url,exc_info=1)
            raise e
        
    async def get_custom_channel_ids_for_stories_by_server_id(self, serverid:str, isactive: bool=1) -> List[str]:
        try:
            self.logger.info("%s.get_custom_channels_for_stories_by_server_id method invoked for server id: %s isactive: %s", self.file_prefix, serverid, isactive)

            sql="""SELECT ChannelId FROM 
                    STORIES
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
            self.logger.fatal("Exception occured in %s.get_custom_channels_for_stories_by_server_id method invoked for server id: %s isactive: %s", self.file_prefix, serverid, isactive,exc_info=1)
            raise e
        
    async def get_story_urls_from_channel_id(self, channelid:str, isactive: bool=1, iscustomchannel: bool=0) -> List[str]:
        """Returns a list of story urls
        """
        try:
            self.logger.info("%s.get_story_urls_from_channel_id method invoked for channel id: %s, is active: %s, is custom channel: %s", channelid, isactive, iscustomchannel)

            sql="""SELECT Url FROM
                    STORIES
                    WHERE
                    ChannelId=:ChannelId
                    AND
                    IsActive=:IsActive
                    AND
                    IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, isactive, iscustomchannel])
                    conn.commit()
            
                    result=curs.fetchall()

            if result:
                return result

            return None

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_urls_from_channel_id method invoked for channel id: %s, is active: %s, is custom channel: %s", channelid, isactive, iscustomchannel,exc_info=1)
            raise e
        
    async def get_story_url_from_story_id(self, storyid:str, isactive:bool=1) -> str:
        try:
            self.logger.info("%s.get_story_url_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive)

            sql="""SELECT Url FROM
                    STORIES
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

            return result

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_url_from_story_id method invoked for story id: %s, isactive: %s", self.file_prefix, storyid, isactive,exc_info=1)
            raise e
        
    async def get_active_stories(self, isactive:bool =1) -> List[Story]:
        try:
            self.logger.info("%s.get_active_stories method invoked", self.file_prefix)

            sql="""SELECT * FROM
                    STORIES
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
                        story_data=list(db_result)
                        column_names=list(map(lambda x: x.lower(), [d[0] for d in curs.description]))
            
            if db_result and story_data:
                result= await self.map.map_story_records_list(story_data, column_names)

                return result

            return None
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_active_stories method invoked", self.file_prefix,exc_info=1)
            return None
        
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
        
    async def update_channel_id_for_stories(self, storyid: str, channelid:str="", isactive:bool=1) -> bool:
        try:
            self.logger.info("%s.update_channel_id_for_stories method invoked for storyid: %s, channel id: %s", self.file_prefix, storyid, channelid)

            sql="""UPDATE STORIES SET
                    ChannelId=:ChannelId,
                    WHERE
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, storyid, isactive])
                    conn.commit()
                
            return True
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_channel_id_for_stories method invoked for storyid: %s, channel id: %s", self.file_prefix, storyid, channelid,exc_info=1)
            raise e
        
    async def inactivate_custom_channel_for_stories(self, storyid: str, channelid: str="", isactive: bool=1) -> bool:
        try:
            self.logger.info("%s.inactivate_custom_channel_for_stories method invoked for story id: %s, channel id: %s", self.file_prefix, storyid, channelid)

            sql="""UPDATE STORIES SET
                    ChannelId=:ChannelId,
                    IsActive=:IsActive
                    WHERE
                    StoryId=:StoryId
                    AND
                    IsActive=:IsActive
                    AND
                    IsCustomChannel=:IsCustomChannel
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[channelid, 0, storyid, 1, 1])
                    conn.commit()
            
            return True
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.inactivate_custom_channel_for_stories method invoked for story id: %s, channel id: %s", self.file_prefix, storyid, channelid,exc_info=1)
            raise e
        
    async def update_last_updated_date_for_story_id(self, storyid:str, lastupdated:datetime= datetime.utcnow()) -> bool:
        try:
            self.logger.info("%s.update_last_updated_date_for_story_id method invoked for story id: %s, last updated: %s", self.file_prefix, storyid, lastupdated)

            sql="""UPDATE STORIES SET 
                    LastUpdatedOn=:LastUpdatedOn
                    WHERE
                    StoryId=:StoryId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[lastupdated, storyid])
                    conn.commit()
            
            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_last_updated_date_for_story_id method for story id: %s, last updated: %s", self.file_prefix, storyid, lastupdated,exc_info=1)
            return False

    async def update_last_checked_date_for_story_id(self, storyid:str, lastchecked:datetime= datetime.utcnow()) -> bool:
        try:
            self.logger.info("%s.update_last_checked_date_for_story_id method invoked for story id: %s, last checked: %s", self.file_prefix, storyid, lastchecked)

            sql="""UPDATE STORIES SET 
                    LastcheckedOn=:LastcheckedOn
                    WHERE
                    StoryId=:StoryId
                """

            with cx_Oracle.connect(self.connection_string) as conn:
                with conn.cursor() as curs:
                    curs.execute(sql,[lastchecked, storyid])
                    conn.commit()
            
            return True

        except Exception as e:
            self.logger.fatal("Exception occured in %s.update_last_checked_date_for_story_id method for story id: %s, last checked: %s", self.file_prefix, storyid, lastchecked,exc_info=1)
            return False

    async def inactivate_all_stories_by_server_id(self, serverid:str) -> bool:
        try:
            self.logger.info("%s.inactivate_all_stories_by_server_id method invoked for server id: %s", self.file_prefix, serverid)

            sql="""UPDATE STORIES 
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
            self.logger.fatal("Exception occured in %s.inactivate_all_stories_by_server_id method invoked for server id: %s", self.file_prefix, serverid,exc_info=1)
            return False

    #endregion
