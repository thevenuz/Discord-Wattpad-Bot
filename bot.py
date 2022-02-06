import os
import hikari
import lightbulb
import json
from lightbulb.ext import tasks
import wattpad as ws
import dotenv
import logging

dotenv.load_dotenv()
TOKEN=os.getenv('BOTTOKEN')

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

bot=lightbulb.BotApp(token=TOKEN)
tasks.load(bot)

bot.load_extensions_from('./extensions',must_exist=True)
bot.load_extensions_from('./errorhandler',must_exist=True)


@bot.listen(hikari.StartedEvent)
async def msg(event):
    print('bot has started')


#task for fetching new chapters starts, checks every 2 mins
@tasks.task(m=2, auto_start=True)
async def getnewchapter():
    try:
        logger.error('task triggered')
        with open('stories.json', 'r') as s, open('channels.json','r') as f:
            stories=json.load(s)
            channels=json.load(f)
        
        
        for story in stories:
            for key in stories[story]:
                logger.info('Cheking for a new story of %s',key)
                storytitle=str(key).split('/')
                title=storytitle[-1].split('-',1)
                title=title[-1].replace('-',' ')

                try:
                    newchapter= await ws.get_chapter(str(key))
                    if newchapter:
                        for ch in channels[story]:
                            for nc in newchapter:
                                msg=f'**New chapter from {title}**\n {str(nc)}'
                            await bot.rest.create_message(ch, msg)

                except Exception as e:
                    logger.fatal('Error occured in wattpad get_chapter method', exc_info=1)
                    raise e
            
    except Exception as e:
        logger.critical('Error in getnewchapter task:',exc_info=1)
        pass



#task for fetching new chapters end





#guild join start
@bot.listen(hikari.GuildJoinEvent)
async def guildjoin(guild: hikari.GuildJoinEvent):
    logger.info('Guild Join event has been triggered for %s', guild.guild_id)
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

    try:
        descwhat='Whenever you write a new chapter in your story and publish it, this bot will automatically fetch the new chapter\'s URL and post it in your server.'
        deschow='Specify the channel/channels, story/stories that you wish to receive the new chapter updates.\nOnly members with ADMIN or MODMEMBERS permission can use the commands. That\'s it. New chapter links of the stories will be posted in the added channels whenever a new chapter is published.'
        desccmd='This bot supports the new slash commands, so the prefix for all the commands is `/`. All the commands are self explanatory. Please use `/help` for more details about commands.'
        descother1='Bot works pretty well already but consider this as a beta and it will be improved over time.'
        descother2='Sometimes the slash commands take some time to register and appear in the server. So please be patient for an hour or so if the commands do not appear.'
        descother3='Bot supports multiple servers.'
        descother=f'{descother1}\n{descother2}\n{descother3}\n'

        em=hikari.Embed(title='Thanks for inviting Wattapd bot to your server! Here\'s a rundown of this bot.',  color=0Xff500a)
        em.add_field(name='What is this bot capable of?',value=descwhat)
        em.add_field(name='How does this bot work?', value=deschow)
        em.add_field(name='How to use the commands?', value=desccmd)
        #em.add_field(name='Other stuff:', value=descother)

        for k,v in guild.channels.items():
            if v.parent_id:
                defaultchannel=k
                await guild.app.rest.create_message(defaultchannel, embed=em)
                break

    except Exception as e:
        logger.critical('Error in sending welcome msg for guild %s', guild.guild_id, exc_info=1)
        raise e


#guild join end




@bot.command
@lightbulb.command('ping','get the bot\'s latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    try:
        await ctx.respond(f'**Bot\'s Latency: {bot.heartbeat_latency*1000:.2f}ms**')
    except Exception as e:
        logger.critical('Error with Ping command for guild %s',ctx.guild_id, exc_info=1)
        raise e


bot.run(activity=hikari.Activity(name="WATTAPD FOR NEW CHAPTERS", type=hikari.ActivityType.WATCHING))