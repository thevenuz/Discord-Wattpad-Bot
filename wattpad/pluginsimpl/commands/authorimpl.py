from wattpad.logger.baselogger import BaseLogger

class AuthorImpl:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.pluginsimpl.commands.authorimpl"
        self.logger= BaseLogger().loggger_init()

    async def follow_author(self, guildId: str, url:str):
        try:
            self.logger.info("%s.follow_author method invoked for server: %s, author: %s", self.file_prefix, guildId, url)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.follow_author method for server: %s, author: %s", self.file_prefix, guildId, url, exc_info=1)
            raise e
        
