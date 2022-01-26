import hikari
import lightbulb
import json
from lightbulb.ext import tasks
import wattpad as ws


bot=lightbulb.BotApp(token='OTI5Mzg0MzM5ODQwNTg1Nzk5.YdminQ.zUwPrYfycq0SQtVQefRUIjUM7LQ', default_enabled_guilds=(906917949888147477, 931555271447293962))
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
            newchapter=ws.get_chapter(str(key))
            if newchapter:
                for ch in channels[story]:
                    for nc in newchapter:
                        await bot.rest.create_message(ch, str(nc))



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
    if any(role.permissions.all(hikari.Permissions.ADMINISTRATOR or hikari.Permissions.MODERATE_MEMBERS) for role in roles):
        return True

    return False

#permissions


@bot.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('ping','gives latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    try:
        check=bot.cache.get_guild_channel(906917970620592178).name
        await ctx.respond('pong')
    except Exception as e:
        print(e)


#get channels start
@bot.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('getchannels','Gives a list of your current channels')
@lightbulb.implements(lightbulb.SlashCommand)
async def getchannels(ctx):
        with open('channels.json') as f:
            channels=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            for channel in channels:
                if channel==str(ctx.guild_id):
                    for key in channels[channel]:
                        msg=str(msg)+'#'+str(bot.cache.get_guild_channel(int(key)).name)+'\n'
        if not msg:
            msg='No channels were added to your list.'
        else:
            msg='Your channels list:\n'+msg

        await ctx.respond(msg)


#get channels end


# #custom help command start
# @bot.command
# @lightbulb.option('category','Use channel for channel related help', str, choices=('channel','story'))
# @lightbulb.command('help','Gives you commands list. Use empty or channel or story as categories')
# @lightbulb.implements(lightbulb.SlashCommand)
# async def help(ctx):
#     category=ctx.options.category
#     category=category.strip()
#     category=category.replace(' ','')
#     with open('text.json','r') as f:
#         text=json.load(f)

#     if category.lower()=='channel':
#         em=hikari.Embed(title='CHANNEL COMMANDS')
#         em.add_field(name='addchannel', value=str(text['addchannel']), inline=False)
#         em.add_field(name='removechannel',value=str(text['removechannel']), inline=False)
#         em.add_field(name='getchannels',value=str(text['getchannels']),inline=False)
#         await ctx.respond(embed=em)

#     elif category.lower()=='story':
#         em=hikari.Embed(title='STORY COMMANDS')
#         em.add_field(name='addstory', value=str(text['addstory']), inline=False)
#         em.add_field(name='removestory',value=str(text['removestory']), inline=False)
#         em.add_field(name='getstories',value=str(text['fetch']), inline=False)
#         await ctx.respond(embed=em)
    
#     else:
#         em=hikari.Embed(title='HELP')
#         em.add_field(name='channel', value=str('channel'), inline=False)
#         em.add_field(name='story',value=str('story'), inline=False)
#         await ctx.respond(embed=em)


# #custom help command end



bot.run()