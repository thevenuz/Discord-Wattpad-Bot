import hikari
import lightbulb
from lightbulb.ext import tasks
import logging
from datetime import datetime
import dotenv
import os

plugin=lightbulb.Plugin("TaskPlugin")


dotenv.load_dotenv()
PUBLICLOGCHANNEL=os.getenv('PUBLICLOGCHANNEL')

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

@tasks.task(d=7,auto_start=True)
async def load_active_servers():
    try:
        logger.info("load_active_servers task has been invoked on %s",datetime.utcnow())
        myGuilds= await plugin.bot.rest.fetch_my_guilds()
        guildNumbers=len(myGuilds)
        msgContent=f"The bot is currently active in {guildNumbers} servers."

        await plugin.bot.rest.create_message(PUBLICLOGCHANNEL,msgContent)


    except Exception as e:
        logger.fatal("Exception has occured in load_active_servers task",exc_info=1)
        raise e




def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

