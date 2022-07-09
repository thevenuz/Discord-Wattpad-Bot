import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.pluginsexecution.commandsexec.authorexec import AuthorExec

plugin= lightbulb.Plugin("AuthorPlugin")

file_prefix="wattpad.plugins.commands.author"

logger=BaseLogger().loggger_init()

@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("authorprofileurl", "Url of the Author's profile you want to follow", str, required=True)
@lightbulb.command("followauthor","Follow an author to receive new announcements from the author", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def follow_author(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.follow_author method invoked for author: %s, server: %s", file_prefix, ctx.options.authorprofileurl, ctx.guild_id)

        profileUrl= ctx.options.authorprofileurl
        guildId= str(ctx.guild_id)

        msgs= await Config().get_messages("en")

        #call the exec
        result= await AuthorExec().follow_author(profileUrl, guildId)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['follow:author:success']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.follow_story method for story: %s, server: %s, Error: %s", file_prefix, profileUrl, guildId, result.ResultInfo)

            if result.IsInvalidUrl:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['invalid:url']}", description=f"{msgs['invalid:author:url']}", color=0xFF0000))
            
            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.follow_author method invoked for author: %s, server: %s", file_prefix, ctx.options.authorprofileurl, ctx.guild_id,exc_info=1)
        raise e
    