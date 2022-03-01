import string
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime,timedelta
import logging


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')

logger=logging.getLogger()
logger.setLevel(logging.ERROR)

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   


#region checks
async def checkStory(url):
    try:
        
        domain='www.wattpad.com'
        
        try:   
            r=requests.get(url,headers=headers)
        except:
            logger.error('Something went wrong while sending a request to the URL %s', url,exc_info=1)
            return False

        if r.status_code==200 and domain in url:
            return True
        return False
    except Exception as e:
        logger.fatal('Exception occured in checkstory method for story %s',url,exc_info=1)
        raise e


async def checkProfile(url):
    try:
        domain='www.wattpad.com'
        try:   
            r=requests.get(url,headers=headers)
        except:
            logger.error('Something went wrong while sending a request to the URL %s', url,exc_info=1)
            return False

        if r.status_code==200 and domain in url:
            return True
        return False
        
    except Exception as e:
        logger.fatal('Exception occured in checkProfile method for author %s',url,exc_info=1)
        raise e

#endregion checks


#region get new chapter
async def get_chapter(url,lastchecked):
    try:
        logger.info('Get a new chapter for story %s', url)
        newchapters=[]
        try:
            r=requests.get(url,headers=headers)
        except:
            logger.error('Something went wrong while sending a request to the URL %s', url,exc_info=1)
            return newchapters

        if r.status_code==200:
            nowDate=datetime.utcnow()
            if not lastchecked:
                lastchecked=nowDate-timedelta(minutes=2)

            soup=BeautifulSoup(r.content,'html.parser')

            #check if last updated has minutes or seconds in it
            comparetextmin='min'
            comparetextsec='sec'
            lastupdate=None
            updated=None
            try:
                lastupdate=soup.find('span',class_='table-of-contents__last-updated')
                if lastupdate:
                    updated=lastupdate.find('strong').text
                    logger.info('last updated %s',updated)
            except Exception as e:
                logger.fatal('Exception while fetching last upadated',exc_info=1)
                pass

            if (not lastupdate) or (not updated) or (comparetextmin in updated) or (comparetextsec in updated):
                divs=soup.find('div', class_='story-parts')
                if divs:
                    for item in divs:
                        #get individual chapters
                        eachChapter=item.find_all('a', class_='story-parts__part')
                        
                        for a in reversed(eachChapter):
                            chapterLink='https://www.wattpad.com'+a['href']
                            part=a['href'].split('-')[0].replace('/','')
                            #ope each chapter one by one
                            try:
                                chapterReq=requests.get(chapterLink,headers=headers)
                            except:
                                logger.error('Something went wrong while sending a request to the URL %s', url,exc_info=1)
                                continue

                            if chapterReq.status_code==200:
                                eachChapterSoup=BeautifulSoup(chapterReq.content,'html.parser')
                                scripts=eachChapterSoup.find_all('script', type='text/javascript')
                                for script in scripts:
                                    if 'window.prefetched =' in script.text:
                                        scriptData=script.text.strip()
                                        scriptData=scriptData.replace('window.prefetched =','')
                                        #the json data here is incomplete, so using the below code to convert that into a workable json
                                        while True:
                                            try:
                                                validJson=json.loads(scriptData + "}")
                                            except:
                                                scriptData = scriptData[:-1]
                                                continue
                                            break
                                        prefix='part.'+part+'.metadata'
                                        createDate=validJson[prefix]['data']['createDate']
                                        actualDate=datetime.strptime(createDate,"%Y-%m-%dT%H:%M:%SZ")
                                        lastcheckeddate=datetime.strptime(lastchecked,"%Y-%m-%d %H:%M:%S")
                                        #dateDifference=nowDate-actualDate
                                        #check the time differnce between now and published time
                                        #minuteDiffernce=dateDifference.total_seconds()/60
                                        #logger.info('minutes diff of part %s is %s',chapterLink,minuteDiffernce)
                                        #if the time difference is less than 2 min, return this chapter link
                                        if actualDate>lastcheckeddate:
                                            newchapters.append(chapterLink)
                                            return newchapters,actualDate

                                        

    except Exception as e:
        logger.critical('Exception occured in wattapd scraper for story %s', url,exc_info=1)
        pass

#endregion get new chapter


#region get new announcement
async def get_new_announcement(url,lastchecked):
    try:
        logger.info('Get a new Announcement for author %s triggered', url)
        author_name=url.split('/user/')[1]
        announcement_url=f'{url}/conversations'
        try:
            r=requests.get(announcement_url,headers=headers)
        except:
            logger.error('Something went wrong while sending a request to the URL %s', url,exc_info=1)
            return None

        if r.status_code==200:
            nowDate=datetime.utcnow()
            if not lastchecked:
                lastchecked=nowDate-timedelta(minutes=5)

            soup=BeautifulSoup(r.content,'html.parser')
            divs=soup.find('div', class_='pinned-item')
            if divs:
                from_name=divs.find('h3',class_='from-name')
                if from_name.text.lower()==author_name.lower():
                    timestamp=divs.find('time',class_='timestamp')
                    try:
                        timestampList=timestamp.attrs['datetime']
                    except:
                        pass
                    #lastUpdateTime=timestampList['datetime']
                    lastUpdateTime=datetime.strptime(timestampList,"%Y-%m-%dT%H:%M:%SZ")
                    lastcheckeddate=datetime.strptime(lastchecked,"%Y-%m-%d %H:%M:%S")
                    if lastUpdateTime>lastcheckeddate:
                        #panel=divs.find_all('div',{'class':['panel-body','message','new-message']})
                        panel=divs.select('div.panel-body.new-message')
                        announcement_text=panel[0].text.strip()
                        return announcement_text,lastUpdateTime

    

    except Exception as e:
        logger.critical('Exception occured in wattapd scraper for story %s', url,exc_info=1)
        pass

#endregion get announcement

