import lightbulb
import hikari
from wattpad.logger.baselogger import BaseLogger
from wattpad.utils.config import Config
from wattpad.meta.models.enum import HelpCategory

plugin=lightbulb.Plugin("HelpPlugin")

file_prefix= "wattpad.plugins.commands.help"
logger= BaseLogger().loggger_init()

@plugin.command
@lightbulb.option("category","Use channel/story/custom message/author/custom channel/setup/about for detailed help on categories", str, choices=("Channel","Story","Author","Custom Message","Custom Channel","Setup","About"), required=False)
@lightbulb.command("help","Check the help comamnd. Use empty/channel/story/author/setup/about as categories", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.SlashContext):
    try:
        logger.info("%s.help method invoked for server: %s, category: %s", file_prefix, ctx.guild_id, ctx.options.category)

        category:str= ctx.options.category
        msgs= await Config().get_messages("en")

        if not category:
            logger.info("Empty help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:title']}", description=f"{msgs['help:desc']}", color=0xFF0000)

            embed.add_field(name=f"{msgs['help:note:title']}", value=f"{msgs['help:note']}", inline=False)

            embed.add_field(name=f"**set-channel**", value=f"{msgs['help:set:channel']}", inline=False)
            embed.add_field(name=f"**unset-channel**", value=f"{msgs['help:unset:channel']}", inline=True)
            embed.add_field(name=f"**check-channels**", value=f"{msgs['help:check:channels']}", inline=True)

            embed.add_field(name=f"**follow-story**", value=f"{msgs['help:follow:story']}", inline=False)
            embed.add_field(name=f"**unfollow-story**", value=f"{msgs['help:unfollow:story']}", inline=True)
            embed.add_field(name=f"**check-stories**", value=f"{msgs['help:check:stories']}", inline=True)

            embed.add_field(name=f"**follow-author**", value=f"{msgs['help:follow:author']}", inline=False)
            embed.add_field(name=f"**unfollow-author**", value=f"{msgs['help:unfollow:author']}", inline=True)
            embed.add_field(name=f"**check-authors**", value=f"{msgs['help:check:authors']}", inline=True)

            embed.add_field(name=f"**set-custom-channel for-story**", value=f"{msgs['help:set:custom:channel:story']}", inline=False)
            embed.add_field(name=f"**set-custom-channel for-author**", value=f"{msgs['help:set:custom:channel:author']}", inline=True)
            embed.add_field(name=f"**unset-custom-channel for-story**", value=f"{msgs['help:unset:custom:channel:story']}", inline=True)
            embed.add_field(name=f"**unset-custom-channel for-author**", value=f"{msgs['help:unset:custom:channel:author']}", inline=True)
            embed.add_field(name=f"**check-custom-channels**",value=f"{msgs['help:check:custom:channels']}", inline=True)

            embed.add_field(name=f"**set-custom-message for-story**", value=f"{msgs['help:set:custom:msg:story']}", inline=False)
            embed.add_field(name=f"**set-custom-message for-author**", value=f"{msgs['help:set:custom:msg:author']}", inline=True)
            embed.add_field(name=f"**unset-custom-message for-story**", value=f"{msgs['help:unset:custom:msg:story']}", inline=True)
            embed.add_field(name=f"**unset-custom-message for-author**", value=f"{msgs['help:unset:custom:msg:author']}", inline=True)
            embed.add_field(name=f"**check-custom-messages**",value=f"{msgs['help:check:custom:msgs']}", inline=True)

        elif category.lower() == HelpCategory.About:
            logger.info("About help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:about:title']}", description=f"{msgs['help:about']}", color=0xFF0000)

        elif category.lower() == HelpCategory.Setup:
            logger.info("Setup help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:setup:title']}", description=f"{msgs['help:setup']}", color=0xFF0000)

        elif category.lower() == HelpCategory.Channel:
            logger.info("Channel help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:channel:title']}", color=0xFF0000)

            embed.add_field(name=f"**set-channel**", value=f"{msgs['set:channel']}{msgs['set:channel:ex']}", inline=False)
            embed.add_field(name=f"**unset-channel**",value=f"{msgs['unset:channel']}{msgs['unset:channel:ex']}", inline=False)
            embed.add_field(name=f"**check-channels**",value=f"{msgs['check:channels']}{msgs['check:channels:ex']}", inline=False)

        elif category.lower == HelpCategory.Story:
            logger.info("Story help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:story:title']}", color=0xFF0000)

            embed.add_field(name=f"**follow-story**", value=f"{msgs['follow:story']}{msgs['follow:story:ex']}", inline=False)
            embed.add_field(name=f"**unfollow-story**",value=f"{msgs['unfollow:story']}{msgs['unfollow:story:ex']}", inline=False)
            embed.add_field(name=f"**check-stories**",value=f"{msgs['check:stories']}{msgs['check:stories:ex']}", inline=False)

        elif category.lower() == HelpCategory.Author:
            logger.info("Author help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:author:title']}", color=0xFF0000)

            embed.add_field(name=f"**follow-author**", value=f"{msgs['follow:author']}{msgs['follow:author:ex']}", inline=False)
            embed.add_field(name=f"**unfollow-author**",value=f"{msgs['unfollow:author']}{msgs['unfollow:author:ex']}", inline=False)
            embed.add_field(name=f"**check-authors**",value=f"{msgs['check:authors']}{msgs['check:authors:ex']}", inline=False)

        elif category.lower() == HelpCategory.CustomChannel:
            logger.info("Custom channel help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:custom:channel:title']}", color=0xFF0000)

            embed.add_field(name=f"**set-custom-channel for-story**", value=f"{msgs['set:custom:channel:story']}{msgs['set:custom:channel:story:ex']}", inline=False)
            embed.add_field(name=f"**set-custom-channel for-author**", value=f"{msgs['set:custom:channel:author']}{msgs['set:custom:channel:author:ex']}", inline=False)
            embed.add_field(name=f"**unset-custom-channel for-story**", value=f"{msgs['unset:custom:channel:story']}{msgs['unset:custom:channel:story:ex']}", inline=False)
            embed.add_field(name=f"**unset-custom-channel for-author**", value=f"{msgs['unset:custom:channel:author']}{msgs['unset:custom:channel:author:ex']}", inline=False)
            embed.add_field(name=f"**check-custom-channels**",value=f"{msgs['check:custom:channels']}{msgs['check:custom:channels:ex']}", inline=False)

        elif category.lower() == HelpCategory.CustomMsg:
            logger.info("Custom message help command triggered")

            embed= hikari.Embed(title=f"{msgs['help:custom:msg:title']}", color=0xFF0000)

            embed.add_field(name=f"**set-custom-message for-story**", value=f"{msgs['set:custom:msg:story']}{msgs['set:custom:msg:story:ex']}", inline=False)
            embed.add_field(name=f"**set-custom-message for-author**", value=f"{msgs['set:custom:msg:author']}{msgs['set:custom:msg:author:ex']}", inline=False)
            embed.add_field(name=f"**unset-custom-message for-story**", value=f"{msgs['unset:custom:msgl:story']}{msgs['unset:custom:msg:story:ex']}", inline=False)
            embed.add_field(name=f"**unset-custom-message for-author**", value=f"{msgs['unset:custom:msg:author']}{msgs['unset:custom:msg:author:ex']}", inline=False)
            embed.add_field(name=f"**check-custom-messages**",value=f"{msgs['check:custom:msgs']}{msgs['check:custom:msgs:ex']}", inline=False)

        await ctx.respond(embed=embed)
    
    except Exception as e:
        logger.fatal("Exception occured in %s.help method for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e
    