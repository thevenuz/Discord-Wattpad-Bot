from wattpad.logger.baselogger import BaseLogger
from wattpad.models.result import ResultValidateUrl
from bs4 import BeautifulSoup
import aiohttp
import re


class WattpadUtil:
    def __init__(self) -> None:
        self.filePrefix = "wattpad.utils.wattpadutil"
        self.logger = BaseLogger().loggger_init()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

    async def validate_author_url(self, url: str) -> ResultValidateUrl:
        try:
            self.logger.info("%s.validate_author_url method invoked for url: %s", self.filePrefix, url)

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
            self.logger.fatal("Exception occured in %s.validate_author_url method", self.filePrefix, exc_info=1)
            raise e

    async def get_actual_author_url(self, authorUrl: str) -> str:
        try:
            self.logger.info("%s.get_actual_author_url method invoked for author: %s", self.filePrefix, authorUrl)

            # get the url by removing utm tags
            if "utm" in authorUrl:
                actual_author_url = await self.__get_author_url_from_utm(authorUrl)
                return actual_author_url

            self.logger.error("%s.get_actual_author_url method - URL: %s is inavalid but doesn't contain utm", self.filePrefix, authorUrl)
            return authorUrl

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_author_url method invoked for author: %s", self.filePrefix, authorUrl, exc_info=1)
            raise e

    async def get_author_name(self, url: str) -> str:
        try:
            self.logger.info("%s.get_author_name method invoked", self.filePrefix)

            authorName = url.split('/user/')[1].replace('-', ' ')

            return authorName
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_author_name method", self.filePrefix, exc_info=1)
            raise e
        
    async def validate_story_url(self, storyUrl:str) -> ResultValidateUrl:
        try:
            self.logger.info("%s.validate_story_url method invoked for story: %s", self.filePrefix, storyUrl)

            validurl= False

            #make a request to story and see if it's valid
            request_result= await self.__make_request_to_url(storyUrl)

            if str(request_result) == "0" or str(request_result) == "200":
                validurl= True
            
            if validurl:
                matchUrl = re.findall("wattpad.com/story", storyUrl)

                if matchUrl:
                    return ResultValidateUrl(True, "Success")

                else:
                    return ResultValidateUrl(False, "pattern doesn't match", HasPattern=False)
            
            else:
                return ResultValidateUrl(False, "Request to URL failed", IsInvalidUrl=True)

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.validate_story_url method for story: %s", self.filePrefix, storyUrl, exc_info=1)
            raise e

    async def get_actual_story_url(self, storyUrl: str) -> str:
        try:
            self.logger.info("%s.get_actual_story_url method invoked for story: %s", self.filePrefix, storyUrl)

            # get the story URLs from chapter urls or remove utm tags
            if "utm" in storyUrl:
                actual_story_url = await self.__get_story_url_from_utm(storyUrl)
                return actual_story_url

            elif "story" not in storyUrl:
                actual_story_url = await self.__get_story_url_from_chapter(storyUrl)
                return actual_story_url

            self.logger.error("%s.get_actual_story_url method - URL: %s is inavalid but doesn't contain utm or is a chapter link", self.filePrefix, storyUrl)
            return storyUrl
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_story_url method invoked for story: %s", self.filePrefix, storyUrl,exc_info=1)
            raise e

    async def get_story_title_from_url(self, url:str) -> str:
        try:
            self.logger.info("%s.get_story_title_from_url method invoked for story: %s", self.filePrefix, url)

            if "utm" in url:
                url = await self.__get_story_url_from_utm(url)

            storytitle = str(url).split('/')
            title = storytitle[-1].split('-', 1)
            title = title[-1].replace('-', ' ')

            return title
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_title_from_url method invoked for story: %s", self.filePrefix, url,exc_info=1)
            raise e

    async def __make_request_to_url(self, url:str) -> str:
        try:
            self.logger.info("%s.__make_request_to_url method invoked for url: %s", self.filePrefix, url)

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    r = await response.text()

            return response.status

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__make_request_to_url method invoked for url: %s", self.filePrefix, url, exc_info=1)
            return 0

    async def __get_author_url_from_utm(self, authorUrl: str) -> str:
        try:
            self.logger.info("%s.__get_author_url_from_utm method invoked for author: %s", self.filePrefix, authorUrl)

            actual_author_url = authorUrl.split("?")[0]
            return actual_author_url

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_author_url_from_utm method for author: %s", self.filePrefix, authorUrl, exc_info=1)
            raise e
    
    async def __get_story_url_from_utm(self, url:str) -> str:
        try:
            self.logger.info("%s.__get_story_url_from_utm method invoked for story: %s", self.filePrefix, url)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers) as response:
                        r = await response.text()

            except Exception as e:
                self.logger.error("Exception occured %s.__get_story_url_from_utm while sending request to the chapter URL: %s", self.filePrefix, url,exc_info=1)
                return url

            if response.status == 200:
                soup = BeautifulSoup(r, 'html.parser')
                item = soup.find('link', {'href': True, 'rel': "canonical"})
                actual_story_url = item["href"]

                self.logger.info("The story URl of: %s without utm tags is %s",url,actual_story_url)

                return actual_story_url

            return url
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_url_from_utm method invoked for story: %s", self.filePrefix, url,exc_info=1)
            raise e
        
    async def __get_story_url_from_chapter(self, url:str) -> str:
        try:
            self.logger.info("%s.__get_story_url_from_chapter method invoked for entered story url: %s", self.filePrefix, url)

            domain = "https://www.wattpad.com"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers) as response:
                        r = await response.text()

            except:
                self.logger.error("Exception occured in %s.__get_story_url_from_chapter while sending request to the chapter URL: %s", self.filePrefix, url,exc_info=1)
                return url

            if response.status == 200:
                soup = BeautifulSoup(r, 'html.parser')
                item = soup.find("div", class_="dropdown-menu pull-left")
                title = item.find("div", class_="toc-header text-center")
                anchor = title.find("a", class_="on-navigate")
                link = anchor["href"]

                story_url = domain + link

                self.logger.info("The story URl for chapter URL : %s is %s", url, story_url)

                return story_url
        
            return url

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_url_from_chapter method invoked for entered story url: %s", self.filePrefix, url,exc_info=1)
            raise e
        