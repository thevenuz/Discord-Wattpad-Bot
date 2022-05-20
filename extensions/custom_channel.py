import hikari
import lightbulb
import logging
import json
import helpers.json_helper as jhelper

plugin=lightbulb.Plugin("CustomchannelPlugin")

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="customchannel")
logger.setLevel(logging.ERROR)


msgs={
    "NotFollowingAuthor":"You're not following this author currently. Use `/followauthor` to follow a new author or `/checkauthors` to check the authors you're already following.",
    "NotFollowingStory":"You're not following this story currently. use `/followstory` to follow a new story or `/checkstories` to check the stories you're already following",
    "NotFollowingAnyAuthors":"You're not following any authors in this server. Try `/checkauthors` to see the author's you're following and `/followauthor` to follow a new author",
    "NotFollowingAnyStories":"You're not following any stories in this servers. Try `/checkstories` to see the stories you're following and `/followstory` to follow a new story.",
    "NotsetChannelAuthor":"channel has not been set as a custom channel for the updates from this author. Try `/check-custom-channels` to see which channles have been set for which stories/Announcements.",
    "NotsetChannelStory":"channel has not been set as a custom channel for the updates from this story. Try `/check-custom-channels` to see which channles have been set for which stories/Announcements.",
    "NoStoryFound":"No story with the title {url} has been matched with the stories you're already following. Try using the full URL of the story instead of the title",
    "NoAuthorFound":"No Author with the name {url} has been matched with the Authrors you're already following. Try using the full URL of the Author's profile.",
    "domain":"wattpad.com"
}

@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the Story title/Author name or full URL of the story or author's profile.",required=True)
@lightbulb.option("category","whether your custom channel is for story or announcement updates",str,choices=("story","announcement"),required=True)
@lightbulb.option('channel','Mention the channels which you want as a custom channel for updates.',
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("set-custom-channel","set a custom channel for bot to send updates for particular stories/announcements")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_custom_channel(ctx:lightbulb.SlashContext):
    try:
        logger.info("custom_channel.set_custom_channel method invoked for category %s, channel %s, story/author: %s",ctx.options.category,ctx.options.channel,ctx.options.url)

        category=ctx.options.category
        url=ctx.options.url
        channel=ctx.options.channel
        guild=str(ctx.guild_id)

        isAuthor=False
        isStory=False
        found=False

        channel_id=channel.id

        if category.lower()=="announcement":
            ##load authors.json
            records=await jhelper.read_from_json("authors.json")
            isAuthor=True
            not_follow_msg=msgs["NotFollowingAnyAuthors"]
            not_follow_any=msgs["NotFollowingAnyAuthors"]
            no_record_found=msgs["NoAuthorFound"]
            

        elif category.lower()=="story":
            records=await jhelper.read_from_json("stories.json")
            isStory=True
            not_follow_msg=msgs["NotFollowingAnyStories"]
            not_follow_any=msgs["NotFollowingAnyStories"]
            no_record_found=msgs["NoStoryFound"]

        else:
            logger.fatal("category is not story or announcement for guild: %s, category:%s, url: %s",guild,category,url)
            await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description="Uh-oh!! The developer has messed up somewhere. Try again or contact the dev." ))

        ##get the full URL if input is just title
        if msgs["domain"] not in url:
            found, count, full_url=await get_full_url(url,guild,channel_id, records)
            if found and count==1:
                url=full_url
            else:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"You're following multiple {'Stories' if isStory else 'Authors'} that has {url} in it. Please use the full url of the {'Story' if isStory else 'Author Profile'}."))
                found=False
        else:
            found=True


        if records and found:
            if guild not in records:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"{not_follow_any}"))
            else:
                for guild_id, items in records.items():
                    if guild_id==guild:
                        if not any(str(url)==itm['url'] for  itm in items):
                            await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"{not_follow_msg}"))

                        else:
                            for item in items:
                                if url==item["url"]:
                                    
                                    item["CustomChannel"]=str(channel_id)

                                    if isAuthor:
                                        update_authors=await jhelper.write_to_json("authors.json",records)
                                        response_msg=f"All the updates from the author: {url} will be sent in channel <#{channel_id}>"
                                    elif isStory:
                                        update_authors=await jhelper.write_to_json("stories.json",records)
                                        response_msg=f"All the updates from the story: {url} will be sent in channel <#{channel_id}>"

                                    if update_authors:
                                        em=hikari.Embed(title="Success!!",description=response_msg,color=0Xff500a)
                                        
                                        await ctx.respond(embed=em)

                                    else:
                                        emContent='Uh-oh, something is not right. Please check `/check-custom-channels` to see if the custom channel has been setup properly.'
                                        emErr=hikari.Embed(title=f'🛑 Error:',description=f'{emContent}',color=0xFF0000)
                                        await ctx.respond(embed=emErr) 
                                                                    
        elif not found:
            if isAuthor:
                no_record_found=f"No story with the title {url} has been matched with the stories you're already following. Try using the full URL of the story instead of the title"
            else:
                no_record_found=f"No Author with the name {url} has been matched with the Authrors you're already following. Try using the full URL of the Author's profile."
            await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"{no_record_found}"))




    except Exception as e:
        logger.fatal("Exception occured in custom_channel.set_custom_channel method for category %s, channel %s, story/author: %s",ctx.options.category,ctx.options.channel,exc_info=1)
        raise e



@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the Story title/Author name or full URL of the story or author's profile.",required=True)
@lightbulb.option("category","whether your custom channel is for story or announcement updates",str,choices=("story","announcement"),required=True)
@lightbulb.option('channel','Mention the channels which you want to remove.',
required=True,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command("unset-custom-channel","unset the custom channel you've already setup for stories/announcements")
@lightbulb.implements(lightbulb.SlashCommand)
async def unset_custom_channel(ctx:lightbulb.SlashContext):
    try:
        logger.info("custom_channel.unset_custom_channel triggered for server: %s,category: %s, url: %s",ctx.guild_id,ctx.options.category,ctx.options.url)

        category=ctx.options.category
        url=str(ctx.options.url)
        channel=ctx.options.channel
        guild=str(ctx.guild_id)

        isAuthor=False
        isStory=False
        found=False

        channel_id=str(channel.id)

        if category.lower()=="announcement":
            ##load authors.json
            records=await jhelper.read_from_json("authors.json")
            isAuthor=True
            not_follow_msg=msgs["NotFollowingAnyAuthors"]
            not_follow_any=msgs["NotFollowingAnyAuthors"]
            no_record_found=msgs["NoAuthorFound"]
            not_set_channel=msgs["NotsetChannelAuthor"]
            

        elif category.lower()=="story":
            records=await jhelper.read_from_json("stories.json")
            isStory=True
            not_follow_msg=msgs["NotFollowingAnyStories"]
            not_follow_any=msgs["NotFollowingAnyStories"]
            no_record_found=msgs["NoStoryFound"]
            not_set_channel=msgs["NotsetChannelStory"]

        else:
            logger.fatal("category is not story or announcement for guild: %s, category:%s, url: %s",guild,category,url)
            await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description="Uh-oh!! The developer has messed up somewhere. Try again or contact the dev." ))
        
        ##get the full URL if input is just title
        if msgs["domain"] not in url:
            found, count, full_url=await get_full_url(url,guild,channel_id, records, True)
            if found and count==1:
                url=full_url
            elif count>1:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"You're following multiple {'Stories' if isStory else 'Authors'} that has {url} in it. Please use the full url of the {'Story' if isStory else 'Author Profile'}."))
                found=False
        else:
            found=True

        if records and found:
            if guild not in records:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"{not_follow_any}"))
            else:
                for guild_id, items in records.items():
                    if guild_id==guild:
                        if not any(str(url)==itm['url'] for  itm in items):
                            await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"{not_follow_msg}"))

                        elif not any(str(channel_id)==itm["CustomChannel"] for itm in items):
                            await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"<#{channel_id}> {not_set_channel}"))

                        else:
                            for item in items:
                                if item["url"]==url and item["CustomChannel"]==channel_id:
                                    item["CustomChannel"]=""

                                    if isAuthor:
                                        update_authors=await jhelper.write_to_json("authors.json",records)
                                        response_msg=f"<#{channel_id}> has been succesfully unset as custom channel for updates from Author: {url}. Updates from this Author will still be shared in common channel that's been setup for updates."
                                    elif isStory:
                                        update_authors=await jhelper.write_to_json("stories.json",records)
                                        response_msg=f"<#{channel_id}> has been succesfully unset as custom channel for updates from Story: {url}. Updates from this Story will still be shared in common channel that's been setup for updates."

                                    if update_authors:
                                        em=hikari.Embed(title="Success!!",description=response_msg,color=0Xff500a)
                                        
                                        await ctx.respond(embed=em)

                                    else:
                                        emContent='Uh-oh, something is not right. Please check `/check-custom-channels` to see if the custom channel has been unset properly.'
                                        emErr=hikari.Embed(title=f'🛑 Error:',description=f'{emContent}',color=0xFF0000)
                                        await ctx.respond(embed=emErr) 


        elif not found and count<1:
            if isAuthor:
                no_record_found=f"No story with the title {url} has been matched with the stories you're already following. Try using the full URL of the story instead of the title"
            else:
                no_record_found=f"No Author with the name {url} has been matched with the Authrors you're already following. Try using the full URL of the Author's profile."
            await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"{no_record_found}"))



    except Exception as e:
        logger.fatal("Exception occured in custom_channel.unset_custom_channel for server: %s,category: %s, url: %s",ctx.guild_id,ctx.options.category,ctx.options.url,exc_info=1)
        raise e



@plugin.command()
@lightbulb.option("category","whether your custom channel is for story or announcement updates",str,choices=("story","announcement"),required=True)
@lightbulb.command("check-custom-channels","unset the custom channel you've already setup for stories/announcements")
@lightbulb.implements(lightbulb.SlashCommand)
async def check_custom_channels(ctx:lightbulb.SlashContext):
    try:
        logger.info("custom_channel.check_custom_channels triggered for server: %s, category:%s",ctx.guild_id,ctx.options.category)

        category=ctx.options.category
        guild=str(ctx.guild_id)

        result_list=""

        if category.lower()=="announcement":
            ##load authors.json
            records=await jhelper.read_from_json("authors.json")
            isAuthor=True
            not_follow_msg=msgs["NotFollowingAnyAuthors"]
            not_follow_any=msgs["NotFollowingAnyAuthors"]
            

        elif category.lower()=="story":
            records=await jhelper.read_from_json("stories.json")
            isStory=True
            not_follow_msg=msgs["NotFollowingAnyStories"]
            not_follow_any=msgs["NotFollowingAnyStories"]

        else:
            logger.fatal("category is not story or announcement for guild: %s, category:%s",guild,category)
            await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description="Uh-oh!! The developer has messed up somewhere. Try again or contact the dev." ))

        if records:
            if guild not in records:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:",description=f"{not_follow_any}"))
            else:
                for guild_id, items in records.items():
                    items=sorted(items,key=lambda i: i["CustomChannel"])
                    if guild_id==guild:
                        for item in items:
                            if item["CustomChannel"]:
                                list_url=item["url"]
                                list_channel=item["CustomChannel"]
                                if list_channel in result_list:
                                    result_list=f"{str(result_list)} {list_url}\n"
                                else:
                                    result_list=f"{str(result_list)}<#{list_channel}> :\n {list_url}\n"
        
                if result_list:
                    await ctx.respond(embed=hikari.Embed(title=f"Your Custom Channels for {'Announcements' if isAuthor else 'Stories'}:",description=f"{result_list}"))

                else:
                    await ctx.respond(embed=hikari.Embed(title=f"So Empty!!", description="Looks like you haven't setup any custom channels yet."))





    except Exception as e:
        logger.fatal("Exception occured in custom_channel.check_custom_channels for server: %s, category:%s",ctx.guild_id,ctx.options.category)
        raise e




async def get_full_url(title:str,guild:str,channel:str,data:dict,unset=False):
    try:
        logger.info("custom_channel.get_full_url triggered for title:%s",title)

        if guild in data:
            for guild_id, items in data.items():
                if guild==guild_id:
                    if not any(title in itm['url'] for  itm in items):
                        return False,0,None
                    if unset:
                        if sum(channel in itm["CustomChannel"] for itm in items)==1:
                            for item in items:
                                if title in item["url"]:
                                    return True,1,item["url"]
                    else:
                        count=sum(title in itm["url"] for itm in items)
                        if count>1:
                            return False,count,None
                        for item in items:
                            if title in item["url"]:
                                return True,1,item["url"]

                    return False,0,None
            
        else:
            return False,0, None

    except Exception as e:
        logger.fatal("Exception occured in custom_channel.get_full_url for title:%s",title,exc_info=1)
        raise e



def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)