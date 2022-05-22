import helpers.json_helper as jhelper
import logging

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="bot")
logger.setLevel(logging.DEBUG)


async def get_custom_channel(guild:str, story_url:str, category:str):
    try:
        logger.info("custom_channel_helper.get_custom_channel triggered for guild: %s, story: %s",guild,story_url)

        if category.lower()=="author":
            records=await jhelper.read_from_json("Authors.json")
        else:
            records=await jhelper.read_from_json("Stories.json")

        if records:
            for guild_id, items in records.items():
                if guild==guild_id:
                    for item in items:
                        if "CustomChannel" in item:
                            if item["url"]==story_url and item["CustomChannel"]:
                                return item["CustomChannel"]

        return None

    except Exception as e:
        logger.fatal("Exception occured in custom_channel_helper.get_custom_channel triggered for guild: %s, story: %s",guild,story_url,exc_info=1)
        pass