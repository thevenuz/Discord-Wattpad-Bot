from typing import List
from wattpad.db.models.author import Author
from wattpad.logger.baselogger import BaseLogger
import aiohttp

from wattpad.meta.models.result import ResultAuthor

class AuthorUtil:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.utils.cauthorutil"
        self.logger= BaseLogger().loggger_init()
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

    async def validate_author_url(self, authorurl:str) -> ResultAuthor:
        try:
            self.logger.info("%s.validate_author_url method invoked for url: %s", self.file_prefix, authorurl)

            #need to check the URL pattern here
            pattern="wattpad.com/user/"

            validurl= False

            #make a request to author url and see if it's valid
            request_result= await self.__make_request_to_url(authorurl)

            if request_result == "0" or request_result == "200":
                validurl= True
            
            if validurl:
                if pattern in authorurl:
                    return ResultAuthor(True, "Success")
                else:
                    return ResultAuthor(False, "pattern doesn't match", HasPattern=False)
            
            else:
                return ResultAuthor(False, "Request to URL failed", IsInvalidUrl=True)
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.validate_author_url method invoked for url: %s", self.file_prefix, authorurl,exc_info=1)
            raise e

    async def get_actual_author_url(self, authorurl:str) -> str:
        try:
            self.logger.info("%s.get_actual_author_url method invoked for author: %s", self.file_prefix, authorurl)

            #get the story URLs from chapter urls or remove utm tags
            if "utm" in authorurl:
                actual_author_url= await self.__get_author_url_from_utm(authorurl)
                return actual_author_url


            self.logger.error("%s.get_actual_story_url method - URL: %s is inavalid but doesn't contain utm", self.file_prefix, authorurl)
            return authorurl
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_author_url method invoked for author: %s", self.file_prefix, authorurl,exc_info=1)
            raise e

    async def build_author_data_msg(self, authors:List[Author]) -> str:
        try:
            self.logger.info("%s.build_author_data_msg method invoked", self.file_prefix)

            return_msg=""

            for index, author in enumerate(authors):
                return_msg= f"{return_msg}{index}. {author.Url}\n"

            
            return return_msg
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_author_data_msg method invoked", self.file_prefix,exc_info=1)
            raise e
        

    async def __get_author_url_from_utm(self, authorurl:str) -> str:
        try:
            self.logger.info("%s.__get_author_url_from_utm method invoked for author: %s", self.file_prefix, authorurl)

            actual_author_url=authorurl.split("?")[0]
            return actual_author_url
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_utm method invoked for author: %s", self.file_prefix, authorurl,exc_info=1)
            raise e
        

    async def __make_request_to_url(self, url:str) -> str:
        try:
            self.logger.info("%s.__make_request_to_url method invoked for url: %s", self.file_prefix, url)

            
            async with aiohttp.ClientSession() as session:
                async with session.get(url,headers=self.headers) as response:
                    r=await response.text()

            return response.status

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__make_request_to_url method invoked for url: %s", self.file_prefix, url,exc_info=1)
            return 0