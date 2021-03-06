from typing import List
from wattpad.db.models.story import Story
from wattpad.logger.baselogger import BaseLogger
from bs4 import BeautifulSoup
import aiohttp
from wattpad.meta.models.checkcustomchannels import CheckCustomMsgStory, StoryCustomChannel
from wattpad.meta.models.result import ResultStory

class StoryUtil:
    def __init__(self) -> None:
        self.file_prefix = "wattpad.utils.storyutil"
        self.logger= BaseLogger().loggger_init()
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

    async def validate_story_url(self, storyUrl:str) -> ResultStory:
        try:
            self.logger.info("%s.validate_story_url method invoked for story: %s", self.file_prefix, storyUrl)

            #need to check the URL pattern here
            pattern="wattpad.com/story/"

            validurl= False

            #make a request to story and see if it's valid
            request_result= await self.__make_request_to_url(storyUrl)

            if str(request_result) == "0" or str(request_result) == "200":
                validurl= True
            
            if validurl:
                if pattern in storyUrl:
                    return ResultStory(True, "Success")
                else:
                    return ResultStory(False, "pattern doesn't match", HasPattern=False)
            
            else:
                return ResultStory(False, "Request to URL failed", IsInvalidUrl=True)

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.validate_story_url method invoked for story: %s", self.file_prefix, storyUrl, exc_info=1)
            raise e


    async def get_actual_story_url(self, storyUrl: str) -> str:
        try:
            self.logger.info("%s.get_actual_story_url method invoked for story: %s", self.file_prefix, storyUrl)

            #get the story URLs from chapter urls or remove utm tags
            if "utm" in storyUrl:
                actual_story_url= await self.__get_story_url_from_utm(storyUrl)
                return actual_story_url

            elif "story" not in storyUrl:
                actual_story_url= await self.__get_story_url_from_chapter(storyUrl)
                return actual_story_url

            self.logger.error("%s.get_actual_story_url method - URL: %s is inavalid but doesn't contain utm or is a chapter link", self.file_prefix, storyUrl)
            return storyUrl
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_actual_story_url method invoked for story: %s", self.file_prefix, storyUrl,exc_info=1)
            raise e

    async def build_story_data_msg(self, stories:List[Story]) -> str:
        try:
            self.logger.info("%s.build_story_data_msg method invoked", self.file_prefix)

            return_msg=""

            for index, story in enumerate(stories):
                return_msg= f"{return_msg}{index + 1}. {story.Url}\n"

            
            return return_msg

        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_story_data_msg method invoked", self.file_prefix,exc_info=1)
            raise e

    async def build_check_custom_channel_msg(self, stories:List[StoryCustomChannel]) -> str:
        try:
            self.logger.info("%s.build_check_custom_channel_msg method invoked", self.file_prefix)

            result=""
            newline="\n"
            story_data=""

            for story in stories:
                if story.Stories:
                    for s in  story.Stories:
                        story_data= story_data + s + newline

                    result= f"{result}<#{story.Channel}>{newline}{story_data}"

            return result
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_custom_channel_msg method invoked", self.file_prefix,exc_info=1)
            raise e
        
    async def build_check_custom_msgs_msg(self, records:List[CheckCustomMsgStory]) -> str:
        try:
            self.logger.info("%s.build_check_custom_msgs_msg method invoked", self.file_prefix)

            result=""
            newline="\n"

            for record in records:
                result= f"{result}{newline}{record.Story} - **{record.Message}**"

            return result
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.build_check_custom_msgs_msg method invoked", self.file_prefix,exc_info=1)
            raise e

    async def __get_story_url_from_utm(self, url:str) -> str:
        try:
            self.logger.info("%s.__get_story_url_from_utm method invoked for story: %s", self.file_prefix, url)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url,headers=self.headers) as response:
                        r=await response.text()

            except Exception as e:
                self.logger.error("Exception occured %s.__get_story_url_from_utm while sending request to the chapter URL: %s", self.file_prefix, url,exc_info=1)
                return url

            
            if response.status==200:
                soup=BeautifulSoup(r,'html.parser')
                item=soup.find('link', {'href': True, 'rel': "canonical"})
                actual_story_url=item["href"]

                self.logger.info("The story URl of: %s without utm tags is %s",url,actual_story_url)

                return actual_story_url

            return url
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_url_from_utm method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e
        
    
    async def __get_story_url_from_chapter(self, url:str) -> str:
        try:
            self.logger.info("%s.__get_story_url_from_chapter method invoked for entered story url: %s", self.file_prefix, url)

            domain="https://www.wattpad.com"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url,headers=self.headers) as response:
                        r=await response.text()

            except:
                self.logger.error("Exception occured in %s.__get_story_url_from_chapter while sending request to the chapter URL: %s", self.file_prefix, url,exc_info=1)
                return url

            
            if response.status==200:
                soup=BeautifulSoup(r,'html.parser')
                item=soup.find("div",class_="dropdown-menu pull-left")
                title=item.find("div",class_="toc-header text-center")
                anchor=title.find("a",class_="on-navigate")
                link=anchor["href"]

                story_url= domain + link

                self.logger.info("The story URl for chapter URL : %s is %s", url, story_url)

                return story_url
        
            return url

        except Exception as e:
            self.logger.fatal("Exception occured in %s.__get_story_url_from_chapter method invoked for entered story url: %s", self.file_prefix, url,exc_info=1)
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

    async def get_story_title_from_url(self, url:str) -> str:
        try:
            self.logger.info("%s.get_story_title_from_url method invoked for story: %s", self.file_prefix, url)

            if "utm" in url:
                url= await self.__get_story_url_from_utm(url)

            storytitle= str(url).split('/')
            title= storytitle[-1].split('-',1)
            title= title[-1].replace('-',' ')

            return title
            
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_story_title_from_url method invoked for story: %s", self.file_prefix, url,exc_info=1)
            raise e
        