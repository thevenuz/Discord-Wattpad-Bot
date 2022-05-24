import json
import logging
import helpers.json_helper as jhelper

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="msghelper")
logger.setLevel(logging.ERROR)

async def get_story_custommessage(guildId:str, storyURL:str):
    '''Checks if any custom message for stories has been setup for a server'''
    try:
        logger.info("get_story_custommessage has been invoked for server:%s",guildId)

        # with open("messages.json","r") as m:
        #     messages=json.load(m)

        #async impl of reading from json file:
        messages=await jhelper.read_from_json("messages.json")

        stories=await jhelper.read_from_json("stories.json")

        if guildId in stories:
            for guild, items in stories.items():
                if guild==guildId:
                    for item in items:
                        if "CustomMsg" in item:
                            if item["CustomMsg"] and item["CustomMsg"]!="":
                                if item["url"]==storyURL:
                                    return item["CustomMsg"]
        

        if messages and guildId in messages:
            for guild, msg in messages.items():
                if guild==guildId:
                    if msg["story"]!="":
                        CustomMsg=msg["story"]
                        return CustomMsg

    except Exception as e:
        logger.fatal("Exception occured in get_story_custommessage for server:%s",guildId,exc_info=1)
        raise e


async def get_announcement_custommessage(guildId:str,authorURL:str):
    try:
        logger.info("get_announcement_custommessage has been invoked for server:%s",guildId)

        # with open("messages.json","r") as m:
        #     messages=json.load(m)

        #async impl of reading from json file:
        messages=await jhelper.read_from_json("messages.json")
        authors=await jhelper.read_from_json("authors.json")

        
        if guildId in authors:
            for guild, items in authors.items():
                if guild==guildId:
                    for item in items:
                        if "CustomMsg" in item:
                            if item["CustomMsg"] and item["CustomMsg"]!="":
                                if item["url"]==authorURL:
                                    return item["CustomMsg"]

        if messages and guildId in messages:
            for guild, msg in messages.items():
                if guild==guildId:
                    if msg["announcement"]!="":
                        CustomMsg=msg["announcement"]
                        return CustomMsg

    except Exception as e:
        logger.fatal("Exception occured in get_announcement_custommessage for server:%s",guildId,exc_info=1)
        raise e


