from datetime import datetime

try:
    import lightbulb
    import json
    import hikari
    import logging
    import wattpad as ws
    from helpers.wattpad_helper import get_storyurl_from_chapter,get_storyurl_without_utm
    import helpers.json_helper as jhelper
except Exception as e:
    print(str(e))

plugin=lightbulb.Plugin('StoryPlugin')


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="story")
logger.setLevel(logging.ERROR)

#region follow story
#add a new story
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option('storyurl', 'Url of the story you want to follow')
@lightbulb.command('followstory','Follow a story to receive new chapter noifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def addstory(ctx:lightbulb.SlashContext):
    try:
        logger.info('Follow story command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.options.storyurl)

        enteredStoryURL=ctx.options.storyurl

        #check if the entered URL belongs to a individual chapter, if yes try to fetch story URL from that
        storyURL=""
        if "story" not in enteredStoryURL:
            try:
                storyURL=await get_storyurl_from_chapter(enteredStoryURL)

            except Exception as e:
                logger.fatal("Exception occured in story.followstory method while fetching story url for chapter URL: %s and guild: %s",enteredStoryURL,ctx.guild_id,exc_info=1)
                pass
        
        elif "utm" in enteredStoryURL:
            try:
                storyURL=await get_storyurl_without_utm(enteredStoryURL)

            except Exception as e:
                logger.fatal("Exception occured in story.followstory method while fetching story url without utm tags: %s and guild: %s",enteredStoryURL,ctx.guild_id,exc_info=1)
                pass

        if not storyURL:
            storyURL=enteredStoryURL


        # with open('stories.json','r') as s:
        #     stories=json.load(s)

        #async impl of reading from json file:
        stories=jhelper.read_from_json("stories.json")

        domain='www.wattpad.com'
        if domain not in storyURL:
            logger.error('The provided URL is not wattpad URL %s', storyURL)
            msgstr=hikari.Embed(title=f'🛑 An error occurred with the `addstory` command.', color=0xFF0000)
            msgstr.add_field(name='Error:', value='The URL you used is not a valid wattpad URL. Try with a valid one.', inline=False)
            await ctx.respond(embed=msgstr)

        else:
            if storyURL!=None and (await ws.checkStory(storyURL)):
                embContent='New chapter links from this story will be shared in this server.'
                em=hikari.Embed(title='You have succesfully followed this story.',description=embContent, color=0Xff500a)
                if not stories:
                    #stories[str(ctx.guild_id)]=[str(ctx.options.storyurl)]
                    stories[str(ctx.guild_id)]=[{"url":f'{str(storyURL)}',"lastupdated":f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}]
                else:
                    if str(ctx.guild_id) not in stories:
                        #stories[str(ctx.guild_id)]=[str(ctx.options.storyurl)]
                        stories[str(ctx.guild_id)]=[{"url":f'{str(storyURL)}',"lastupdated":f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}]
                    else:
                        for guild, story in stories.items():
                            if guild==str(ctx.guild_id):
                                if any(str(storyURL)==sty['url'] for  sty in story):
                                    embContent='No need to follow the same story twice.'
                                    em=hikari.Embed(title='You\'re already following this story.',description=embContent, color=0Xff500a)
                                else:
                                    story.append({"url": f'{storyURL}',"lastupdated": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}' })
                        

                # with open('stories.json','w') as s:
                #     json.dump(stories,s,indent=2)

                #async impl of writing to json files:
                result=await jhelper.write_to_json("stories.json",stories)

                await ctx.respond(embed=em)


            else:
                ErrContent='Oops!! There is something wrong with your story link. Check the link and try again.'
                emErr=hikari.Embed(title=f'🛑 Error:',description=ErrContent, color=0xFF0000)
                
                await ctx.respond(embed=emErr)

    except Exception as e:
        logger.fatal('Exception has occured in Follow story command for guild %s and story %s',ctx.guild_id,ctx.options.storyurl,exc_info=1)
        raise e

#endregion follow story      

#region unfollow story   
#remove story start
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option('storyurl','Url of the story you want to unfollow')
@lightbulb.command('unfollowstory','unfollow a story to stop receiving new chapter updates.')
@lightbulb.implements(lightbulb.SlashCommand)
async def removestory(ctx):
    try:
        logger.info('Unfollow story command has been triggered for guild %s and story %s',ctx.guild_id, ctx.options.storyurl)
        url=ctx.options.storyurl

        emContent='New chapter links from this story will no longer be posted in this  server.'
        em=hikari.Embed(title='You have succesfully unfollowed this story.', description=emContent,color=0Xff500a)

        # with open('stories.json','r') as f:
        #     stories=json.load(f)

        #async impl of reading from json file:
        stories=jhelper.read_from_json("stories.json")


        if ctx.channel_id is not None:
            for guild,story in stories.items():
                if guild==str(ctx.guild_id):
                    if any(str(url)==sty['url'] for sty in story ):
                        for sty in story:
                            if sty['url']==str(url):
                                story.remove(sty)

                    else:
                        em=hikari.Embed(title='You\'re not following this story from the beginning.',color=0Xff500a)
                        
                    
        # with open('stories.json','w') as f:
        #     json.dump(stories,f,indent=2)

        #async impl of writing to json files:
        result=await jhelper.write_to_json("stories.json",stories)

        await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in Unfollow story command for guild %s and story %s',ctx.guild_id,ctx.options.storyurl,exc_info=1)
        raise e

#endregion unfollow story


#region get stories
#get stories of a server
@plugin.command
@lightbulb.command('checkstories','check the stories that you are already following in this server')
@lightbulb.implements(lightbulb.SlashCommand)
async def getstories(ctx):
    try:
        logger.info('get stories has been triggered for guild %s and channel %s',ctx.guild_id, ctx.channel_id)

        # with open('stories.json') as f:
        #     stories=json.load(f)

        #async impl of reading from json file:
        stories=jhelper.read_from_json("stories.json")


        msg=''
        if ctx.guild_id is not None:
            for guild, story in stories.items():
                if guild==str(ctx.guild_id):
                    for sty in story:
                        key=sty['url']
                        msg=f'{str(msg)} {str(key)}\n'

        if not msg:
            msg='You\'re not following any stories in this server right now. Use `/folowstory` command to follow a new story.'
            em=hikari.Embed(title='So empty!!',description=msg, color=0Xff500a)
            
        else:
            msg=f'{msg}'
            em=hikari.Embed(title='Stories you\'re following in this server:', description=msg, color=0Xff500a)
            

        await ctx.respond(embed=em)
    
    except Exception as e:
        logger.fatal('Exception in get stories command for guild %s',ctx.guild_id, exc_info=1)
        raise e


#endregion get stories


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

