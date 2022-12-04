from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.datautil import DataUtil
from wattpad.models.result import ResultFollow, ResultUnfollow, ResultCheckAuthors
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
                    if guild == guildId:
                        if any(authorUrl == data["url"] for data in author):

                            #Already following the author in the server
                            return ResultFollow(True, "Already following", InvalidUrl= False, AlreadyFollowing= True, authorName= authorName)

                        else:
                            #append new author data to existing data
                            author.append(authorData)
                        
            #update the author data to json file
            result = await dataUtil.update_authors(authors)

            if result:
                return ResultFollow(True, "Author follow success", AlreadyFollowing= False, AuthorName= authorName)

            return ResultFollow(UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method for server: %s, author: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e
        
    async def unfollow_author(self, guildId:str, url: str) -> ResultUnfollow:
        try:
            self.logger.info("%s.unfollow_author method invoked for server: %s, author: %s", self.filePrefix, guildId, url)

            isAuthorName = False
            dataUtil = DataUtil()
            profileUrl = url

            if "/user/" not in url:
                isAuthorName = True

            #get authors
            authors = await dataUtil.get_authors()

            #filter the authors of the particular guild
            filteredAuthors = dict(filter(lambda x: x[0] == guildId, authors.items()))

            for guild, author in filteredAuthors:
                if guild == guildId:
                    #get url if entered input is author name
                    if isAuthorName:
                        if any(url in (foundurl := rec["url"]) for rec in author):
                            profileUrl = foundurl

                        else:
                            #url with the author name bot found
                            return ResultUnfollow(False, "Url with Author name not found", AuthorNameNotFound= True)

                    if any(profileUrl == rec["url"] for rec in author):
                        for rec in author:
                            if profileUrl == rec["url"]:
                                author.remove(rec)

                                #update the authors data to json file
                                result = await dataUtil.update_authors(authors)

                                if result:
                                    return ResultUnfollow(True, "Author unfollowed")

                                self.logger.error("%s.unfollow_author method: unknown error occured when updating authors", self.filePrefix)
                                return ResultUnfollow(False, "Unknown error", UnknownError= True)

                    else:
                        #no author found with the url
                        return ResultUnfollow(False, "Author not found", AuthorNotFound= True)
                    
            return ResultUnfollow(False, "Unknown error", UnknownError= True)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.unfollow_author method for server: %s, author: %s", self.filePrefix, guildId, url, exc_info=1)
            raise e 
        
    async def check_authors(self, guildId: str) -> ResultCheckAuthors:
        try:
            self.logger.info("%s.check_authors method invoked for server: %s", self.filePrefix, guildId)

            authors = await DataUtil().get_authors()

            filteredAuthors = [author for guild, author in authors.items() if guild == guildId]

            return ResultCheckAuthors(True, "check authors sucsess", Data= filteredAuthors)

        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_authors method for server: %s", self.filePrefix, guildId, exc_info=1)
            raise e
        