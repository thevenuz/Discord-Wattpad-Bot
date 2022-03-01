from datetime import datetime
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
LOGCHANNEL=os.getenv('LOGCHANNEL')

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

#region tasks

#region get new chapter task
#task for fetching new chapters, checks every 2 mins
@tasks.task(m=2, auto_start=True)
async def getnewchapter():
    try:
        logger.info('task triggered')
        with open('stories.json', 'r') as s, open('channels.json','r') as f:
            stories=json.load(s)
            channels=json.load(f)
        
        for guild,story in stories.items():
            for sty in story:
                if sty:
                    key=sty['url']
                    lastchecked=sty['lastupdated']
                    logger.info('Cheking for a new story of %s',key)
                    title=''
                    if 'utm' not in key:
                        storytitle=str(key).split('/')
                        title=storytitle[-1].split('-',1)
                        title=title[-1].replace('-',' ')
                        title=f'from {title}'

                    try:
                        newchapter= await ws.get_chapter(str(key),lastchecked)
                        if newchapter:
                            for ch in channels[guild]:
                                for nc in newchapter[0]:
                                    msg=f'**New chapter {title}**\n {str(nc)}'
                                await bot.rest.create_message(ch, msg)

                            sty['lastupdated']=f'{newchapter[1]}'
                            with open('stories.json','w') as s:
                                json.dump(stories,s,indent=2)

                        

                    except Exception as e:
                        logger.fatal('Error occured in wattpad get_chapter method', exc_info=1)
                        raise e
          
    except Exception as e:
        logger.critical('Error in getnewchapter task:',exc_info=1)
        pass

#endregion get new chapter


#region get new announcement task
#task for fetching new announcements from authors
@tasks.task(m=3,auto_start=True)
async def get_announcement():
    try:
        logger.info('get announcement task triggered')
        with open('authors.json','r') as a, open('channels.json','r') as c:
            authors=json.load(a)
            channels=json.load(c)

        for guild, author in authors.items():
            for auth in author:
                if auth:
                    profile=auth['url']
                    lastchecked=auth['lastupdated']
                    author_name=auth['url'].split('/user/')[1].replace('-',' ')


                    try:
                        new_announcement=await ws.get_new_announcement(profile,lastchecked)
                        # new_announcement_text=new_announcement
                        # new_updated_time=datetime.utcnow()
                        if new_announcement:
                            for ch in channels[guild]:
                                if new_announcement[0]:
                                    msg=f'New Announcement from **{author_name}**'
                                    em=hikari.Embed(title='Announcement:',description=f'{new_announcement[0]}',color=0Xff500a)
                                    await bot.rest.create_message(ch,embed=em,content=msg)

                            auth['lastupdated']=str(new_announcement[1])
                            with open('authors.json','w') as a:
                                json.dump(authors,a,indent=2)

                    except Exception as e:
                        logger.fatal('Exception occured in task get_announcement method for author: %s',profile,exc_info=1)
                        pass

                

    except Exception as e:
        logger.critical('Exception occured in get announcement task:', exc_info=1)
        raise e

#endregion get new announcement

#endregion tasks


#region events
#region guild join event
@bot.listen(hikari.GuildJoinEvent)
async def guildjoin(guild: hikari.GuildJoinEvent):
    try:
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

        with open('authors.json','r') as a:
            authors=json.load(a)

        if str(guild.guild_id) not in authors:
            authors[str(guild.guild_id)]=[]

        with open('authors.json','w') as a:
            json.dump(authors,a,indent=2)
        

       
        #region not using
        # try:
        #     descwhat='Whenever you write a new chapter in your story and publish it, this bot will automatically share the new chapter\'s link in your server.'
        #     deschow1=''
        #     deschow='Specify the channel/channels, story/stories that you wish to receive the new chapter updates.\nOnly members with ADMIN or MODMEMBERS permission can use the commands. That\'s it. New chapter links of the stories will be posted in the added channels whenever a new chapter is published.'
        #     desccmd='This bot supports the new slash commands, so the prefix for all the commands is `/`. All the commands are self explanatory. Please use `/help` for more details about commands.'
        #     descother1='Bot works pretty well already but consider this as a beta and it will be improved over time.'
        #     descother2='Sometimes the slash commands take some time to register and appear in the server. So please be patient for an hour or so if the commands do not appear.'
        #     descother3='Bot supports multiple servers.'
        #     descother=f'{descother1}\n{descother2}\n{descother3}\n'

        #     em=hikari.Embed(title='Thanks for adding the bot to your server! Here\'s a rundown of this bot.',  color=0Xff500a)
        #     em.add_field(name='What does this bot do?',value=descwhat)
        #     em.add_field(name='How to use the bot?', value=deschow)
        #     em.add_field(name='How to use the commands?', value=desccmd)
        #     #em.add_field(name='Other stuff:', value=descother)

        #     if created_channel:
        #         await guild.app.rest.create_message(created_channel.id,embed=em)
            
        #     else:
        #         for k,v in guild.channels.items():
        #             if v.parent_id:
        #                 defaultchannel=k
        #                 await guild.app.rest.create_message(defaultchannel, embed=em)
        #                 break

        # except Exception as e:
        #     logger.critical('Error in sending welcome msg for guild %s', guild.guild_id, exc_info=1)
        #     pass

        # try:
        #     joinmsg=f'Bot joined a new server guild Id: {guild.guild_id} and server name: {guild.guild.name}'
        #     await bot.rest.create_message(LOGCHANNEL,joinmsg)
        # except Exception as e:
        #     logger.fatal('Excpetion occured when sending join msg to log server for guild Id: %s and server name: %s',guild.guild_id,guild.old_guild.name)
        #     pass
        #endregion not using
    except Exception as e:
        logger.critical('Error in guild join event for guild %s', guild.guild_id, exc_info=1)
        pass

#endregion guild join event



#region Guild leave event 
@bot.listen(hikari.GuildLeaveEvent)
async def guildLeave(guild: hikari.GuildLeaveEvent):
    try:
        logger.error('Guild leave event triggered for the guild: %s, guild name: %s', guild.guild_id, guild.old_guild.name)
        with open('stories.json', 'r') as s, open('channels.json','r') as f:
            stories=json.load(s)
            channels=json.load(f)

        if guild.guild_id:
            if str(guild.guild_id) in channels:
                del channels[str(guild.guild_id)]
            if str(guild.guild_id) in stories:
                del stories[str(guild.guild_id)]

        with open('stories.json', 'w') as s, open('channels.json','w') as f:
            json.dump(channels,f,indent=2)
            json.dump(stories,s,indent=2)

        try:
            joinmsg=f'Bot left a server guild Id: {guild.guild_id} and server name: {guild.old_guild.name}'
            await bot.rest.create_message(LOGCHANNEL,joinmsg)
        except Exception as e:
            logger.fatal('Excpetion occured when sending leave msg to log server for guild: %s and server name: %s',guild.guild_id,guild.old_guild.name)
            pass

    except Exception as e:
        logger.fatal('Exception has occured in Guild leave event for guild: %s', guild.guild_id)
        pass

#endregion Guild leave event

#endregion events

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