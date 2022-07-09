from wattpad.db.repository.serverrepo import ServerRepo
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import Result, ResultAuthor
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
                #insert the data in to author table
                author= Author(Url=authorUrl, ServerId=serverid, IsActive=1)

                author_result= await self.authorRepo.insert_author_data(author)

                if author_result:
                    return ResultAuthor(True, "Success")

                else:
                    return ResultAuthor(False, "Error with inserting author data")
            
            else:
                return ResultAuthor(False, "Error in inserting server data")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method invoked for author: %s, server: %s", self.file_prefix, url, guildid,exc_info=1)
            raise e
        