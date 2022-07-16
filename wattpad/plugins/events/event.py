import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.eventsexecution.eventexec import Eventexec

plugin= lightbulb.Plugin("EventPlugin")

file_prefix="wattpad.plugins.events.event"
logger=BaseLogger().loggger_init()

@plugin.listener(hikari.GuildJoinEvent)
async def guild_join_event(event: hikari.GuildJoinEvent):
    try:
        logger.info("%s.guild_join_event method invoked for server: %s", file_prefix, event.guild_id)

        guildId= str(event.guild_id)
        #call the exec
        result= await Eventexec().guild_join_event(guildId)

        logger.info("Guild join method ended for server: %s", event.guild_id)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", file_prefix, event.guild_id,exc_info=1)
        raise e
    

@plugin.listener(hikari.GuildLeaveEvent)
async def guild_leave_event(event: hikari.GuildLeaveEvent):
    try:
        logger.info("%s.guild_leave_event method invoked for server: %s", file_prefix, event.guild_id)

        guildId= str(event.guild_id)
        #call the exec
        result= await Eventexec().guild_leave_event(guildId)

        logger.info("Guild leave method ended for server: %s", event.guild_id)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.guild_leave_event method invoked for server: %s", file_prefix, event.guild_id,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)