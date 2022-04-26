import hikari
import lightbulb
import json
import logging
import wattpad as ws
from datetime import datetime
from helpers.wattpad_helper import get_actual_author_url

plugin=lightbulb.Plugin('AuthorPlugin')


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)

#region follow author
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option('authorprofileurl', 'Url of the Author\'s profile you want to follow')
@lightbulb.command('followauthor','Follow an author to receive new announcements from the author')
@lightbulb.implements(lightbulb.SlashCommand)
async def followauthor(ctx:lightbulb.SlashContext):
    try:
        enteredURL=ctx.options.authorprofileurl
        logger.info('Follow author command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.options.authorprofileurl)

        #check if the profile URL contains any UTM tags and if yes, get a normal url withput utm tags
        profileUrl=""
        try:
            if "utm" in enteredURL:
                profileUrl=await get_actual_author_url(enteredURL)

        except Exception as e:
            logger.fatal("Exception occured in author.followauthor method while fetching actual author url for entered author url: %s, guild: %s",enteredURL,ctx.guild_id,exc_info=1)
            pass

        if not profileUrl:
            profileUrl=enteredURL


        with open('authors.json','r') as s:
            authors=json.load(s)

        domain='www.wattpad.com'
        if domain not in profileUrl:
            logger.error('The provided URL is not wattpad URL %s', profileUrl)
            msgstr=hikari.Embed(title=f'🛑 An error occurred with the `followauthor` command.', color=0xFF0000)
            msgstr.add_field(name='Error:', value='The URL you used is not a valid wattpad URL. Try with a valid one.', inline=False)
            await ctx.respond(embed=msgstr)

        else:
            if profileUrl!=None and (await ws.checkProfile(profileUrl)):
                author_name=profileUrl.split('/user/')[1].replace('-',' ')
                embContent=f'New announcements from {author_name} will be shared in this server.'
                msg=f'You have succesfully followed {author_name}'
                if not authors:
                    authors[str(ctx.guild_id)]=[{"url":f'{str(profileUrl)}',"lastupdated":f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}]
                else:
                    if str(ctx.guild_id) not in authors:
                        authors[str(ctx.guild_id)]=[{"url":f'{str(profileUrl)}',"lastupdated":f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}]
                    else:
                        for guild, author in authors.items():
                            if guild==str(ctx.guild_id):
                                if author:
                                    if any(str(profileUrl)==sty['url'] for  sty in author):
                                        msg=f'You\'re already following {author_name}'
                                        embContent=f'No need to follow the same author twice!!'
                                    else:
                                        author.append({"url": f'{profileUrl}',"lastupdated": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}' })
                                    
                                else:
                                    author.append({"url": f'{profileUrl}',"lastupdated": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}' })
       

                with open('authors.json','w') as s:
                    json.dump(authors,s,indent=2)

                em=hikari.Embed(title=msg,description=embContent, color=0Xff500a)

                await ctx.respond(embed=em)


            else:
                ErrContent='Oops!! There is something wrong with your author profile link. Check the link and try again.'
                emErr=hikari.Embed(title=f'🛑 Error:',description=ErrContent, color=0xFF0000)
                
                await ctx.respond(embed=emErr)

    except Exception as e:
        logger.fatal('Exception has occured in follow author command for guild %s and author %s',ctx.guild_id,profileUrl,exc_info=1)
        raise e

#endregion follow author

#region unfollow author
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option('authorprofileurl', 'Url of the Author\'s profile you want to unfollow')
@lightbulb.command('unfollowauthor','Unfollow an author to stop receing new announcements from this author.')
@lightbulb.implements(lightbulb.SlashCommand)
async def unfollowauthor(ctx:lightbulb.SlashContext):
    try:
        logger.info('Unfollow author method triggered for guild: %s and author: %s',ctx.guild_id,ctx.options.authorprofileurl)
        authorprofile=ctx.options.authorprofileurl
        author_name=authorprofile.split('/user/')[1].replace('-',' ')
        emContent=f'New announcements from {author_name} will not be shared in this server'
        emTitle=f'You have succesfully unfollowed {author_name}'
        with open('authors.json','r') as f:
            authors=json.load(f)
        if ctx.channel_id is not None:
            for guild,author in authors.items():
                if guild==str(ctx.guild_id):
                    if any(str(authorprofile)==auth['url'] for auth in author):
                        for auth in author:
                            if auth['url']==str(authorprofile):
                                author.remove(auth)
                    else:
                        emContent=f'Check if you wanted to unfollw a different author!'
                        emTitle=f'You\'re not following {author_name} from the beginning.'
                        
                        
                    
        with open('authors.json','w') as f:
            json.dump(authors,f,indent=2)

        
        
        em=hikari.Embed(title=emTitle, description=emContent,color=0Xff500a)

        await ctx.respond(embed=em)

    except Exception as e:
        logger.critical('Exception occured in Unfollowauthor command for guild %s and author %s',ctx.guild_id,ctx.options.authorprofileurl)

#endregion unfollow author


#region get authors
@plugin.command
@lightbulb.command('checkauthors','Check the author\'s you\'re following in this server')
@lightbulb.implements(lightbulb.SlashCommand)
async def getauthors(ctx:lightbulb.SlashContext):
    try:
        logger.info('getauthors command triggered for guild: %s',ctx.guild_id)
        with open('authors.json') as f:
            authors=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            for guild, author in authors.items():
                if guild==str(ctx.guild_id):
                    for auth in author:
                        key=auth['url']
                        msg=f'{str(msg)} {str(key)}\n'

        if not msg:
            msg='You\'re not following any authors in this server.'
            em=hikari.Embed(title='So empty!!',description=msg, color=0Xff500a)
            
        else:
            msg=f'{msg}'
            em=hikari.Embed(title='Author\'s you\'re following:', description=msg, color=0Xff500a)
            

        await ctx.respond(embed=em)
    
    except Exception as e:
        logger.critical('Exception occured in author.py getauthors commands for guild: %s',ctx.guild_id)

#endregion get authors


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
