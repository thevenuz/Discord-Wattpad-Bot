import hikari
import lightbulb
from lightbulb.ext import tasks
from wattpad.utils.config import Config
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.db import DBConfig

file_prefix= "bot"
logger= BaseLogger().loggger_init()

settings= Config().load_settings()

TOKEN= settings.Token
LOGCHANNEL= settings.LogChannel
PUBLICLOGCHANNEL= settings.PublicLogChannel

bot=lightbulb.BotApp(token=TOKEN)

#initialize oracle client path upon startup
DBConfig().initialize_oracle_client_path()

tasks.load(bot)

bot.load_extensions_from("./wattpad/plugins/commands",must_exist=True)
bot.load_extensions_from("./wattpad/plugins/events",must_exist=True)
bot.load_extensions_from("./wattpad/plugins/tasks",must_exist=True)
bot.load_extensions_from("./wattpad/plugins/errorhandler",must_exist=True)


@bot.listen(hikari.StartedEvent)
async def msg(event):
    print("bot has started...")

@bot.command
@lightbulb.command("ping","check the bot's latency")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    try:
        await ctx.respond(f'**Bot\'s Latency: {bot.heartbeat_latency*1000:.2f}ms**')
    except Exception as e:
        logger.critical("Exception occured in %s.ping command for server: %s", file_prefix, ctx.guild_id, exc_info=1)
        raise e


bot.run(activity=hikari.Activity(name="WATTAPD FOR NEW CHAPTERS", type=hikari.ActivityType.WATCHING))