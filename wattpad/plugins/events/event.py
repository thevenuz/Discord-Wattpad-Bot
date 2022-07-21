import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.eventsexecution.eventexec import Eventexec
from wattpad.utils.config import Config

plugin= lightbulb.Plugin("EventPlugin")

file_prefix="wattpad.plugins.events.event"
logger=BaseLogger().loggger_init()

@plugin.listener(hikari.GuildJoinEvent)
async def guild_join_event(event: hikari.GuildJoinEvent):
    try:
        logger.info("%s.guild_join_event method invoked for server: %s", file_prefix, event.guild_id)

        guildId= str(event.guild_id)
        settings= Config().load_settings()
        #call the exec
        result= await Eventexec().guild_join_event(guildId)

        if result:
            publicjoinmsg=f"Bot joined a new server: {event.guild.name}"
            joinmsg= f"Bot joined a new server: {event.guild.name}, Id: {event.guild_id}"
            await plugin.bot.rest.create_message(settings.LogChannel, joinmsg)
            await plugin.bot.rest.create_message(settings.PublicLogChannel, publicjoinmsg)

        logger.info("Guild join method ended for server: %s", event.guild_id)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.guild_join_event method invoked for server: %s", file_prefix, event.guild_id,exc_info=1)
        raise e
    

@plugin.listener(hikari.GuildLeaveEvent)
async def guild_leave_event(event: hikari.GuildLeaveEvent):
    try:
        logger.info("%s.guild_leave_event method invoked for server: %s", file_prefix, event.guild_id)

        guildId= str(event.guild_id)
        settings= Config().load_settings()
        #call the exec
        result= await Eventexec().guild_leave_event(guildId)

        if result:
            publicleftmsg=f"Bot joined a new server: {event.old_guild.name}"
            leftmsg= f"Bot joined a new server: {event.old_guild.name}, Id: {event.guild_id}"
            await plugin.bot.rest.create_message(settings.LogChannel, leftmsg)
            await plugin.bot.rest.create_message(settings.PublicLogChannel, publicleftmsg)

        logger.info("Guild leave method ended for server: %s", event.guild_id)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.guild_leave_event method invoked for server: %s", file_prefix, event.guild_id,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)