from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.wattpadutil import WattpadUtil
from wattpad.utils.jsonutil import JsonUtil
from wattpad.models.result import ResultFollow
from wattpad.models.author import Authors

class AuthorImpl:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsimpl.commands.authorimpl"
        self.logger= BaseLogger().loggger_init()

    async def follow_author(self, guildId: str, url:str) -> ResultFollow:
        try:
            self.logger.info("%s.follow_author method invoked for server: %s, author: %s", self.file_prefix, guildId, url)

            wattpadUtil = WattpadUtil()
            jsonUtil = JsonUtil()
            authorUrl = ""

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

            #get authors data
            authorData = await jsonUtil.read_from_json("config", "authors.json")

            authorResult = Authors(authorData)


        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method for server: %s, author: %s", self.file_prefix, guildId, url, exc_info=1)
            raise e
        
