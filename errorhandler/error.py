import hikari
import lightbulb
import logging

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

errors = {
            "CommandNotFound": "Moron!! You used an invalid command!",
            "MissingPermissions": "You do not have required permission to run this command! You need to have either ADMINISTRATOR or MODERATEMEMBERS permission to use this command.",
            "BotMissingPermissions": "I don't have required permission `{}` to complete that command.",
            "CheckFailure": "You are not authorized to use this command! You need to have either ADMINISTRATOR or MODERATEMEMBERS permission to use this command.",
            "other": "Uh-oh!! The developer has fucked up somewhere!!"
        }

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    try:
        logger.error('Error msgs got triggered for command %s in guild %s and channel %s', event.context.command.name,event.context.guild_id,event.context.channel_id, exc_info=1)
        errorMsg=hikari.Embed(title=f'🛑 An error occurred with the `{event.context.command.name}` command.', color=0xFF0000)
        if isinstance(event.exception, lightbulb.MissingRequiredPermission):
            logger.info('Error due to missing permissions')
            msg=errors["MissingPermissions"]
            errorMsg.add_field(name='Error:', value=msg, inline=False)
            await event.context.respond(embed=errorMsg)

        if isinstance(event.exception, lightbulb.CheckFailure):
            logger.info('Error due to missing permissions')
            msg=errors["CheckFailure"]
            errorMsg.add_field(name='Error:',value=msg, inline=False)
            await event.context.respond(embed=errorMsg)

        elif isinstance(event.exception,lightbulb.BotMissingRequiredPermission):
            logger.info('Error due to bot missing permissions')
            msg=errors["BotMissingPermissions"]
            errorMsg.add_field(name='Error:', value=msg, inline=False)
            await event.context.respond(embed=errorMsg)

        elif isinstance(event.exception,lightbulb.CommandNotFound):
            logger.info('Error due to invalid command')
            msg=errors["CommandNotFound"]
            errorMsg.add_field(name='Error:',value=msg, inline=False)
            await event.context.respond(embed=errorMsg)

        else:
            logger.fatal('Some unknown exception has occured for command %s', event.context.command.name, exc_info=1)
            msg=errors["other"]
            errorMsg.add_field(name='Error:', value=msg, inline=False)
            await event.context.respond(embed=errorMsg)
           
    except Exception as e:
        logger.critical('Exception occured in Error handler for command %s', event.context.command.name, exc_info=1)
        ctcerrorMsg=hikari.Embed(title=f'🛑 An error occurred with the `{event.context.command.name}` command.', color=0xFF0000)
        msg=errors["other"]
        ctcerrorMsg.add_field(name='Error:', value=msg, inline=False)
        await event.context.respond(embed=ctcerrorMsg)

    

def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent,on_error)

def unload(bot):
    bot.unsubscribe(lightbulb.CommandErrorEvent,on_error)
