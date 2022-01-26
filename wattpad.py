from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

def checkStory(url):
    domain='www.wattpad.com'
    r=requests.get(url,headers=headers)
    if r.status_code==200 and domain in url:
        return True
    return False

def get_chapter(url):
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        nowDate=datetime.utcnow()

        soup=BeautifulSoup(r.content,'html.parser')

        #find all the chapters
        divs=soup.find('div', class_='story-parts')
        if divs:
            for item in divs:
                allChapters=item.find_all('div', class_='part__label')[-1].text
                #get individual chapters
                eachChapter=item.find_all('a', class_='story-parts__part')
                newchapters=[]
                for a in eachChapter:
                    chapterLink='https://www.wattpad.com'+a['href']
                    part=a['href'].split('-')[0].replace('/','')
                    #ope each chapter one by one
                    chapterReq=requests.get(chapterLink,headers=headers)
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
                                dateDifference=nowDate-actualDate
                                #check the time differnce between now and published time
                                minuteDiffernce=dateDifference.total_seconds()/60
                                #if the time difference is less than 2 min, return this chapter link
                                if minuteDiffernce<=2:
                                    newchapters.append(chapterLink)

                return newchapters



