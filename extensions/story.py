try:
    import lightbulb
    import json
    import hikari
    import logging
    import wattpad as ws
    
except Exception as e:
    print(str(e))

plugin=lightbulb.Plugin('StoryPlugin')


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)


#add story start
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.owner_only)
@lightbulb.option('storyurl', 'Url of the story to be added')
@lightbulb.command('addstory','Adds your current story to receive new chapter noifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def addstory(ctx):
    try:
        logger.info('Add story command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.options.storyurl)
        with open('stories.json','r') as s:
            stories=json.load(s)

        domain='www.wattpad.com'
        if domain not in ctx.options.storyurl:
            logger.error('The provided URL is not wattpad URL %s', ctx.options.storyurl)
            msgstr=hikari.Embed(title=f'🛑 An error occurred with the `addstory` command.', color=0xFF0000)
            msgstr.add_field(name='Error:', value='The URL you used is not a valid wattpad URL. Try with a valid one.', inline=False)
            await ctx.respond(embed=msgstr)

        else:
            if ctx.options.storyurl!=None and (await ws.checkStory(ctx.options.storyurl)):
                if not stories:
                    stories[str(ctx.guild_id)]=[str(ctx.options.storyurl)]
                else:
                    if str(ctx.guild_id) not in stories:
                        stories[str(ctx.guild_id)]=[str(ctx.options.storyurl)]
                    else:
                        for guild in stories:
                            if guild==str(ctx.guild_id) and str(ctx.options.storyurl) not in stories[str(ctx.guild_id)]:
                                stories[str(ctx.guild_id)].append(str(ctx.options.storyurl))

                with open('stories.json','w') as s:
                    json.dump(stories,s,indent=2)

                
                embContent='You will receive new chapter notications from this story.'
                em=hikari.Embed(title='Story has been successfully added to this server\'s list.',description=embContent, color=0Xff500a)

                await ctx.respond(embed=em)


            else:
                ErrContent='Oops!! There is something wrong with your story link. Check the link and try again.'
                emErr=hikari.Embed(title=f'🛑 Error:',description=ErrContent, color=0xFF0000)
                
                await ctx.respond(embed=emErr)

    except Exception as e:
        logger.fatal('Exception has occured in Add story command for guild %s and story %s',ctx.guild_id,ctx.options.storyurl,exc_info=1)
        raise e

        

    
#remove story start
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.owner_only)
@lightbulb.option('storyurl','Url of the story to be removed')
@lightbulb.command('removestory','removes your current story from receiving new chapter notifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def removestory(ctx):
    try:
        logger.info('Remove story command has been triggered for guild %s and story %s',ctx.guild_id, ctx.options.storyurl)
        url=ctx.options.storyurl
        with open('stories.json','r') as f:
            stories=json.load(f)
        if ctx.channel_id is not None:
            for guild in stories:
                if guild==str(ctx.guild_id) and str(url) in stories[str(ctx.guild_id)]:
                    stories[str(ctx.guild_id)].remove(str(url))

        with open('stories.json','w') as f:
            json.dump(stories,f,indent=2)

        
        emContent='You will no loger receive new chapter notifications from this story.'
        em=hikari.Embed(title='This story has been removed.', description=emContent,color=0Xff500a)

        await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in remove story command for guild %s and story %s',ctx.guild_id,ctx.options.storyurl,exc_info=1)
        raise e



#remove story end


#get stories start
@plugin.command
@lightbulb.command('getstories','fetch your server\'s stories that are getting new chapter updates')
@lightbulb.implements(lightbulb.SlashCommand)
async def getstories(ctx):
    try:
        logger.info('get channels has been triggered for guild %s and channel %s',ctx.guild_id, ctx.channel_id)
        with open('stories.json') as f:
            stories=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            for guild in stories:
                if guild==str(ctx.guild_id):
                    for key in stories[guild]:
                        msg=f'{str(msg)} {str(key)}\n'
        if not msg:
            msg='No stories were added to your list.'
            em=hikari.Embed(title='So empty!!',description=msg, color=0Xff500a)
            
        else:
            msg=f'{msg}'
            em=hikari.Embed(title='Your server\'s stories:', description=msg, color=0Xff500a)
            

        await ctx.respond(embed=em)
    
    except Exception as e:
        logger.fatal('Exception in getchannels command for guild %s',ctx.guild_id, exc_info=1)
        raise e

#get stories end


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

