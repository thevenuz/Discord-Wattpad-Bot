from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import ResultNewUpdate
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime,timedelta

class Scraper:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.scraper.scraper"
        self.logger= BaseLogger().loggger_init()
        self.headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}  

    async def get_new_chapter(self, url:str, lastchecked:datetime) -> ResultNewUpdate:
        try:
            self.logger.info("%s.get_new_chapter method invoked for story: %s, lastchecked: %s", self.file_prefix, url, lastchecked)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url,headers=self.headers) as response:
                        r=await response.text()

            except:
                self.logger.fatal("Exception occured in %s.get_new_chapter method while sneding request to stpory: %s, last checked: %s", self.file_prefix, url, lastchecked, exc_info=1)
                return ResultNewUpdate(False, "Exception occured while sending request to the story url")

            if response.status == 200:
                current_date_time= datetime.utcnow()

                if not lastchecked:
                    lastchecked=current_date_time - timedelta(minutes=10)

                soup=BeautifulSoup(r,'html.parser')

                #check if last updated has minutes or seconds in it
                comparetextmin= "min"
                comparetextsec= "sec"
                lastupdate=None
                updated=None

                try:
                    lastupdate=soup.find('span',class_='table-of-contents__last-updated')

                    if lastupdate:
                        updated= lastupdate.find('strong').text
                        self.logger.info("last updated: %s",updated)

                except Exception as e:
                    self.logger.fatal("Exception occured in %s.get_new_chapter method while chekcing for lastupdated", self.file_prefix, exc_info=1)
                    pass

                if (not lastupdate) or (not updated) or (comparetextmin in updated) or (comparetextsec in updated):
                    # divs=soup.find('div', class_='story-parts')
                    all_chapters= soup.find('div', class_='story-parts')

                    if all_chapters:
                        for item in all_chapters:
                            #get individual chapters
                            each_chapter= item.find_all('a', class_='story-parts__part')

                            for a in reversed(each_chapter):
                                chapterLink= "https://www.wattpad.com" + a['href']
                                part= a['href'].split('-')[0].replace('/','')

                                #open each chapter one by one
                                try:
                                    async with aiohttp.ClientSession() as client:
                                        async with client.get(chapterLink,headers=self.headers) as resp:
                                            chapterReq=await resp.text()

                                except:
                                    self.logger.error("Exception occured in %s.get_new_chapter while sending a request to the URL %s", self.file_prefix, url,exc_info=1)
                                    continue

                                if resp.status==200:
                                    eachChapterSoup=BeautifulSoup(chapterReq,'html.parser')
                                    scripts=eachChapterSoup.find_all('script', type='text/javascript')

                                    
                                    scriptData=await self.__script_with_data(scripts)

                                    #new method for getting proper json data
                                    if scriptData:
                                        validJson=await self.__get_usable_json(scriptData)

                                    else:
                                        self.logger.error("Error occured in %s.get_new_chapter. Error: script data is not found for a chapter: %s", self.file_prefix, chapterLink)

                                    if validJson:
                                        prefix='part.'+part+'.metadata'
                                        createDate=validJson[prefix]['data']['createDate']

                                        actualDate=datetime.strptime(createDate,"%Y-%m-%dT%H:%M:%SZ")
                                        lastcheckeddate=datetime.strptime(lastchecked,"%Y-%m-%d %H:%M:%S")
                                        
                                        #if the published date of new chpater is greater than lastchecked date, return the chapter url
                                        if actualDate > lastcheckeddate:
                                            self.logger.info("%s.get_new_chapter method ended for story: %s", self.file_prefix, url)
                                            
                                            return ResultNewUpdate(True, "Success in getting new chapter", NewUpdate=chapterLink, UpdatedDate=actualDate)

            return ResultNewUpdate(False, "some unknown error occured")   

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_chapter method for story: %s, lastchecked: %s", self.file_prefix, url, lastchecked, exc_info=1)
            pass

    async def get_new_announcement(self, url:str, lastchecked: datetime) -> ResultNewUpdate:
        try:
            self.logger.info("%s.get_new_announcement method invoked for url: %s, last checked: %s", self.file_prefix, url, lastchecked)

            author_name=url.split('/user/')[1]
            conversations_url=f'{url}/conversations'
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(conversations_url,headers=self.headers) as response:
                        r=await response.text()

            except:
                self.logger.error("Exception occured in %s.get_new_announcement method while sending request to author url: %s", self.file_prefix, conversations_url, exc_info=1)
                return None

            if response.status==200:
                current_date_time = datetime.utcnow()
                if not lastchecked:
                    lastchecked=current_date_time - timedelta(minutes=10)

                soup=BeautifulSoup(r,'html.parser')
                announcements= soup.find('div', class_='pinned-item')

                if announcements:
                    from_name=announcements.find('h3',class_='from-name')

                    if from_name.text.lower()==author_name.lower():
                        timestamp=announcements.find('time',class_='timestamp')

                        try:
                            timestampList=timestamp.attrs['datetime']

                        except:
                            pass

                        lastUpdateTime=datetime.strptime(timestampList,"%Y-%m-%dT%H:%M:%SZ")
                        lastcheckeddate=datetime.strptime(lastchecked,"%Y-%m-%d %H:%M:%S")

                        if lastUpdateTime > lastcheckeddate:
                            panel=announcements.select('div.panel-body.new-message')
                            announcement_text=panel[0].text.strip() 

                            self.logger.info("%s.get_new_announcement method ended for author: %s", self.file_prefix, url)

                            return ResultNewUpdate(True, "succes", NewUpdate=announcement_text, UpdatedDate=lastUpdateTime)
                            
            return ResultNewUpdate(False, "some unknown error occured")   
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_new_announcement method invoked for url: %s, last checked: %s", self.file_prefix, url, lastchecked,exc_info=1)
            raise e
        
    #region misc methods
    async def __script_with_data(self, scripts):
        try:
            self.logger.info("%s.script_with_data method invoked", self.file_prefix)
            for script in scripts:
                if 'window.prefetched =' in script.text:
                    scriptData=script.text.strip()
                    scriptData=scriptData.replace('window.prefetched =','')
                    return scriptData

        except Exception as e:
            self.logger.fatal("Exception occured in %s.script_with_data method while getting script data", self.file_prefix, exc_info=1)
            pass

    async def __get_usable_json(self, rawJSON) -> dict:
        """
        Takes incomplete json from scraped data and returns a usable json
        """
        try:
            self.logger.info("%s.get_usable_json method invoked", self.file_prefix)
            while True:
                try:
                    validJSON=json.loads(rawJSON + "}")
                except:
                    rawJSON = rawJSON[:-1]
                    continue
                break
            return validJSON

        except Exception as e:
            self.logger.fatal("Exception occured in %s.get_usable_json method", self.file_prefix, exc_info=1)
            pass
        
    #endregion