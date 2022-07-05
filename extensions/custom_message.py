from decimal import DecimalException
import hikari
import lightbulb
import logging
import json
import helpers.json_helper as jhelper

plugin=lightbulb.Plugin("CustomMessagrPlugin")

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger(name="cmessage")
logger.setLevel(logging.ERROR)


@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","URL/title of the story/announcement for which this message needs to be applied",required=False)
@lightbulb.option("custommessage","Your custom message",required=True)
@lightbulb.option("category","whether your custom message is for story or announcement updates",str,choices=("story","announcement"),required=True)
@lightbulb.command("setcustommessage","set a custom message that bot can use when sharing updates")
@lightbulb.implements(lightbulb.SlashCommand)
async def setCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("setCustomMessage command has been triggered in server: %s, category: %s, message: %s",ctx.guild_id,ctx.options.category,ctx.options.custommessage,)

        
        category:str=ctx.options.category
        customMsg=ctx.options.custommessage
        guildId=str(ctx.guild_id)
        responsMsg="Your custom message has been set succesfully."
        url=ctx.options.url
        domain="wattpad.com"

        isStory=False
        isAuthor=False
        found=False
        count=0

        if category.lower()=="story":
            isStory=True
        else:
            isAuthor=True

        # with open('messages.json','r') as m:
        #     messages=json.load(m)

        #async impl of reading from json file:
        if url:
            if isStory:
                messages=await jhelper.read_from_json("stories.json")
            else:
                messages=await jhelper.read_from_json("authors.json")
            
            if domain not in url:
                found,count,full_url=await get_full_url(url,guildId,messages)
            else:
                found=True

            if found and count==1:
                url=full_url
            elif count>1:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"You're following multiple {'Stories' if isStory else 'Authors'} that has {url} in it. Please use the full url of the {'Story' if isStory else 'Author Profile'}."))
                found=False
        else:
            found=True
            messages=await jhelper.read_from_json("messages.json")

        if found:
            if url:
                if guildId not in messages:
                    await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description=f"You're not following any {'stories' if isStory else 'Authors'} in this server. Try {'`/followstory`' if isStory else '`/followauthor`'} command to follow."))
                else:
                    for guild,items in messages.items():
                        if guild==guildId:
                            if not any(url==itm["url"] for itm in items):
                                await ctx.respond(embed=hikari.Embed(title=f"🛑Error:", description=f"You're not following this {'story' if isStory else 'Author'} in this server. Try {'`/followstory`' if isStory else '`/followauthor`'} command to follow."))
                            else:
                                for item in items:
                                    if item["url"]==url:
                                        item["CustomMsg"]=customMsg
                                        if isStory:
                                            result=await jhelper.write_to_json("stories.json",messages)
                                        else:
                                            result=await jhelper.write_to_json("authors.json",messages)

                                        responsMsg=responsMsg+f" The bot will use this message while sharing updates from {'story' if isStory else 'Author'} {url}."
            else:
                if isStory:
                    if guildId not in messages:
                        messages[guildId]={"story":f'{customMsg}',"announcement":""}

                    else:
                        for guild, msg in messages.items():
                            if guild==guildId:
                                if not url:
                                    msg["story"]=f"{customMsg}"
                                else:
                                    msg["story"]=f"{customMsg}"


                    responsMsg=responsMsg+" The bot will use this message while sharing story updates from now on."



                else:
                    if guildId not in messages:
                        messages[guildId]={"story":"","announcement":f'{customMsg}'}

                    else:
                        for guild, msg in messages.items():
                            if guild==guildId:
                                msg["announcement"]=f"{customMsg}"

                    responsMsg=responsMsg+" The bot will use this message while sharing announcement updates from now on."



                # with open("messages.json","w") as m:
                #         json.dump(messages,m,indent=2)

                #async impl of writing to json files:
                result=await jhelper.write_to_json("messages.json",messages)
            if result:
                await ctx.respond(embed=hikari.Embed(title="Success!!",description=f"{responsMsg}"))
            else:
                await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description=f"Uh-ohh! Something went wrong. Try `/checkcustommsg` command to check if the custom message has been setup."))


    except Exception as e:
        logger.fatal("Exception in setCustomMessage command in server: %s, category: %s, message: %s",ctx.guild_id,ctx.options.category,ctx.options.custommessage,exc_info=1)
        raise e


@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","URL/title of the story or announcement for which the custom message needs to be removed.",required=False)
@lightbulb.option("category","whether you want to remove story or announcement custom message",str,choices=("story","announcement"),required=True)
@lightbulb.command("unsetcustommessage","remove the custom message for updates. After removing default messages will be used")
@lightbulb.implements(lightbulb.SlashCommand)
async def removeCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("removeCustomMessage command has been invoked in server: %s, category: %s",ctx.guild_id,ctx.options.category)

        guildId=str(ctx.guild_id)
        category=ctx.options.category
        isEmpty=False
        url=ctx.options.url
        domain="wattpad.com"
        responseMsg=""

        isStory=False
        isAuthor=False
        found=False
        count=0
        result=""

        if category.lower()=="story":
            isStory=True
        else:
            isAuthor=True

        # with open("messages.json","r") as m:
        #     messages=json.load(m)

         #async impl of reading from json file:
        if url:
            if isStory:
                messages=await jhelper.read_from_json("stories.json")
            else:
                messages=await jhelper.read_from_json("authors.json")
            
            if domain not in url:
                found,count,full_url=await get_full_url(url,guildId,messages)
            else:
                found=True

            if found and count==1:
                url=full_url
            elif count>1:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"You're following multiple {'Stories' if isStory else 'Authors'} that has {url} in it. Please use the full url of the {'Story' if isStory else 'Author Profile'}."))
                found=False
            else:
                await ctx.respond(embed=hikari.Embed(title=f"🛑 Error:", description=f"You're not following any {'stories' if isStory else 'author'} that has title {url} in it. Try using the full url."))

        else:
            messages=await jhelper.read_from_json("messages.json")

        if url:
            if found:
                if guildId not in messages:
                    await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description=f"You're not following any {'stories' if isStory else 'Authors'} in this server. Try {'`/followstory`' if isStory else '`/followauthor`'} command to follow."))
                else:
                    for guild,items in messages.items():
                        if guild==guildId:
                            if not any(url==itm["url"] for itm in items):
                                await ctx.respond(embed=hikari.Embed(title=f"🛑Error:", description=f"You're not following this {'story' if isStory else 'Author'} in this server. Try {'`/followstory`' if isStory else '`/followauthor`'} command to follow."))
                            else:
                                for item in items:
                                    if item["url"]==url:
                                        item["CustomMsg"]=""
                                        if isStory:
                                            result=await jhelper.write_to_json("stories.json",messages)
                                        else:
                                            result=await jhelper.write_to_json("authors.json",messages)

                                        responseMsg=responseMsg+f" Your custom message for the {'story' if isStory else 'Announcement'} from {url} has been removed succesfully."

        else:
            if messages and guildId in messages:
                if category=="story":
                    for guild, msg in messages.items():
                        if guild==guildId:
                            if msg["story"]=="" or msg["story"] is None:
                                isEmpty=True
                            msg["story"]=""
            
                else:
                    for guild, msg in messages.items():
                        if guild==guildId:
                            if msg["announcement"]=="" or msg["announcement"] is None:
                                isEmpty=True
                            msg["announcement"]=""
            
                # with open("messages.json","w") as m:
                #     json.dump(messages,m,indent=2)

                #async impl of writing to json files:
                result=await jhelper.write_to_json("messages.json",messages)

                responseMsg=f"Your {category} custom message has been removed succesfully."
                if isEmpty:
                    responseMsg=f"You don\'t have any custom messages set up for {category} category."
                

            else:
                responseMsg=f"Empty!! No custom messages has been set before.\n Use `/setcustommessage` command to set a custom message."
                await ctx.respond(responseMsg)

        if isEmpty:
            await ctx.respond(embed=hikari.Embed(title="Empty!!", description=f"You don't have any custom messages setup for {category} category."))

        if (result or found) and not isEmpty:
            await ctx.respond(embed=hikari.Embed(title=f"Success!!",description=f"{responseMsg}"))
        elif found and not isEmpty:
            await ctx.respond(embed=hikari.Embed(title=f"🛑Error:",description="Uh-oh!! Something went wrong. Try `/checkcustommsg` to check if the custom message has been unset.") )

    except Exception as e:
        logger.fatal("Exception in setCustomMessage command in server: %s, category: %s",ctx.guild_id,ctx.options.category,exc_info=1)
        raise e

@plugin.command()
@lightbulb.option("category","whether you want to check story or announcement custom messages",str,choices=("story","announcement"),required=False)
@lightbulb.command("checkcustommsg","check your custom story and announcement messages you've setup.")
@lightbulb.implements(lightbulb.SlashCommand)
async def checkCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("checkCustomMessage command has been invoked in server: %s",ctx.guild_id)
        guildId=str(ctx.guild_id)
        responseMsg="Your custom messages:\n"
        emptyMsg="Empty!! Looks like you didn\'t set up any custom messages.\n Try `/setcustommessage` command to set a custom message."
        category:str=ctx.options.category

        isAuthor=False
        isStory=False
        storyContent=""
        authorContent=""
        isEmpty=True
        noCategory=False

        if category and  category.lower()=="story":
            isStory=True
            stories=await jhelper.read_from_json("stories.json")
        elif category and category.lower()=="announcement":
            isAuthor=True
            authors=await jhelper.read_from_json("authors.json")
        else:
            noCategory=True
            authors=await jhelper.read_from_json("authors.json")
            stories=await jhelper.read_from_json("stories.json")

        # with open("messages.json","r") as m:
        #     messages=json.load(m)

         #async impl of reading from json file:
        messages=await jhelper.read_from_json("messages.json")
        

        #fetch from messages.json
            #fetch by categories

        if messages and guildId in messages:
            for guild, msg in messages.items():
                if guild==guildId:
                    if msg["story"]=="" and msg["announcement"]=="":
                        isEmpty=True
                    else:
                        if msg["story"]:
                            isEmpty=False
                            storyContent=storyContent+f"For whole Category: {msg['story']}\n"
                        if msg["announcement"]:
                            isEmpty=False
                            authorContent=authorContent+f"For whole Category: {msg['announcement']}\n"

        if isStory or noCategory:
            if guildId in stories:
                for guild, items in stories.items():
                    if guild==guildId:
                        for item in items:
                            if "CustomMsg" in item:
                                if item["url"] and item["CustomMsg"]:
                                    isEmpty=False
                                    storyContent=storyContent+f"{item['url']} : {item['CustomMsg']}\n"

        if isAuthor or noCategory:
            if guildId in authors:
                for guild, items in authors.items():
                    if guild==guildId:
                            for item in items:
                                if "CustomMsg" in item:
                                    if item["url"] and item["CustomMsg"]:
                                        isEmpty=False
                                        authorContent=authorContent+f"{item['url']} : {item['CustomMsg']}\n"



        if isEmpty:
            await ctx.respond(embed=hikari.Embed(title=f"So Empty!!:", description=f"Looks like you have not setup any custom messages yet. Use `/setcustommessage` command to set one."))
        else:
            if isStory and not storyContent:
                await ctx.respond(embed=hikari.Embed(title="Empty!!", description="Looks like you have not setup any custom messages for story updates."))
            elif isAuthor and not authorContent:
                await ctx.respond(embed=hikari.Embed(title="Empty!!", description="Looks like you have not setup any custom messages for Announcement updates."))
            else:
                em=hikari.Embed(title="Your Custom Messages:")
                if storyContent:
                    if isStory or noCategory:
                        em.add_field(name="Stories", value=f"{storyContent}\n")
                if authorContent:
                    if isAuthor or noCategory:
                        em.add_field(name="Announcements:", value=f"{authorContent}")
                
                await ctx.respond(embed=em)

        

        #fetch from authors and stories by category

        #consolidate all of them and send it back

        #region oldcode
        # if messages and guildId in messages:
        #     for guild,msg in messages.items():
        #         if guild==guildId:
        #             if msg["story"]=="" and msg["announcement"]=="":
        #                 await ctx.respond(emptyMsg)
        #             else:
        #                 if msg["story"]!="":
        #                     responseMsg=responseMsg+f'**Story:** {msg["story"]}\n'
        #                 if msg["announcement"]!="":
        #                     responseMsg=responseMsg+f'**Announcement:** {msg["announcement"]}'

        #                 await ctx.respond(responseMsg)


        # else:
        #     await ctx.respond(emptyMsg)'
            
        #     '
        #endregion oldcode

    except Exception as e:
        logger.fatal("Exception in chcekCustomMessages command for server %s",ctx.guild_id,exc_info=1)
        raise e



async def get_full_url(title:str,guild:str,data:dict):
    try:
        logger.info("custom_message.get_full_url triggered for title:%s",title)

        if guild in data:
            for guild_id, items in data.items():
                if guild==guild_id:
                    if not any(title in itm['url'] for  itm in items):
                        return False,0,None
                    
                    
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
        logger.fatal("Exception occured in custom_message.get_full_url for title:%s",title,exc_info=1)
        raise e


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)