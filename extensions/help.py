import hikari
import lightbulb
import json

plugin=lightbulb.Plugin('HelpPlugin')


# #error handler
# @plugin.listener(lightbulb.CommandErrorEvent)
# async def on_command_error(event):
#     await event.context.respond('OOPS!! Looks like something went wrong.') #need to check if this works

# #error handler


#custom help command end
@plugin.command
@lightbulb.option('category','Use channel for channel related help', str, choices=('channel','story'))
@lightbulb.command('help','Gives you commands list. Use empty or channel or story as categories')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    category=ctx.options.category
    category=category.strip()
    category=category.replace(' ','')
    with open('text.json','r') as f:
        text=json.load(f)

    if category.lower()=='channel':
        em=hikari.Embed(title='CHANNEL COMMANDS',  color=0Xff500a)
        em.add_field(name='addchannel', value=str(text['addchannel']), inline=False)
        em.add_field(name='removechannel',value=str(text['removechannel']), inline=False)
        em.add_field(name='getchannels',value=str(text['getchannels']),inline=False)
        await ctx.respond(embed=em)

    elif category.lower()=='story':
        em=hikari.Embed(title='STORY COMMANDS', color=0Xff500a)
        em.add_field(name='addstory', value=str(text['addstory']), inline=False)
        em.add_field(name='removestory',value=str(text['removestory']), inline=False)
        em.add_field(name='getstories',value=str(text['fetch']), inline=False)
        await ctx.respond(embed=em)
    
    else:
        em=hikari.Embed(title='HELP', color=0Xff500a)
        em.add_field(name='channel', value=str('channel'), inline=False)
        em.add_field(name='story',value=str('story'), inline=False)
        await ctx.respond(embed=em)


#custom help command end

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

