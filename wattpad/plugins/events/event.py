import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsimpl.events.eventimpl import EventImpl
from wattpad.utils.config import Config

plugin = lightbulb.Plugin("EventPlugin")

filePrefix = "wattpad.plugins.events.event"
logger = BaseLogger().loggger_init()

@plugin.listener(hikari.GuildJoinEvent)
async def guild_join_event(event: hikari.GuildJoinEvent):
    try:
        logger.info("%s.guild_join_event method invoked for server: %s", filePrefix, event.guild_id)

        guildId = str(event.guild_id)
        settings= Config().load_settings()
        #call the impl
        result= await EventImpl().guild_join_event(guildId)

        if result:
            if settings.PublicLogChannel:
                publicJoinMsg = f"Bot joined a new server: {event.guild.name}"
                await plugin.bot.rest.create_message(settings.PublicLogChannel, publicJoinMsg)

            if settings.LogChannel:
                privateJoinMsg = f"Bot joined  new server: {event.guild.name}, Id: {event.guild_id}"
                await plugin.bot.rest.create_message(settings.LogChannel, privateJoinMsg)
            
    
    except Exception as e:
        logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", filePrefix, event.guild_id,exc_info=1)
        raise e
        

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)