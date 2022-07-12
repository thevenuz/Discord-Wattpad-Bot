import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.commandsexec.customchannelexec import CustomChannlExec
from wattpad.utils.config import Config
from wattpad.utils.hikariutil import HikariUtil

plugin= lightbulb.Plugin("CustomChannelPlugin")

file_prefix= "wattpad.plugins.commands.customchannel"
logger=BaseLogger().loggger_init()


@plugin.command()
@lightbulb.command("set-custom-channel","set a custom channel for bot to send updates for particular stories/announcements",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_custom_channel(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_channel method invoked for server: %s", file_prefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
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
        logger.info("%s.set_custom_channel_for_story method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channel_id= ctx.options.channel.id
        storyurl= ctx.options.url

        msgs= await Config().get_messages("en")

        #check for required permissions
        perms_result= await HikariUtil().check_channel_perms(ctx, channel_id)

        if perms_result.IsSuccess:
            #call the exec
            result= await CustomChannlExec().set_custom_channel_for_story(guildId, channel_id, storyurl)

            if result.IsSuccess:
                msg_description= msgs['custom:channel:story:success'].format(f"{storyurl}", f"{channel_id}")
                
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:channel:success']}", description=f"{msg_description}", color=0xFF0000))

            else:
                logger.error("error occured in %s.set_custom_channel_for_story for server: %s, channel: %s, story: %s", file_prefix, guildId, channel_id, storyurl)
                if result.HasMultipleResults:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

                else:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.set_custom_channel_for_story method with permissions for channel: %s, server: %s, Error: %s", file_prefix, channel_id, guildId, perms_result.ResultInfo)

            if not perms_result.HasSendPerms and not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:sendandembed:perms']}", color=0xFF0000))
            
            elif not perms_result.HasSendPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:send:perms']}", color=0xFF0000))

            elif not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:embed:perms']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel_for_story method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
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
        logger.info("%s.set_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channel_id= ctx.options.channel.id
        authorurl= ctx.options.url

        msgs= await Config().get_messages("en")

        #check for required permissions
        perms_result= await HikariUtil().check_channel_perms(ctx, channel_id)

        if perms_result.IsSuccess:
            #call the exec
            result= await CustomChannlExec().set_custom_channel_for_author(guildId, channel_id, authorurl)

            if result.IsSuccess:
                msg_description= msgs['custom:channel:author:success'].format(f"{authorurl}", f"{channel_id}")
                
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:channel:success']}", description=f"{msg_description}", color=0xFF0000))

            else:
                logger.error("error occured in %s.set_custom_channel_for_author for server: %s, channel: %s, story: %s", file_prefix, guildId, channel_id, authorurl)
                if result.HasMultipleResults:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['author:multiple:title']}", color=0xFF0000))

                else:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.set_custom_channel_for_author method with permissions for channel: %s, server: %s, Error: %s", file_prefix, channel_id, guildId, perms_result.ResultInfo)

            if not perms_result.HasSendPerms and not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:sendandembed:perms']}", color=0xFF0000))
            
            elif not perms_result.HasSendPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:send:perms']}", color=0xFF0000))

            elif not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:embed:perms']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
        raise e
    

@plugin.command()
@lightbulb.command("unset-custom-channel","Unset a custom channel for bot to send updates for particular stories/announcements",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def unset_custom_channel(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_channel method invoked for server: %s", file_prefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_channel method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e


@unset_custom_channel.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.option("channel","Select the channel which you want to remove as a custom channel.",
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("for-story","unset a custom channel for stories in which the bot shares the updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unset_custom_channel_for_story(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channelid= ctx.options.channel.id
        storyurl= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomChannlExec().unset_custom_channel_for_story(guildId, channelid, storyurl)

        if result.IsSuccess:
            msg_description= msgs['unset:custom:channel:story:success'].format(f"{channelid}", f"{storyurl}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0xFF0000))

        else:
            logger.error("Error in %s.unset_custom_channel_for_story method for server: %s, channel: %s, story: %s, error: %s", file_prefix, guildId, channelid, storyurl, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

            elif result.Notfound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['custom:channel:not:set:story']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_channel_for_story method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
        raise e
    
@unset_custom_channel.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.option("channel","Select the channel which you want to remove as a custom channel.",
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("for-author","unset a custom channel for author in which the bot shares the updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unset_custom_channel_for_author(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url)

        guildId= str(ctx.guild_id)
        channelid= ctx.options.channel.id
        authorurl= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomChannlExec().unset_custom_channel_for_author(guildId, channelid, authorurl)

        if result.IsSuccess:
            msg_description= msgs['unset:custom:channel:story:success'].format(f"{channelid}", f"{authorurl}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0xFF0000))

        else:
            logger.error("Error in %s.unset_custom_channel_for_author method for server: %s, channel: %s, author: %s, error: %s", file_prefix, guildId, channelid, authorurl, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['author:multiple:title']}", color=0xFF0000))

            elif result.Notfound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['custom:channel:not:set:author']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_channel_for_author method invoked for server: %s, channel: %s, url: %s", file_prefix, ctx.guild_id, ctx.options.channel.id, ctx.options.url,exc_info=1)
        raise e

@plugin.command
@lightbulb.option("category","Select whether you want to check story/author custom channels",str, choices=("story", "announcements"), required=False)
@lightbulb.command("check-custom-channels", "Check the custom channels for stories and author updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_custom_channels(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.check_custom_channels method invoked for server: %s, category: %s", file_prefix, ctx.guild_id, ctx.options.category)

        guildId= str(ctx.guild_id)
        category= ctx.options.category

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomChannlExec().
    
    except Exception as e:
        logger.fatal("Exception occured in %s.check_custom_channels method invoked for server: %s, category: %s", file_prefix, ctx.guild_id, ctx.options.category,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin) 