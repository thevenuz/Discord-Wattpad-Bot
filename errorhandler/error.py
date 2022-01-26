import hikari
import lightbulb

errors = {
            "CommandNotFound": "Moron!! You used an invalid command!",
            "MissingPermissions": "You do not have required permission to run this command!",
            "BotMissingPermissions": "I don't have required permission `{}` to complete that command.",
            "CheckFailure": "You are not authorized to use this command.!",
            "other": "Uh-oh!! The developer has fucked up somewhere!!"
        }

async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    errorMsg=hikari.Embed(title=f'🛑 An error occurred with the `{event.context.command.name}` command.', color=0xFF0000)
    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        msg=errors["MissingPermissions"]
        errorMsg.add_field(name='Error:', value=msg, inline=False)
        await event.context.respond(embed=errorMsg, content=msg)

    if isinstance(event.exception, lightbulb.CheckFailure):
        msg=errors["CheckFailure"]
        errorMsg.add_field(name='Error:',value=msg, inline=False)
        await event.context.respond(embed=errorMsg)

    elif isinstance(event.exception,lightbulb.BotMissingRequiredPermission):
        msg=errors["BotMissingPermissions"]
        errorMsg.add_field(name='Error:', value=msg, inline=False)
        await event.context.respond(embed=errorMsg)

    elif isinstance(event.exception,lightbulb.CommandNotFound):
        msg=errors["CommandNotFound"]
        errorMsg.add_field(name='Error:',value=msg, inline=False)
        await event.context.respond(embed=errorMsg)

    else:
        msg=errors["other"]
        errorMsg.add_field(name='Error:', value=msg, inline=False)
        await event.context.respond(embed=errorMsg)
        #todo: log this error in a log file for analyzing errors.

    

def load(bot):
    bot.subscribe(lightbulb.CommandErrorEvent,on_error)

def unload(bot):
    bot.unsubscribe(lightbulb.CommandErrorEvent,on_error)
