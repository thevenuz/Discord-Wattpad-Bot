from bs4 import BeautifulSoup
import logging
import aiohttp

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')

logger=logging.getLogger(name="wpadhelper")
logger.setLevel(logging.ERROR)

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}   

async def get_actual_author_url(authorProfileUrl:str)->str:
    """
    If the entered author profile URL contains UTM tags, the scraping used for get announcements will not work properly.
    This method will take a profile URL with UTM tags and returns the actual URL that is compatible with scraper.
    returns: the URL of an author profile that can be used to fetch new announcements
    """

    try:
        logger.info("wattpad_helper.get_actual_author_url invoked for URL: %s",authorProfileUrl)
        authorUrl=authorProfileUrl.split("?")[0]
        return authorUrl


    except Exception as e:
        logger.critical("Exception occured in wattpad_helper.get_actual_author_url method for profile URL : %s", authorProfileUrl, exc_info=1)
        pass


async def get_storyurl_from_chapter(chapterURL:str)->str:
    """
    If the user enters a individual chapter URL instead of the story URL, this method will help to fetch the story URL from chapter URL.
    returns: Story URL
    """

    try:
        logger.info("wattpad_helper.get_storyurl_from_chapter invoked for URL: %s",chapterURL)
        domain="https://www.wattpad.com"
        try:
            #r=requests.get(chapterURL,headers=headers)

            #async impl of requests
            async with aiohttp.ClientSession() as session:
                async with session.get(chapterURL,headers=headers) as response:
                    r=await response.text()
        except:
            logger.error("Exception occured in wattpad_helper.get_storyurl_from_chapter while sending request to the chapter URL: %s", chapterURL,exc_info=1)
            return chapterURL

        #if r.status_code==200:
        if response.status==200:
            # soup=BeautifulSoup(r.content,'html.parser')
            soup=BeautifulSoup(r,'html.parser')
            item=soup.find("div",class_="dropdown-menu pull-left")
            title=item.find("div",class_="toc-header text-center")
            anchor=title.find("a",class_="on-navigate")
            url=anchor["href"]

            storyURL=domain+url

            logger.info("The story URl for chapter URL : %s is %s",chapterURL,storyURL)

            return storyURL


    except Exception as e:
        logger.critical("Exception occured in wattpad_helper.get_storyurl_from_chapter method for profile URL : %s", chapterURL, exc_info=1)
        pass


async def get_storyurl_without_utm(storyURL:str)->str:
    """
    Method to remove utm tags from the entered url and return simple story url
    returns: story url without utm tags
    """

    try:
        logger.info("wattpad_helper.get_storyurl_without_utm invoked for URL: %s",storyURL)
        try:
            #r=requests.get(storyURL,headers=headers)

            #async impl of requests
            async with aiohttp.ClientSession() as session:
                async with session.get(storyURL,headers=headers) as response:
                    r=await response.text()
        except:
            logger.error("Exception occured in wattpad_helper.get_storyurl_without_utm while sending request to the chapter URL: %s", storyURL,exc_info=1)
            return storyURL

        # if r.status_code==200:
        if response.status==200:
            # soup=BeautifulSoup(r.content,'html.parser')
            soup=BeautifulSoup(r,'html.parser')
            item=soup.find('link', {'href': True, 'rel': "canonical"})
            actualStoryURL=item["href"]

            logger.info("The story URl of: %s without utm tags is %s",storyURL,actualStoryURL)

            return actualStoryURL



    except Exception as e:
        logger.fatal("Exception occured in wattpad_helper.get_storyurl_without_utm for story url: %s",storyURL,exc_info=1)
        pass



#methods not related to scraping

async def get_story_title(storyURL:str)->str:
    """
    Takes story link and returns that story title
    """
    try:
        logger.info("get_story_title invoked for story url:%s",storyURL)

        
        storytitle=str(storyURL).split('/')
        title=storytitle[-1].split('-',1)
        title=title[-1].replace('-',' ')
        return title


    except Exception as e:
        logger.fatal("Exception occured in helpers.wattpad_helper.get_story_title for story url: %s",storyURL,exc_info=1)
        pass

