import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.meta.models.result import ResultPermissionsCheck

class HikariUtil:
    def __init__(self) -> None:
        self.file_prefix= "wattpad.utils.hikariutil"
        self.logger= BaseLogger().loggger_init()

    async def check_channel_perms(self, ctx: lightbulb.SlashContext, channelid:str) -> ResultPermissionsCheck:
        try:
            self.logger.info("%s.check_channel_read_perms method invoked for server: %s, channel: %s", self.file_prefix, ctx.guild_id, channelid)

            has_send_perms= False
            has_embed_perms= False
            has_read_perms= False

            channelobj= await ctx.bot.rest.fetch_channel(channelid)
            bot_member= ctx.bot.cache.get_member(ctx.guild_id, ctx.bot.get_me())
            
            perms= lightbulb.utils.permissions_in(channelobj, bot_member)

            if perms:
                if hikari.Permissions.VIEW_CHANNEL in perms:
                    has_read_perms= True

                if hikari.Permissions.SEND_MESSAGES in perms:
                    has_send_perms=True

                if hikari.Permissions.EMBED_LINKS in perms:
                    has_embed_perms=True

                if has_send_perms and has_embed_perms:
                    return ResultPermissionsCheck(True, "success", HasReadPerms=has_read_perms, HasSendPerms=has_send_perms, HasEmbedPerms=has_embed_perms)
                else:
                    return ResultPermissionsCheck(False, "The bot doesn't have required send permissions", HasReadPerms=has_read_perms, HasSendPerms=has_send_perms, HasEmbedPerms=has_embed_perms)

            return ResultPermissionsCheck(False, "No perissions were found")
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s.check_channel_read_perms method invoked for server: %s, channel: %s", self.file_prefix, ctx.guild_id, channelid,exc_info=1)
            raise e
    
    async def send_story_update(self, serverid: str, channelid: str, msg:str, chapterlink: str) -> bool:
        try:
            self.logger.info("%s.send_story_update method invoked for server: %s, channel: %s, msg: %s, chapter: %s", self.file_prefix, serverid, channelid, msg, chapterlink)

            
        
        except Exception as e:
            self.logger.fatal("Exception occured in %s. method",exc_info=1)
            raise e
        