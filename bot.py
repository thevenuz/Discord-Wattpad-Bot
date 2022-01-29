import os
import hikari
import lightbulb
import json
from lightbulb.ext import tasks
import wattpad as ws
import dotenv

dotenv.load_dotenv()
TOKEN=os.getenv('BOTTOKEN')

bot=lightbulb.BotApp(token=TOKEN, default_enabled_guilds=(906917949888147477, 931555271447293962))
tasks.load(bot)

bot.load_extensions_from('./extensions',must_exist=True)
bot.load_extensions_from('./errorhandler',must_exist=True)

#task for fetching new chapters starts, checks every 2 mins
@tasks.task(m=2, auto_start=True)
async def getnewchapter():
    with open('stories.json', 'r') as s, open('channels.json','r') as f:
        stories=json.load(s)
        channels=json.load(f)
    
    
    for story in stories:
        for key in stories[story]:
            storytitle=str(key).split('/')
            title=storytitle[-1].split('-',1)
            title=title[-1].replace('-',' ')


            newchapter=ws.get_chapter(str(key))
            if newchapter:
                for ch in channels[story]:
                    for nc in newchapter:
                        msg=f'**New chapter from {title}**\n {str(nc)}'
                        await bot.rest.create_message(ch, msg)



#task for fetching new chapters end



@bot.listen(hikari.StartedEvent)
async def msg(event):
    print('bot has started')

#error handler
# @bot.listen(lightbulb.CommandErrorEvent)
# async def on_command_error(event):
#     await event.context.respond('OOPS!! Looks like something went wrong.') 
    #need to check if this works

#error handler


#guild join start
@bot.listen(hikari.GuildJoinEvent)
async def guildjoin(guild):
    with open('channels.json','r') as f:
        channels=json.load(f)

    
    if str(guild.guild_id) not in channels:
        channels[str(guild.guild_id)]=[]

    with open('channels.json','w') as s:
        json.dump(channels,s,indent=2)

    with open('stories.json','r') as s:
        stories=json.load(s)
    
    
    
    if str(guild.guild_id) not in stories:
        stories[str(guild.guild_id)]=[]

    with open('stories.json','w') as f:
        json.dump(stories,f,indent=2)   


#guild join end

#permissions
@lightbulb.Check
def is_AdminOrMod(ctx):
    roles=ctx.member.get_roles()
    if any(role.permissions.all(hikari.Permissions.ADMINISTRATOR) for role in roles) or any(role.permissions.all(hikari.Permissions.MODERATE_MEMBERS) for role in roles):
        return True

    return False

#permissions


@bot.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('ping','get the bot\'s latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    try:
        await ctx.respond(f'**Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms**')
    except Exception as e:
        print(e)








bot.run(activity=hikari.Activity(name="WATTAPD FOR NEW CHAPTERS", type=hikari.ActivityType.WATCHING))