import hikari
import lightbulb
from wattpad.utils.config import Config
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsimpl.commands.custommessageimpl import CustomMessageImpl

plugin = lightbulb.Plugin("CustomMessagePlugin")
filePrefix = "wattpad.plugins.commands.custommessage"
logger = BaseLogger().loggger_init()

@plugin.command()
@lightbulb.command("set-custom-message","set a custom message for bot to use while sharing updates",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_custom_message(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message method invoked for server: %s", filePrefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0Xff500a))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message method invoked for server: %s", filePrefix, ctx.guild_id,exc_info=1)
        raise e

@set_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str)
@lightbulb.option("message","Your custom message for story updates",required=True)
@lightbulb.command("for-story","set a custom messages for a particular story", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_message_for_story(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message)

        guildId= str(ctx.guild_id)
        message= ctx.options.message
        storyUrl= ctx.options.url

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await CustomMessageImpl().set_custom_message_for_story(guildId, storyUrl, message)

        if result.IsSuccess:
            if storyUrl:
                response = msgs['custom:msg:set:story:success'].format(f"{message}", f"{storyUrl}")
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{response}", color=0Xff500a))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['custom:msg:set:story:category:success']}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.set_custom_message_for_story method for server: %s, story: %s, msg: %s, error: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message, result.ResultInfo)

            if result.NoStoryNameFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.NoStoryFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['unfollow:story:not:following']}", color=0xFF0000))
            
            elif result.MultipleStoriesFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message, exc_info=1)
        raise e
    
@set_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the Author",str)
@lightbulb.option("message","Your custom message for author's announcements",required=True)
@lightbulb.command("for-announcements","set a custom messages for a particular author's announcements", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_message_for_author(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message)

        guildId= str(ctx.guild_id)
        message= ctx.options.message
        storyUrl= ctx.options.url

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await CustomMessageImpl().set_custom_message_for_author(guildId, storyUrl, message)

        if result.IsSuccess:
            if storyUrl:
                response = msgs['custom:msg:set:author:success'].format(f"{message}", f"{storyUrl}")
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{response}", color=0Xff500a))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['custom:msg:set:author:category:success']}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.set_custom_message_for_author method for server: %s, author: %s, msg: %s, error: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message, result.ResultInfo)

            if result.NoAuthorNameFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.NoAuthorFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['unfollow:author:not:following']}", color=0xFF0000))
            
            elif result.MultipleAuthorsFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['author:multiple:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", filePrefix, ctx.guild_id, ctx.options.url, ctx.options.message,exc_info=1)
        raise e
    
