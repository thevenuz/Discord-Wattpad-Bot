import hikari
import lightbulb
from wattpad.logger.baselogger import BaseLogger
from wattpad.pluginsexecution.commandsexec.storyexec import StoryExec
from wattpad.utils.config import Config
from wattpad.utils.storyutil import StoryUtil

plugin=lightbulb.Plugin("StoryPlugin")

file_prefix="wattpad.plugins.commands.story"

logger=BaseLogger().loggger_init()

@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("storyurl", "Url of the story you want to follow",str,required=True)
@lightbulb.command("follow-story","Follow a story to receive new chapter noifications", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def follow_story(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.follow_story method invoked for story: %s", file_prefix, ctx.options.storyurl)

        storyURL=ctx.options.storyurl
        guildId= str(ctx.guild_id)

        #TODO: add a set-language command and load different languges
        msgs= await Config().get_messages("en")

        #call the execution
        result= await StoryExec().follow_story(storyURL, guildId)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['follow:story:success']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.follow_story method for story: %s, server: %s, Error: %s", file_prefix, storyURL, guildId, result.ResultInfo)

            if result.IsInvalidUrl:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['invalid:url']}", description=f"{msgs['invalid:story:url']}", color=0xFF0000))

            elif result.AlreadyFollowing:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['already:following:story']}", color=0xFF0000))
                
            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))

        
    except Exception as e:
        logger.fatal("Exception occured in %s.follow_story method invoked for story: %s", file_prefix, ctx.options.storyurl,exc_info=1)
        raise e
    
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option("storyurl","Url of the story you want to unfollow. You can also use title instead of full url", str, required=True)
@lightbulb.command("unfollow-story", "Unfollow a story that you're already following to stop receiving new chapter updates", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unfollow_story(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.unfollow_story method invoked for story: %s, server: %s", file_prefix, ctx.options.storyurl, ctx.guild_id)

        storyURL= ctx.options.storyurl
        guildId= str(ctx.guild_id)

        msgs= await Config().get_messages("en")

        #call the exec
        result= await StoryExec().unfollow_story(storyURL, guildId)

        if result.IsSuccess:
            await ctx.respond(embed=hikari.Embed(title=f"{msgs['success']}", description=f"{msgs['unfollow:story:success']}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.unfollow_story method for story: %s, server: %s, Error: %s", file_prefix, storyURL, guildId, result.ResultInfo)

            if result.IsInvalidTitle:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['invalid:title']}", color=0xFF0000))

            elif result.HasMultipleStories:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['story:multiple:title']}", color=0xFF0000))
            
            elif result.NotFollowing:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['error']}", description=f"{msgs['unfollow:story:not:following']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))
            

    
    except Exception as e:
        logger.fatal("Exception occured in %s.unfollow_story method invoked for story: %s, server: %s", file_prefix, ctx.options.storyurl, ctx.guild_id, exc_info=1)
        raise e
    

@plugin.command
@lightbulb.command("check-stories","check the stories that you are following in this server", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_stories(ctx: lightbulb.SlashContext) -> None:
    try:
        logger.info("%s.check_stories method invoked for server: %s", file_prefix, ctx.guild_id)

        guildId= str(ctx.guild_id)

        msgs= await Config().get_messages("en")

        #call the exec
        result = await StoryExec().check_stories(guildId)

        if result.IsSuccess:
            #build the description of the msg
            story_data= await StoryUtil().build_story_data_msg(result.Data)

            await ctx.respond(embed=hikari.Embed(title=f"{msgs['check:stories:following']}", description=f"{story_data}", color=0xFF0000))

        else:
            logger.error("Error occured in %s.check_stories method for server: %s, Error: %s", file_prefix, guildId, result.ResultInfo)
            if result.IsEmpty:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['empty']}", description=f"{msgs['check:stories:empty']}", color=0xFF0000))

            else:
                await ctx.respond(embed=hikari.Embed(title=f"{msgs['unknown:error']}", description=f"{msgs['unknown:error:msg']}", color=0xFF0000))


    except Exception as e:
        logger.fatal("Exception occured in %s.check_stories method invoked for server: %s", file_prefix, ctx.guild_id,exc_info=1)
        raise e
    


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)