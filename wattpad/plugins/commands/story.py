import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger

plugin = lightbulb.Plugin("StoryPlugin")

filePrefix = "wattpad.plugins.commands.story"

logger = BaseLogger().loggger_init()

@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("storyurl", "Url of the story you want to follow",str,required=True)
@lightbulb.command("follow-story","Follow a story to receive new chapter noifications", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def follow_story(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.follow_story method invoked for story: %s", filePrefix, ctx.options.storyurl)

        storyURL = ctx.options.storyurl
        guildId = str(ctx.guild_id)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.follow_story method for story: %s", filePrefix, ctx.options.storyurl, exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)