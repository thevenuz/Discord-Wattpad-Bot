from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import Result, ResultAuthor, ResultUnfollow, ResultCheck
from wattpad.utils.authorutil import AuthorUtil
from wattpad.db.models.server import Server
from wattpad.db.models.author import Author
from wattpad.db.repository.authorrepo import AuthorRepo

class AuthorExec:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsexecution.commandsexec.authorexec"
        self.logger= BaseLogger().loggger_init()
        self.authorUtil= AuthorUtil()
        self.serverRepo= ServerRepo()
        self.authorRepo= AuthorRepo()
        self.prefix= "wattpad.com"

    async def follow_author(self, url:str, guildid:str) -> ResultAuthor:
        try:
            self.logger.info("%s.follow_author method invoked for author: %s, server: %s", self.file_prefix, url, guildid)

            #check if the entered URL is a proper author URL
            validate_author= await self.authorUtil.validate_author_url(url)

            if not validate_author.IsSuccess:
                if validate_author.IsInvalidUrl:
                    return ResultAuthor(False, "Invalid URL", IsInvalidUrl=True)
                    
                else:
                    #try to get a proper story URl from the entered URL
                    authorUrl= await self.authorUtil.get_actual_author_url(url)

            else:
                authorUrl= url

            #get the data from server table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            #insert the data in to server table if no data is found
            if not serverid:
                server=Server(GuildId=guildid, IsActive=1)
                serverid= await self.serverRepo.insert_server_data(server)

            if serverid:
                #check if this uthor exists in lredy following list
                author_exists= await self.authorRepo.get_author_id_from_server_and_url(url=authorUrl, serverid=serverid, isactive=1)
                if not author_exists:
                    #insert the data in to author table
                    author= Author(Url=authorUrl, ServerId=serverid, IsActive=1)

                    author_result= await self.authorRepo.insert_author_data(author)

                    if author_result:
                        return ResultAuthor(True, "Success")

                    else:
                        return ResultAuthor(False, "Error with inserting author data")
                else:
                    return ResultAuthor(False, "This author is already in following list", AlreadyFollowing=True)
            
            else:
                return ResultAuthor(False, "Error in inserting server data")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method invoked for author: %s, server: %s", self.file_prefix, url, guildid,exc_info=1)
            raise e
        
    async def unfollow_author(self, url:str, guildid:str) -> Result:
        try:
            self.logger.info("%s.unfollow_author method invoked for server: %s, author: %s", self.file_prefix, guildid, url)

            author_url= ""

            if self.prefix not in url:
                #try to get the full author url from title
                author_url= await self.__get_author_url_from_title(url, guildid)

            if not author_url:
                #invalid title
                return Result(False, "Invalid Title", IsInvalidTitle=True)
                
            else:
                #for unfollowing just make inactive as true but we need to delete the records completely

                #get server id from guildid
                serverid= await self.serverRepo.get_serverid_from_server(guildid)

                if not serverid:
                    return ResultUnfollow(False, "Error while getting server id", UnknownError=True)
                
                #get author id from server and author url
                storyid= await self.authorRepo.get_author_id_from_server_and_url(url=author_url, serverid=serverid)

                if not storyid:
                    return ResultUnfollow(False, "Not following the author", NotFollowing=True)

                #inactivate author by id
                inactivate_result= await self.authorRepo.inactivate_author_by_id(storyid)

                if inactivate_result:
                    return ResultUnfollow(True, "Success")

            return ResultUnfollow(False, "Unknown Error", UnknownError=True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.unfollow_author method invoked for server: %s, author: %s", self.file_prefix, guildid, url,exc_info=1)
            raise e

    async def check_authors(self, guildid:str) -> ResultCheck:
        try:
            self.logger.info("%s.check_authors method invoked for server: %s", self.file_prefix, guildid)

            #get server id from servers table
            serverid= await self.serverRepo.get_serverid_from_server(guildid)

            if not serverid:
                return ResultCheck(False, "Error while getting server id")

            else:
                #get authors from the server id
                authors= await self.authorRepo.get_authors_from_server_id(serverid, 1)

                if authors:
                    return ResultCheck(True, "success", Data=authors)

                else:
                    return ResultCheck(False, "No authors found", IsEmpty=True)
            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_authors method invoked for server: %s", self.file_prefix, guildid, exc_info=1)
            raise e
        


    #region misc methods
    async def __get_author_url_from_title(self, title:str, server:str) -> str:
        try:
            self.logger.info("%s.__get_author_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server)

            #first get server id
            serverid= await self.serverRepo.get_serverid_from_server(server)

            if serverid:
                format_title=f"%{title}%"
                author_url= await self.authorRepo.get_author_url_from_title(format_title, serverid=serverid)

                if author_url:
                    return author_url

                else:
                    return ""

            return title
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_title method invoked for title: %s, server: %s", self.file_prefix, title, server,exc_info=1)
            raise e
        
    #endregion 