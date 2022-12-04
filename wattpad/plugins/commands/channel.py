import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.pluginsimpl.commands.channelimpl import ChannelImpl
from wattpad.utils.hikariutil import HikariUtil

plugin = lightbulb.Plugin("ChannelPlugin")
filePrefix = "wattpad.plugins.commands.channel"
logger = BaseLogger().loggger_init()

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
        logger.info("%s.set_channel method invoked for server: %s", filePrefix, ctx.guild_id)

        guildId= str(ctx.guild_id)
        channelId=ctx.options.channel.id

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #check for required permissions
        perms_result= await HikariUtil().check_channel_permissions(ctx, channelId)

        if perms_result.IsSuccess:
            #call the implementation
            result = await ChannelImpl().set_channel(guildId, channelId)

            if result.IsSuccess:
                msg_description= msgs['set:channel:success'].format(f"{channelId}")
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.set_channel method with permissions for channel: %s, server: %s, Error: %s", filePrefix, channelId, guildId, perms_result.ResultInfo)

            if not perms_result.HasSendPerms and not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:sendandembed:perms']}", color=0xFF0000))
            
            elif not perms_result.HasSendPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:send:perms']}", color=0xFF0000))

            elif not perms_result.HasEmbedPerms:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['perms:error']}", description=f"{msgs['channel:no:embed:perms']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_channel method for server: %s", filePrefix, ctx.guild_id,exc_info=1)
        raise e
    
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.command("unset-channel","New chapter and announcements will not be shared in any channel if you execute this command", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unset_channel(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_channel method invoked for server: %s", filePrefix, ctx.guild_id)

        guildId= str(ctx.guild_id)

        config = Config()

        language = await config.get_language(guildId)
        msgs = await config.get_messages(language)

        #call the implementation
        result = await ChannelImpl().unset_channel(guildId)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['channel:unset:success']}", color=0Xff500a))

        elif result.NoChannel:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['channel:not:set']}", description=f"{msgs['channel:not:set:msg']}", color=0xFF0000))
        
        else:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_channel method invoked for server: %s", filePrefix, ctx.guild_id,exc_info=1)
        raise e
    