import hikari
import lightbulb
import json
import logging
import helpers.json_helper as jhelper

plugin=lightbulb.Plugin('HelpPlugin')

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="help")
logger.setLevel(logging.ERROR)

#custom help command start
@plugin.command
@lightbulb.option('category','Use channel/story/custom message/author/custom channel/setup/about for detailed help on categories', str, choices=('channel','story','author','custom message','custom channel','setup','about'), required=False)
@lightbulb.command('help','Gives you help on commands. Use empty/channel/story/author/setup/about as categories')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    try:
        logger.info('help command has been triggered in guild %s', ctx.guild_id)

        # with open('text.json','r') as f:
        #         text=json.load(f)

         #async impl of reading from json file:
        text=await jhelper.read_from_json("text.json")

        if ctx.options.category is not None:
            logger.info('Non empty help is triggered')
            category=ctx.options.category
            category=category.strip()
            category=category.replace(' ','')
            

            if category.lower()=='channel':
                logger.info('channel help is trigered')
                em=hikari.Embed(title='CHANNEL COMMANDS',  color=0Xff500a)
                em.add_field(name='setchannel', value=f'{text["setchannel"]}{text["setchannelex"]}', inline=False)
                em.add_field(name='unsetchannel',value=f'{text["unsetchannel"]}{text["unsetchannelex"]}', inline=False)
                em.add_field(name='checkchannels',value=f'{text["checkchannels"]}{text["checkchannelsex"]}',inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=='story':
                logger.info('story help is trigered')
                em=hikari.Embed(title='STORY COMMANDS', color=0Xff500a)
                em.add_field(name='followstory', value=f"{text['followstory']}{text['followstoryex']}", inline=False)
                em.add_field(name='unfollowstory',value=f"{text['unfollowstory']}{text['unfollowstoryex']}", inline=False)
                em.add_field(name='checkstories',value=f"{text['checkstories']}{text['checkstoriesex']}", inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=='author':
                logger.info('author help is trigered')
                em=hikari.Embed(title='AUTHOR COMMANDS', color=0Xff500a)
                em.add_field(name='followauthor', value=f"{text['followauthor']}{text['followauthorex']}", inline=False)
                em.add_field(name='unfollowauthor',value=f"{text['unfollowauthor']}{text['unfollowauthorex']}", inline=False)
                em.add_field(name='checkauthors',value=f"{text['checkauthors']}{text['checkauthorsex']}", inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=='custommessage':
                logger.info("custom message help is triggered")
                em=hikari.Embed(title="CUSTOM MESSAGE COMMANDS",color=0Xff500a)
                em.add_field(name="setcustommessage", value=f"{text['setcustommsg']}{text['setcustommsgex']}",inline=False)
                em.add_field(name="unsetcustommessage",value=f"{text['removecustommsg']}{text['removecustommsgex']}",inline=False)
                em.add_field(name="checkcustommsg",value=f"{text['checkcustommsg']}{text['checkcustommsgex']}")
                await ctx.respond(embed=em)

            elif category.lower()=='setup':
                logger.info('setup help is trigered')
                em=hikari.Embed(title='How to setup?', color=0Xff500a)
                em.add_field(name='setchannel', value=f"{text['setup']}{text['setupex']}", inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=='about':
                logger.info('setup help is trigered')
                em=hikari.Embed(title='What can this Bot do?', color=0Xff500a)
                em.add_field(name='About', value=str(text['about']), inline=False)
                em.add_field(name='Help Server', value=str(text['helpserver']),inline=False)
                await ctx.respond(embed=em)

            elif category.lower()=="customchannel":
                logger.info("custom channel help is invoked")
                em=hikari.Embed(title="CUSTOM CHANNEL COMMANDS", color=0Xff500a)
                em.add_field(name="set-custom-channel", value=f"{text['setcustomchannel']}{text['setcustomchannelex']}",inline=False)
                em.add_field(name="unset-custom-channel", value=f"{text['unsetcustomchannel']}{text['unsetcustomchannelex']}",inline=False)
                em.add_field(name="check-custom-channels",value=f"{text['checkcustomchannels']}{text['checkcustomchannelsex']}",inline=False)
                await ctx.respond(embed=em)

            
            
            else:
                logger.info('Empty help is trigered')
                em=hikari.Embed(title='GENERAL HELP', description='You can use `/help <category>` to get help about specific category with more details. Use channel/story/author/custom message/setup/about as categories.', color=0Xff500a)
                em.add_field(name='NOTE:', value=str(text['Note']), inline=False)
                em.add_field(name='SETUP',value=str(text['setup']), inline=False)
                em.add_field(name='CHANNEL RELATED COMMANDS:',value=f"Commands: `/setchannel`\n`/unsetchannel`\n`checkchannels`\nUse `/help channels` command to see detailed info on channel related commands.", inline=False)
                em.add_field(name='STORY RELATED COMMANDS:',value=f"Commands: `/followstory`\n`/unfollowstory`\n`checkstories`\nUse `/help story` command to see detailed info on story related commands.", inline=False)
                em.add_field(name='AUTHOR RELATED COMMANDS:',value=f"Commands: `/followauthor`\n`/unfollowauthor`\n`/checkauthors`\nuse `/help author` to see detailed info on author related commands.", inline=False)
                em.add_field(name="CUSTOM MESSAGE RELATED COMMANDS:",value=f"Commands: `/setcustommessage`\n`/unsetcustommessage`\n`/checkcustommsg`\nUse `help custom message` command to see info on custom message related commands.",inline=False)
                em.add_field(name="CUSTOM CHANNEL RELATED COMMANDS:",value=f"`/set-custom-channel`\n`/unset-custom-channel`\n`/check-custom-channels`\nUse `/help custom channels` command to see detailed info on custom channels related commands.")
                em.add_field(name='Help Server', value=str(text['helpserver']), inline=False)
                await ctx.respond(embed=em)
        else:
            logger.info('Empty help is trigered')
            em=hikari.Embed(title='GENERAL HELP', description='You can use `/help <category>` to get help about specific category with more details. Use channel/story/author/custom message/setup/about as categories.', color=0Xff500a)
            em.add_field(name='NOTE:', value=str(text['Note']), inline=False)
            em.add_field(name='SETUP',value=str(text['setup']), inline=False)
            em.add_field(name='CHANNEL RELATED COMMANDS:',value=f"Commands: `/setchannel`\n`/unsetchannel`\n`checkchannels`\nUse `/help channels` command to see detailed info on channel related commands.", inline=False)
            em.add_field(name='STORY RELATED COMMANDS:',value=f"Commands: `/followstory`\n`/unfollowstory`\n`checkstories`\nUse `/help story` command to see detailed info on story related commands.", inline=False)
            em.add_field(name='AUTHOR RELATED COMMANDS:',value=f"Commands: `/followauthor`\n`/unfollowauthor`\n`/checkauthors`\nuse `/help author` to see detailed info on author related commands.", inline=False)
            em.add_field(name="CUSTOM MESSAGE RELATED COMMANDS:",value=f"Commands: `/setcustommessage`\n`/unsetcustommessage`\n`/checkcustommsg`\nUse `help custom message` command to see info on custom message related commands.",inline=False)
            em.add_field(name="CUSTOM CHANNEL RELATED COMMANDS:",value=f"`/set-custom-channel`\n`/unset-custom-channel`\n`/check-custom-channels`\nUse `/help custom channels` command to see detailed info on custom channels related commands.")
            em.add_field(name='Help Server', value=str(text['helpserver']), inline=False)
            await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in help commands for guild %s',ctx.guild_id, exc_info=1)
        raise e


#custom help command end

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

