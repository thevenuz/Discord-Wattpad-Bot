import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.commandsexec.channelexec import ChannelExec
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
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['set:channel:success']}", color=0xFF0000))

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
    



def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)