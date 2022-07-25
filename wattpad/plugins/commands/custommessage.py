from soupsieve import select
from wattpad.meta.models.enum import Category
from wattpad.pluginsexecution.commandsexec.custommessageexec import CustomMessageExec
from wattpad.utils.authorutil import AuthorUtil
from wattpad.utils.config import Config
import lightbulb
from wattpad.logger.baselogger import BaseLogger
import hikari

from wattpad.utils.storyutil import StoryUtil

plugin= lightbulb.Plugin("CustomMessagePlugin")

file_prefix= "wattpad.plugins.commands.custommessage"
logger=BaseLogger().loggger_init()

@plugin.command()
@lightbulb.command("set-custom-message","set a custom message for bot to use while sharing updates",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_custom_message(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message method invoked for server: %s", file_prefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0Xff500a))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e


@set_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.option("message","Your custom message for story updates",required=True)
@lightbulb.command("for-story","set a custom messages for a particular story", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_message_for_story(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message)

        guildId= str(ctx.guild_id)
        message= ctx.options.message
        story_url= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().set_custom_message_for_story(guildId, story_url, message)

        if result.IsSuccess:
            msg_description= msgs['custom:msg:set:story:success'].format(f"{message}", f"{story_url}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.set_custom_message_for_story method for server: %s, story: %s, msg: %s, error: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))
            
            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message_for_story method invoked for server: %s, story: %s, msg: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message,exc_info=1)
        raise e
    
@set_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the Author",str, required=True)
@lightbulb.option("message","Your custom message for author's announcements",required=True)
@lightbulb.command("for-announcements","set a custom messages for a particular author's announcements", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_custom_message_for_author(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message)

        guildId= str(ctx.guild_id)
        message= ctx.options.message
        author_url= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().set_custom_message_for_author(guildId, author_url, message)

        if result.IsSuccess:
            msg_description= msgs['custom:msg:set:author:success'].format(f"{message}", f"{author_url}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.set_custom_message_for_author method for server: %s, author: %s, msg: %s, error: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))
            
            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['author:multiple:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.set_custom_message_for_author method invoked for server: %s, author: %s, msg: %s", file_prefix, ctx.guild_id, ctx.options.url, ctx.options.message,exc_info=1)
        raise e

@plugin.command()
@lightbulb.command("unset-custom-message","unset a custom message that's been setup before",auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def unset_custom_message(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_message method invoked for server: %s", file_prefix, ctx.guild_id)

        #code should not hit this
        await ctx.respond(embed=hikari.Embed(title=f"Check subcommands", description=f"Check sub commands", color=0Xff500a))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_message method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e

@unset_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.command("for-story","set a custom messages for a particular story", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unset_custom_message_for_story(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_message_for_story method invoked for server: %s, story: %s", file_prefix, ctx.guild_id, ctx.options.url)

        guildId= str(ctx.guild_id)
        story_url= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().unset_custom_message_for_story(guildId, story_url)

        if result.IsSuccess:
            msg_description= msgs["custom:msg:unset:story:success"].format(f"{story_url}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.unset_custom_message_for_story for server: %s, story: %s, error: %s", file_prefix, ctx.guild_id, ctx.options.url, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))


            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))


    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_message_for_story method invoked for server: %s, story: %s", file_prefix, ctx.guild_id, ctx.options.url,exc_info=1)
        raise e
    
@unset_custom_message.child
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("url","Mention the title/URL of the story",str, required=True)
@lightbulb.command("for-announcement","set a custom messages for a particular story", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def unset_custom_message_for_author(ctx:lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unset_custom_message_for_author method invoked for server: %s, author: %s", file_prefix, ctx.guild_id, ctx.options.url)

        guildId= str(ctx.guild_id)
        story_url= ctx.options.url

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().unset_custom_message_for_author(guildId, story_url)

        if result.IsSuccess:
            msg_description= msgs["custom:msg:unset:story:success"].format(f"{story_url}")
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msg_description}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.unset_custom_message_for_author for server: %s, author: %s, error: %s", file_prefix, ctx.guild_id, ctx.options.url, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.HasMultipleResults:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))


    
    except Exception as e:
        logger.fatal("Exception occured in %s.unset_custom_message_for_author method invoked for server: %s, author: %s", file_prefix, ctx.guild_id, ctx.options.url,exc_info=1)
        raise e

@plugin.command
@lightbulb.option("category","Select whether you want to check story/author announcements custom messages",str, choices=("story", "announcements"), required=False)
@lightbulb.command("check-custom-messages", "Check the existing custom messages for stories and author updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_custom_messages(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.check_custom_messages method invoked for server: %s, category: %s", file_prefix, ctx.guild_id, ctx.options.category)

        guildId= str(ctx.guild_id)
        category= ctx.options.category
        story_return_msg=""
        author_return_msg=""
        msg_description=""

        msgs= await Config().get_messages("en")

        #call the exec
        result= await CustomMessageExec().check_custom_messages(guildId, category=category)

        if result.IsSuccess:
            if result.StoryCustomMsgs:
                story_return_msg= await StoryUtil().build_check_custom_msgs_msg(result.StoryCustomMsgs)

            if result.AuthorCustomMsgs:
                author_return_msg= await AuthorUtil().build_check_custom_msgs_msg(result.AuthorCustomMsgs)

            if category:
                if category.lower() == Category.Story.value:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:msgs']}", description=f"{msgs['story:custom:msgs']}\n{story_return_msg}", color=0Xff500a))
                
                elif category.lower() == Category.Announcements.value:
                    await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:msgs']}", description=f"{msgs['author:custom:msgs']}\n{author_return_msg}", color=0Xff500a))

            else:
                if story_return_msg:
                    msg_description= msg_description + msgs['story:custom:msgs'] + "\n" + story_return_msg + "\n\n"

                if author_return_msg:
                    msg_description= msg_description + msgs['author:custom:msgs'] + "\n" + author_return_msg

                await ctx.respond(embed=hikari.Embed(title=f"{msgs['custom:msgs']}", description=f"{msg_description}", color=0Xff500a))

        else:
            logger.error("Error occured in %s.check_custom_messages method for server: %s, category: %s, error: %s", file_prefix, guildId, category, result.ResultInfo)

            if result.IsEmpty:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['custom:msgs:not:set']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
    
    except Exception as e:
        logger.fatal("Exception occured in %s.check_custom_messages method invoked for server: %s, category: %s", file_prefix, ctx.guild_id, ctx.options.category,exc_info=1)
        raise e
    

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin) 