import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.commandsexec.channelexec import ChannelExec
from wattpad.utils.channelutil import Channelutil
from wattpad.utils.config import Config
from wattpad.utils.hikariutil import HikariUtil

plugin= lightbulb.Plugin("ChannelPlugin")

file_prefix= "wattpad.plugins.commands.channel"

logger=BaseLogger().loggger_init()

@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("channel","Select the channel in which you want to receive updates.",
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("set-channel","sets a channel to receive new chapter notifications", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def set_channel(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_channel method invoked for server: %s", file_prefix, ctx.guild_id)

        guildId= str(ctx.guild_id)
        channel_id=ctx.options.channel.id

        msgs= await Config().get_messages("en")

        #check for required permissions
        perms_result= await HikariUtil().check_channel_perms(ctx, channel_id)

        
        if perms_result.IsSuccess:
            #call the exec
            result= await ChannelExec().set_channel(guildid=guildId, channelid=channel_id)

            if result.IsSuccess:
                msg_description= msgs['set:channel:success'].format(f"{channel_id}")
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

            else:
                logger.error("Error occured in %s.set_channel method for channel: %s, server: %s, Error: %s", file_prefix, channel_id, guildId, result.ResultInfo)

                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.set_channel method with permissions for channel: %s, server: %s, Error: %s", file_prefix, channel_id, guildId, perms_result.ResultInfo)

            if not perms_result.HasSendPerms and not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:sendandembed:perms']}", color=0xFF0000))
            
            elif not perms_result.HasSendPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:send:perms']}", color=0xFF0000))

            elif not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:embed:perms']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_channel method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e
    
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.command("unset-channel","New chapter and announcements will not be shared in any channel if you execute this command", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unset_channel(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_channel method invoked for server: %s", file_prefix, ctx.guild_id)

        guildId= str(ctx.guild_id)
        msgs= await Config().get_messages("en")

        #call the exec
        result= await ChannelExec().unset_channel(guildId)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['channel:unset:success']}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.unset_channel for server: %s, Error: %s", file_prefix, guildId, result.ResultInfo)

            if result.NoChannelFound:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['channel:not:set']}", description=f"{msgs['channel:not:set:msg']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_channel method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e
    
@plugin.command
@lightbulb.command("check-channels", "Check in which channel the new chapter and announcement updates are being shared currently", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_channels(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.check_channels method invoked for server: %s", file_prefix, ctx.guild_id)

        guildId= str(ctx.guild_id)
        msgs= await Config().get_messages("en")

        #call the exec
        result= await ChannelExec().check_channels(guildId)

        if result.IsSuccess:
            channel_data= await Channelutil().build_channel_data_msg(result.Data)
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['check:channels:title']}", description=f"{channel_data}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.check_channels for server: %s, error: %s", file_prefix, guildId, result.ResultInfo)

            if result.IsEmpty:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['empty']}", description=f"{msgs['check:channels:empty']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

    
    except Exception as e:
        logger.fatal("Exception occured in %s.check_channels method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)