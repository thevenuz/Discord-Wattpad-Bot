import json
import logging

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

async def get_story_custommessage(guildId:str):
    '''Checks if any custom message for stories has been setup for a server'''
    try:
        logger.info("get_story_custommessage has been invoked for server:%s",guildId)

        with open("messages.json","r") as m:
            messages=json.load(m)

        if messages and guildId in messages:
            for guild, msg in messages.items():
                if guild==guildId:
                    if msg["story"]!="":
                        CustomMsg=msg["story"]
                        return CustomMsg

    except Exception as e:
        logger.fatal("Exception occured in get_story_custommessage for server:%s",guildId,exc_info=1)
        raise e


async def get_announcement_custommessage(guildId:str):
    try:
        logger.info("get_announcement_custommessage has been invoked for server:%s",guildId)

        with open("messages.json","r") as m:
            messages=json.load(m)

        if messages and guildId in messages:
            for guild, msg in messages.items():
                if guild==guildId:
                    if msg["announcement"]!="":
                        CustomMsg=msg["announcement"]
                        return CustomMsg

    except Exception as e:
        logger.fatal("Exception occured in get_announcement_custommessage for server:%s",guildId,exc_info=1)
        raise e


