import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.utils.msgutil import MsgUtil
from wattpad.pluginsimpl.commands.storyimpl import StoryImpl

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

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await StoryImpl().follow_story(guildId, storyURL)

        if result.IsSuccess:
            if result.AlreadyFollowing:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['already:following:story']}", color=0xFF0000))
            
            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['follow:story:success']}", color=0Xff500a))

        else:
            if result.InvalidUrl:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['invalid:url']}", description=f"{msgs['invalid:story:url']}", color=0xFF0000))
            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.follow_story method for story: %s", filePrefix, ctx.options.storyurl, exc_info=1)
        raise e
    
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("storyurl","Url of the story you want to unfollow. You can also use title instead of full url", str, required=True)
@lightbulb.command("unfollow-story", "Unfollow a story that you're already following to stop receiving new chapter updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unfollow_story(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unfollow_story method invoked for story: %s, server: %s", filePrefix, ctx.options.storyurl, ctx.guild_id)

        storyUrl = str(ctx.options.storyurl)
        guildId = str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await StoryImpl().unfollow_story(guildId, storyUrl)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['unfollow:story:success']}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.unfollow_story method for story: %s, server: %s, Error: %s", filePrefix, storyUrl, guildId, result.ResultInfo)

            if result.StoryNotFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['unfollow:story:not:following']}", color=0xFF0000))

            elif result.StoryNameNotFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    except Exception as e:
        logger.fatal("Exception occured in %s.unfollow_story method for story: %s, server: %s", filePrefix, ctx.options.storyurl, ctx.guild_id, exc_info=1)
        raise e
    
@plugin.command
@lightbulb.command("check-stories","check the stories that you are following in this server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_stories(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.check_stories method invoked for server: %s", filePrefix, ctx.guild_id)

        guildId= str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call implementation
        result = await StoryImpl().check_stories(guildId)

        if result.IsSuccess:
            if result.Data:
                response = await MsgUtil().build_check_authors_msg(result.Data[0])
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['check:stories:following']}", description=f"{response}", color=0Xff500a))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['empty']}", description=f"{msgs['check:stories:empty']}", color=0xFF0000))

        else:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    except Exception as e:
        logger.fatal("Exception occured in %s.check_stories method invoked for server: %s", filePrefix, ctx.guild_id, exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)