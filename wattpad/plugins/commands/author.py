import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.pluginsimpl.commands.authorimpl import AuthorImpl


plugin = lightbulb.Plugin("AuthorPlugin")

filePrefix = "wattpad.plugins.commands.author"

logger = BaseLogger().loggger_init()


@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR) | lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS) | lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS) | lightbulb.owner_only)
@lightbulb.option("authorprofileurl", "Url of the Author's profile you want to follow", str, required=True)
@lightbulb.command("follow-author", "Follow an author to receive new announcements from the author", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def follow_author(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.follow_author method invoked for author: %s, server: %s", filePrefix, ctx.options.authorprofileurl, ctx.guild_id)

        profileUrl = str(ctx.options.authorprofileurl)
        guildId = str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call implementation
        result = await AuthorImpl().follow_author(guildId, profileUrl)

        if result.IsSuccess:
            if result.AlreadyFollowing:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['already:following:author']}", color=0xFF0000))
            
            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['follow:author:success']}", color=0Xff500a))

        else:
            if result.InvalidUrl:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['invalid:url']}", description=f"{msgs['invalid:author:url']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    except Exception as e:
        logger.fatal("Exception occured in %s.follow_author method for author: %s, server: %s", filePrefix, ctx.options.authorprofileurl, ctx.guild_id, exc_info=1)
        raise e

@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("authorprofileurl", "Url of the Author's profile you want to unfollow. You can also use title instead of full url", str, required=True)
@lightbulb.command("unfollow-author","Unfollow an author you're following to stop receing new announcements from the author", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unfollow_author(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unfollow_author method invoked for server: %s, author: %s", filePrefix, ctx.guild_id, ctx.options.authorprofileurl)

        profileUrl = str(ctx.options.authorprofileurl)
        guildId = str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await AuthorImpl().unfollow_author(guildId, profileUrl)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['unfollow:author:success']}", color=0Xff500a))

        elif result.AuthorNotFound:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['unfollow:author:not:following']}", color=0xFF0000))

        elif result.AuthorNameNotFound:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

        else:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.unfollow_author method invoked for server: %s, author: %s", filePrefix, ctx.guild_id, ctx.options.authorprofileurl ,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
