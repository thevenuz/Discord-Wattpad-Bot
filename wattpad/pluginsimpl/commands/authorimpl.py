from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.jsonutil import JsonUtil
from wattpad.utils.datautil import DataUtil
from wattpad.models.result import ResultFollow
from wattpad.models.author import Authors, Author
from datetime import datetime

class AuthorImpl:
    def __init__(self) -> None:
        self.filePrefix= "wattpad.pluginsimpl.commands.authorimpl"
        self.logger= BaseLogger().loggger_init()

    async def follow_author(self, guildId: str, url:str) -> ResultFollow:
        try:
            self.logger.info("%s.follow_author method invoked for server: %s, author: %s", self.filePrefix, guildId, url)

            wattpadUtil = WattpadUtil()
            dataUtil = DataUtil()
            authorUrl = ""
            authorName = ""

            #check if the received url is valid
            validateAuthorUrl = await wattpadUtil.validate_author_url(url)

            if not validateAuthorUrl.IsSuccess:
                if validateAuthorUrl.InvalidUrl:
                    return ResultFollow(False, "Author url pattern doesn't match", InvalidUrl=True, PatternMatched=False)

                else:
                    # try to get a url with pattern
                    authorUrl = await wattpadUtil.get_actual_author_url(url)

            else:
                authorUrl = url

            authorName = await wattpadUtil.get_author_name(authorUrl)

            #prepare author json data to insert
            authorData = {
                "url": authorUrl,
                "lastupdated": f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
                "CustomChannel": "",
                "CustomMsg": "",
                "Error": {
                    "ErrorMsg": "",
                    "ErrorTime": ""
                }
            }

            #get authors data
            authors = await dataUtil.get_authors()

            if not authors or guildId not in authors:
                authors[guildId] = [
                    authorData
                ]

            else:
                for guild, author in authors:
                    if guild == guild:
                        if any(authorUrl == data["url"] for data in author):

                            #Already following the author in the server
                            return ResultFollow(True, "Already following", InvalidUrl= False, AlreadyFollowing= True, authorName= authorName)

                        else:
                            #append new author data to existing data
                            author.append(authorData)
                        

            result = await dataUtil.update_authors(authors)

            if result:
                return ResultFollow(True, "Author follow success", AlreadyFollowing= False, AuthorName= authorName)

            return ResultFollow(UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method for server: %s, author: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e
        
