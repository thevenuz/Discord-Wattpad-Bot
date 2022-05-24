from datetime import datetime
import os
import hikari
import lightbulb
import json
from lightbulb.ext import tasks
import wattpad as ws
import dotenv
import logging
import helpers.message_helper as customMsghelper
import helpers.wattpad_helper as wpad
import helpers.custom_channel_helper as customchnlhelper
import aiofiles

dotenv.load_dotenv()
TOKEN=os.getenv('BOTTOKEN')
LOGCHANNEL=os.getenv('LOGCHANNEL')
PUBLICLOGCHANNEL=os.getenv('PUBLICLOGCHANNEL')

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="bot")
logger.setLevel(logging.DEBUG)

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
        logger.info("getnewchapter task started")
        # with open('stories.json', 'r') as s, open('channels.json','r') as f:
        #     stories=json.load(s)
        #     channels=json.load(f)

        
        #async implementation of reading from files
        async with aiofiles.open("stories.json",mode="r") as s,aiofiles.open("channels.json",mode="r") as c:
            stories=json.loads(await s.read())
            channels=json.loads(await c.read())


        for guild,story in stories.items():
            for sty in story:
                if sty:
                    storyURL=sty["url"]
                    lastchecked=sty['lastupdated']
                    logger.info('Cheking for a new story of %s',storyURL)
                   

                    try:
                        #check if the guild Id is in channels.json or if any custom channel is setup for this story
                        custom_channel=await customchnlhelper.get_custom_channel(guild,storyURL,"story")

                        if guild in channels:
                            if channels[guild] or custom_channel:
                                newchapter= await ws.get_chapter(str(storyURL),lastchecked)
                                if newchapter:
                                    for ch in channels[guild]:
                                        for nc in newchapter[0]:

                                            if custom_channel:
                                                ch=custom_channel

                                            #check if there is a custom msg setup. else generate a default msg
                                            customMsg=await customMsghelper.get_story_custommessage(guild, storyURL)
                                            if customMsg!="" and customMsg is not None:
                                                msg=f"{customMsg}\n{str(nc)}"

                                            else:
                                                #get story title from story link to send in msg description
                                                storyTitle=""
                                                if "utm" not in storyURL:
                                                    try:
                                                        storyTitle=await wpad.get_story_title(storyURL)
                                                    except:
                                                        pass

                                                if storyTitle:
                                                    storyTitle=f"from {storyTitle}"

                                                msg=f'**New chapter {storyTitle}**\n {str(nc)}'

                                            # #check if a custom message has been setup for this server
                                            # customMsg=await customMsghelper.get_story_custommessage(guild)
                                            # if customMsg!="" and customMsg is not None:
                                            #     msg=f"{customMsg}\n{str(nc)}"
                                            
                                        await bot.rest.create_message(ch, msg)

                                        sty['lastupdated']=f'{newchapter[1]}'
                                        # with open('stories.json','w') as s:
                                        #     json.dump(stories,s,indent=2)

                                        #async implementation of writing into json file
                                        async with aiofiles.open("stories.json",mode="w") as s:
                                            await s.write(json.dumps(stories,indent=2))

        

                        

                    except Exception as e:
                        logger.fatal('Error occured in wattpad get_chapter method', exc_info=1)
                        raise e

        logger.info("getnewchapter task ended")
     
    except Exception as e:
        logger.critical('Error in getnewchapter task:',exc_info=1)
        pass

#endregion get new chapter


#region get new announcement task
#task for fetching new announcements from authors
@tasks.task(m=3,auto_start=True)
async def get_announcement():
    try:
        logger.info("get_announcement task started")


        # with open('authors.json','r') as a, open('channels.json','r') as c:
        #     authors=json.load(a)
        #     channels=json.load(c)

        #async implementation of reading from json file
        async with aiofiles.open("authors.json",mode="r") as a, aiofiles.open("channels.json",mode="r") as c:
            authors=json.loads(await a.read())
            channels=json.loads(await c.read())

        for guild, author in authors.items():
            for auth in author:
                if auth:
                    profile=auth['url']
                    lastchecked=auth['lastupdated']
                    author_name=auth['url'].split('/user/')[1].replace('-',' ')
                #check if the guild Id is in channels.json or if any custom channel is setup for this story
                custom_channel=await customchnlhelper.get_custom_channel(guild,profile,"author")
                if guild in channels:
                    if channels[guild] or custom_channel:
                        try:
                            new_announcement=await ws.get_new_announcement(profile,lastchecked)
                            if new_announcement:
                                for ch in channels[guild]:
                                    if new_announcement[0]:
                                        if custom_channel:
                                            ch=custom_channel

                                        msg=f'New Announcement from **{author_name}**'

                                        #check if a custom announcement msg has been setup for this server
                                        customMsg=await customMsghelper.get_announcement_custommessage(guild,profile)
                                        if customMsg!="" and customMsg is not None:
                                            msg=customMsg

                                        em=hikari.Embed(title='Announcement:',description=f'{new_announcement[0]}',color=0Xff500a)
                                        await bot.rest.create_message(ch,embed=em,content=msg)

                                auth['lastupdated']=str(new_announcement[1])

                                # with open('authors.json','w') as a:
                                #     json.dump(authors,a,indent=2)

                                #async implementation of writing to json files
                                async with aiofiles.open("authors.json",mode="w") as a:
                                    await a.write(json.dumps(authors,indent=2))


                    

                        except Exception as e:
                            logger.fatal('Exception occured in task get_announcement method for author: %s',profile,exc_info=1)
                            pass
        logger.info("get_announcement task ended")

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

        #async impl of reading from json files
        async with aiofiles.open("stories.json",mode="r") as s, aiofiles.open("authors.json",mode="r") as a, aiofiles.open("channels.json",mode="r") as c:
            stories=json.loads(await s.read())
            authors=json.loads(await a.read())
            channels=json.loads(await c.read())


        # with open('channels.json','r') as f:
        #     channels=json.load(f)
        

        if str(guild.guild_id) not in channels:
            channels[str(guild.guild_id)]=[]

        # with open('channels.json','w') as s:
        #     json.dump(channels,s,indent=2)

        # with open('stories.json','r') as s:
        #     stories=json.load(s)

        if str(guild.guild_id) not in stories:
            stories[str(guild.guild_id)]=[]

        # with open('stories.json','w') as f:
        #     json.dump(stories,f,indent=2)

        # with open('authors.json','r') as a:
        #     authors=json.load(a)

        if str(guild.guild_id) not in authors:
            authors[str(guild.guild_id)]=[]

        # with open('authors.json','w') as a:
        #     json.dump(authors,a,indent=2)


        #async impl of writing to json files
        async with aiofiles.open("stories.json",mode="w") as s, aiofiles.open("authors.json",mode="w") as a, aiofiles.open("channels.json",mode="w") as c:
            await s.write(json.dumps(stories,indent=2))
            await a.write(json.dumps(authors,indent=2))
            await c.write(json.dumps(channels,indent=2))
            

        try:
            joinmsg=f'Bot joined a new server guild Id: {guild.guild_id} and server name: {guild.guild.name}'
            publicJoinMsg=f"Bot joined a new server: {guild.guild.name}"
            await bot.rest.create_message(LOGCHANNEL,joinmsg)
            await bot.rest.create_message(PUBLICLOGCHANNEL,publicJoinMsg)
        except:
            logger.fatal('Excpetion occured when sending join msg to log server for guild Id: %s and server name: %s',guild.guild_id,guild.old_guild.name)
            pass
        
        
    except Exception as e:
        logger.critical('Error in guild join event for guild %s', guild.guild_id, exc_info=1)
        pass

#endregion guild join event



#region Guild leave event 
@bot.listen(hikari.GuildLeaveEvent)
async def guildLeave(guild: hikari.GuildLeaveEvent):
    try:
        logger.error('Guild leave event triggered for the guild: %s, guild name: %s', guild.guild_id, guild.old_guild.name)

        # with open('stories.json', 'r') as s, open('channels.json','r') as f:
        #     stories=json.load(s)
        #     channels=json.load(f)


        #async impl of reading from json files
        async with aiofiles.open("stories.json",mode="r") as s, aiofiles.open("channels.json",mode="r") as c, aiofiles.open("authors.json",mode="r") as a, aiofiles.open("messages.json", mode="r") as m:
            stories=await s.read()
            authors=await a.read()
            channels=await c.read()
            messages=await m.read()

        if guild.guild_id:
            if str(guild.guild_id) in channels:
                del channels[str(guild.guild_id)]

            if str(guild.guild_id) in stories:
                del stories[str(guild.guild_id)]
            
            if str(guild.guild_id) in authors:
                del authors[str(guild.guild_id)]

            if str(guild.guild_id) in messages:
                del messages[str(guild.guild_id)]


        #async impl of reading in to json files:
        async with aiofiles.open("stories.json",mode="w") as s, aiofiles.open("channels.json",mode="w") as c, aiofiles.open("authors.json",mode="w") as a, aiofiles.open("messages.json", mode="w") as m:
            await s.write(json.dumps(stories,indent=2))
            await a.write(json.dumps(authors,indent=2))
            await c.write(json.dumps(channels,indent=2))
            await m.write(json.dumps(messages,indent=2))

                

        # with open('stories.json', 'w') as s, open('channels.json','w') as f:
        #     json.dump(channels,f,indent=2)
        #     json.dump(stories,s,indent=2)

        # with open ('authors.json','r') as a:
        #     authors=json.load(a)

        # if guild.guild_id:
        #     if str(guild.guild_id) in authors:
        #         del authors[str(guild.guild_id)]

        # with open('authors.json','w') as a:
        #     json.dump(authors,a,indent=2)

        # with open("messages.json","r") as m:
        #     messages=json.load(m)

        # if guild.guild_id:
        #     if str(guild.guild_id) in messages:
        #         del messages[str(guild.guild_id)]

        # with open("messages.json","w") as m:
        #     json.dump(messages,m,indent=2)

        try:
            joinmsg=f'Bot left a server guild Id: {guild.guild_id} and server name: {guild.old_guild.name}'
            publicLeftMsg=f"Bot left server: {guild.old_guild.name}"
            await bot.rest.create_message(LOGCHANNEL,joinmsg)
            await bot.rest.create_message(PUBLICLOGCHANNEL,publicLeftMsg)
        except Exception as e:
            logger.fatal('Excpetion occured when sending leave msg to log server for guild: %s and server name: %s',guild.guild_id,guild.old_guild.name,exc_info=1)
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