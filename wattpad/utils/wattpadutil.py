from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultValidateUrl
import aiohttp
import re

class WattpadUtil:
    def __init__(self) -> None:
        self.file_prefix = "wattpad.utils.wattpadutil"
        self.logger = BaseLogger().loggger_init()

    async def validate_author_url(self, url: str) -> ResultValidateUrl:
        try:
            self.logger.info("%s.validate_author_url method invoked for url: %s", self.file_prefix, url)

            validUrl = False

            requestResult = await self.__make_request_to_url(url)

            if str(requestResult) == "0" or str(requestResult) == "200":
                validUrl = True

            if validUrl:
                matchUrl = re.findall("(wattpad.com/user)", url)

                if matchUrl:
                    return ResultValidateUrl(True, "Valid Url")

                return ResultValidateUrl(False, "Pattern doesn't match", PatternMatched=False)

            return ResultValidateUrl(False, "Request to url failed", InvalidUrl=True)

        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.validate_author_url method", self.file_prefix, exc_info=1)
            raise e

    async def get_actual_author_url(self, authorUrl: str) -> str:
        try:
            self.logger.info("%s.get_actual_author_url method invoked for author: %s", self.file_prefix, authorUrl)

            # get the url by removing utm tags
            if "utm" in authorUrl:
                actual_author_url = await self.__get_author_url_from_utm(authorUrl)
                return actual_author_url

            self.logger.error("%s.get_actual_author_url method - URL: %s is inavalid but doesn't contain utm", self.file_prefix, authorUrl)
            return authorUrl

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_author_url method invoked for author: %s", self.file_prefix, authorUrl, exc_info=1)
            raise e

    async def __make_request_to_url(self, url:str) -> str:
        try:
            self.logger.info("%s.__make_request_to_url method invoked for url: %s", self.file_prefix, url)

            
            async with aiohttp.ClientSession() as session:
                async with session.get(url,headers=self.headers) as response:
                    r=await response.text()

            return response.status

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__make_request_to_url method invoked for url: %s", self.file_prefix, url, exc_info=1)
            return 0

    async def __get_author_url_from_utm(self, authorUrl: str) -> str:
        try:
            self.logger.info("%s.__get_author_url_from_utm method invoked for author: %s", self.file_prefix, authorUrl)

            actual_author_url = authorUrl.split("?")[0]
            return actual_author_url

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_utm method for author: %s", self.file_prefix, authorUrl, exc_info=1)
            raise e
