import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config

filePrefix = "wattpad.plugins.errorhandler.errorhandler"
logger = BaseLogger().loggger_init()

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    try:
        logger.error("%s.on_error method triggered. Error msg triggered for command: %s in server: %s", filePrefix, event.context.command.name, event.context.guild_id)

        msgs= await Config().get_messages("en")

        embed= hikari.Embed(title=f"🛑 An error occurred with the `{event.context.command.name}` command.", color=0xFF0000)

        if isinstance(event.exception, lightbulb.MissingRequiredPermission):
            logger.error("Error occured due to missing permissions in server: %s", event.context.guild_id)

            embed.add_field(name="Error:", value=f"{msgs['error:missing:perms']}")

        if isinstance(event.exception, lightbulb.CheckFailure):
            logger.error("Error occured due to missing permissions in server: %s", event.context.guild_id)

            embed.add_field(name="Error:", value=f"{msgs['error:check:failure']}")

        elif isinstance(event.exception,lightbulb.BotMissingRequiredPermission):
            logger.error("Error due to bot missing permissions in server: %s", event.context.guild_id)

            embed.add_field(name="Error:", value=f"{msgs['error:bot:missing:perms']}")

        elif isinstance(event.exception,lightbulb.CommandNotFound):
            logger.error("Error due to invalid command in server: %s", event.context.guild_id)

            embed.add_field(name="Error:", value=f"{msgs['error:invalid:command']}")

        else:
            logger.fatal("Some unknown exception has occured for command %s in server: %s", event.context.command.name, event.context.guild_id,exc_info=1)

            embed.add_field(name="Error:", value=f"{msgs['error:unknown']}")
           
        await event.context.respond(embed=embed)

    except Exception as e:
        logger.fatal("Exception occured in Error handler for command %s in server: %s", event.context.command.name, event.context.guild_id, exc_info=1)
        pass

    
def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent, on_error)

def unload(bot):
    bot.unsubscribe(lightbulb.CommandErrorEvent, on_error)
