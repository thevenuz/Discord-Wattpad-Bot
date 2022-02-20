from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import logging


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')

logger=logging.getLogger()
logger.setLevel(logging.ERROR)

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

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

            soup=BeautifulSoup(r.content,'html.parser')

            #check if last updated has minutes in it
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
                                        dateDifference=nowDate-actualDate
                                        #check the time differnce between now and published time
                                        minuteDiffernce=dateDifference.total_seconds()/60
                                        logger.info('minutes diff of part %s is %s',chapterLink,minuteDiffernce)
                                        #if the time difference is less than 2 min, return this chapter link
                                        if actualDate>lastcheckeddate:
                                            newchapters.append(chapterLink)
                                            return newchapters,actualDate

                                        if minuteDiffernce<=2:
                                            newchapters.append(chapterLink)

                                            return newchapters

    except Exception as e:
        logger.critical('Exception occured in wattapd scraper for story %s', url,exc_info=1)
        pass



