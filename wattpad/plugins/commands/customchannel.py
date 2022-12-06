import hikari
import lightbulb
from wattpad.pluginsimpl.commands.customchannelimpl import CustomChannelImpl
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.utils.hikariutil import HikariUtil

plugin= lightbulb.Plugin("CustomChannelPlugin")
filePrefix= "wattpad.plugins.commands.customchannel"
logger=BaseLogger().loggger_init()

@plugin.command()
@lightbulb.command("set-custom-channel","set a custom channel for bot to send updates for particular stories/announcements",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_custom_channel(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_channel method invoked for server: %s", filePrefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0Xff500a))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel method for server: %s", filePrefix, ctx.guild_id, exc_info=1)
        raise e

@set_custom_channel.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.option("channel","Select the channel which you want as a custom channel for updates.",
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("for-story","set a custom channel for stories in which the bot shares the updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_channel_for_story(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_channel_for_story method invoked for server: %s, channel: %s, url: %s", filePrefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channelId= ctx.options.channel.id
        storyUrl= ctx.options.url

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #check for required permissions
        perms_result= await HikariUtil().check_channel_permissions(ctx, channelId)

        if perms_result.IsSuccess:
            #call the implementation
            result = await CustomChannelImpl().set_custom_channel_for_story(guildId, channelId, storyUrl)

            if result.IsSuccess:
                response= msgs['custom:channel:story:success'].format(f"{result.StoryName}", f"{channelId}")
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:channel:success']}", description=f"{response}", color=0Xff500a))

            else:
                logger.error("error occured in %s.set_custom_channel_for_story for server: %s, channel: %s, story: %s", filePrefix, guildId, channelId, storyUrl)

                if result.NoStoryFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

                elif result.MultipleStoriesFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

                else:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.set_custom_channel_for_story method with permissions for channel: %s, server: %s, Error: %s", filePrefix, channelId, guildId, perms_result.ResultInfo)

            if not perms_result.HasSendPerms and not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:sendandembed:perms']}", color=0xFF0000))
            
            elif not perms_result.HasSendPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:send:perms']}", color=0xFF0000))

            elif not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:embed:perms']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel_for_story method for server: %s, channel: %s, url: %s", filePrefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
        raise e
    
@set_custom_channel.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the author profile",str, required=True)
@lightbulb.option("channel","Select the channel which you want as a custom channel for updates.",
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("for-author","set a custom channel for authors in which the bot shares the updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_channel_for_author(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", filePrefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channelId= ctx.options.channel.id
        authorUrl = ctx.options.url

        config = Config()

        language = await config.get_language(guildId)

        msgs = await config.get_messages(language)

        #check for required permissions
        perms_result= await HikariUtil().check_channel_permissions(ctx, channelId)    

        if perms_result.IsSuccess:
            #call the implementation
            result = await CustomChannelImpl().set_custom_channel_for_author(guildId, channelId, authorUrl)

            if result.IsSuccess:
                response = msgs['custom:channel:author:success'].format(f"{result.AuthorName}", f"{channelId}")
                
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:channel:success']}", description=f"{response}", color=0Xff500a))

            else:
                logger.error("error occured in %s.set_custom_channel_for_author for server: %s, channel: %s, author: %s", filePrefix, guildId, channelId, authorUrl)

                if result.NoAuthorNameFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

                elif result.MultipleAuthorsFound:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['author:multiple:title']}", color=0xFF0000))

                else:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", filePrefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
        raise e
    