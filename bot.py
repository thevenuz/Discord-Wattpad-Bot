import hikari
import lightbulb
from lightbulb.ext import tasks
from wattpad.utils.config import Config

settings = Config().load_settings()

TOKEN = settings.Token
LOGCHANNEL = settings.LogChannel
PUBLICLOGCHANNEL = settings.PublicLogChannel

bot = lightbulb.BotApp(token=TOKEN)

tasks.load(bot)

bot.load_extensions_from('./wattpad/plugins/commands', must_exist=True)
bot.load_extensions_from('./wattpad/plugins/events', must_exist=True)
bot.load_extensions_from('./wattpad/plugins/errorhandler', must_exist=True)
bot.load_extensions_from('./wattpad/plugins/tasks', must_exist=True)


@bot.listen(hikari.StartedEvent)
async def msg(event):
    print('bot has started')


bot.run(activity=hikari.Activity(name="WATTPAD FOR NEW CHAPTERS & ANNOUNCEMENTS", type=hikari.ActivityType.WATCHING))
