import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.pluginsimpl.commands.authorimpl import AuthorImpl


plugin = lightbulb.Plugin("AuthorPlugin")

file_prefix = "wattpad.plugins.commands.author"

logger = BaseLogger().loggger_init()


@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR) | lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS) | lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS) | lightbulb.owner_only)
@lightbulb.option("authorprofileurl", "Url of the Author's profile you want to follow", str, required=True)
@lightbulb.command("follow-author", "Follow an author to receive new announcements from the author", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def follow_author(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.follow_author method invoked for author: %s, server: %s", file_prefix, ctx.options.authorprofileurl, ctx.guild_id)

        profileUrl = ctx.options.authorprofileurl
        guildId = str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call implementation
        result = await AuthorImpl().follow_author(guildId, profileUrl)

    except Exception as e:
        logger.fatal("Exception occured in %s.follow_author method for author: %s, server: %s", file_prefix, ctx.options.authorprofileurl, ctx.guild_id, exc_info=1)
        raise e


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
