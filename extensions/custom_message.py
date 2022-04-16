import hikari
import lightbulb
import logging
import json

plugin=lightbulb.Plugin("CustomMessagrPlugin")

logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)


@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("custommessage","Your custom message",required=True)
@lightbulb.option("category","whether your custom message is for story or announcement updates",str,choices=("story","announcement"),required=True)
@lightbulb.command("setcustommessage","set a custom message that bot can use when sharing updates")
@lightbulb.implements(lightbulb.SlashCommand)
async def setCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("setCustomMessage command has been triggered in server: %s, category: %s, message: %s",ctx.guild_id,ctx.options.category,ctx.options.custommessage,)

        
        category=ctx.options.category
        customMsg=ctx.options.custommessage
        guildId=str(ctx.guild_id)
        responsMsg="Your custom message has been set succesfully."

        with open('messages.json','r') as m:
            messages=json.load(m)

        if category=="story":
            if guildId not in messages:
                messages[guildId]={"story":f'{customMsg}',"announcement":""}

            else:
                for guild, msg in messages.items():
                    if guild==guildId:
                        msg["story"]=f"{customMsg}"

            responsMsg=responsMsg+" The bot will use this message while sharing story updates from now on."



        else:
            if guildId not in messages:
                messages[guildId]={"story":"","announcement":f'{customMsg}'}

            else:
                for guild, msg in messages.items():
                    if guild==guildId:
                        msg["announcement"]=f"{customMsg}"

            responsMsg=responsMsg+" The bot will use this message while sharing story updates from now on."



        with open("messages.json","w") as m:
                json.dump(messages,m,indent=2)

        await ctx.respond(responsMsg)


    except Exception as e:
        logger.fatal("Exception in setCustomMessage command in server: %s, category: %s, message: %s",ctx.guild_id,ctx.options.category,ctx.options.custommessage,exc_info=1)
        raise e


@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("category","whether you want to remove story or announcement custom message",str,choices=("story","announcement"),required=True)
@lightbulb.command("unsetcustommessage","remove the custom message for updates. After removing default messages will be used")
@lightbulb.implements(lightbulb.SlashCommand)
async def removeCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("removeCustomMessage command has been invoked in server: %s, category: %s",ctx.guild_id,ctx.options.category)

        guildId=str(ctx.guild_id)
        category=ctx.options.category
        isEmpty=False

        with open("messages.json","r") as m:
            messages=json.load(m)

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
            
            with open("messages.json","w") as m:
                json.dump(messages,m,indent=2)

            responseMsg=f"Your {category} custom message has been removed succesfully."
            if isEmpty:
                responseMsg=f"You don\'t have any custom messages set up for {category} category."
            await ctx.respond(responseMsg)

        else:
            responseMsg=f"Empty!! No custom messages has been set before.\n Use `/setcustommessage` command to set a custom message."
            await ctx.respond(responseMsg)

    except Exception as e:
        logger.fatal("Exception in setCustomMessage command in server: %s, category: %s",ctx.guild_id,ctx.options.category,exc_info=1)
        raise e

@plugin.command()
@lightbulb.command("checkcustommsg","check your custom story and announcement messages you've setup.")
@lightbulb.implements(lightbulb.SlashCommand)
async def checkCustomMessage(ctx:lightbulb.SlashContext):
    try:
        logger.info("checkCustomMessage command has been invoked in server: %s",ctx.guild_id)
        guiidId=str(ctx.guild_id)
        responseMsg="Your custom messages:\n"
        emptyMsg="Empty!! Looks like you didn\'t set up any custom messages.\n Try `/setcustommessage` command to set a custom message."

        with open("messages.json","r") as m:
            messages=json.load(m)

        if messages and guiidId in messages:
            for guild,msg in messages.items():
                if guild==guiidId:
                    if msg["story"]=="" and msg["announcement"]=="":
                        await ctx.respond(emptyMsg)
                    else:
                        if msg["story"]!="":
                            responseMsg=responseMsg+f'**Story:** {msg["story"]}\n'
                        if msg["announcement"]!="":
                            responseMsg=responseMsg+f'**Announcement:** {msg["announcement"]}'

                        await ctx.respond(responseMsg)


        else:
            await ctx.respond(emptyMsg)

    except Exception as e:
        logger.fatal("Exception in chcekCustomMessages command for server %s",ctx.guild_id,exc_info=1)
        raise e



def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)