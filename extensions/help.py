import hikari
import lightbulb
import json
import logging

plugin=lightbulb.Plugin('HelpPlugin')

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

#custom help command start
@plugin.command
@lightbulb.option('category','Use channel for channel related help or story for story related help', str, choices=('channel','story'), required=False)
@lightbulb.command('help','Gives you list of commands. Use empty or channel or story as categories')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    try:
        logger.info('help command has been triggered in guild %s', ctx.guild_id)
        with open('text.json','r') as f:
                text=json.load(f)

        if ctx.options.category is not None:
            logger.info('Non empty help is triggered')
            category=ctx.options.category
            category=category.strip()
            category=category.replace(' ','')
            

            if category.lower()=='channel':
                logger.info('channel help is trigered')
                em=hikari.Embed(title='CHANNEL COMMANDS',  color=0Xff500a)
                em.add_field(name='addchannel', value=str(text['addchannel']), inline=False)
                em.add_field(name='removechannel',value=str(text['removechannel']), inline=False)
                em.add_field(name='getchannels',value=str(text['getchannels']),inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=='story':
                logger.info('story help is trigered')
                em=hikari.Embed(title='STORY COMMANDS', color=0Xff500a)
                em.add_field(name='addstory', value=str(text['addstory']), inline=False)
                em.add_field(name='removestory',value=str(text['removestory']), inline=False)
                em.add_field(name='getstories',value=str(text['fetch']), inline=False)
                await ctx.respond(embed=em)
            
            else:
                logger.info('Empty help is trigered')
                em=hikari.Embed(title='HELP COMMANDS', color=0Xff500a)
                em.add_field(name='channel', value=str(text['channel']), inline=False)
                em.add_field(name='story',value=str(text['story']), inline=False)
                await ctx.respond(embed=em)
        else:
            logger.info('Empty help is trigered')
            em=hikari.Embed(title='HELP COMMANDS', color=0Xff500a)
            em.add_field(name='channel', value=str(text['channel']), inline=False)
            em.add_field(name='story',value=str(text['story']), inline=False)
            await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in help commands for guild %s',ctx.guild_id, exc_info=1)
        raise e


#custom help command end

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

