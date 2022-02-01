try:
    import lightbulb
    import json
    import hikari
    import wattpad as ws

except Exception as e:
    print(str(e))

plugin=lightbulb.Plugin('StoryPlugin')


#permissions
@lightbulb.Check
def is_AdminOrMod(ctx):
    roles=ctx.member.get_roles()
    if any(role.permissions.all(hikari.Permissions.ADMINISTRATOR) for role in roles) or any(role.permissions.all(hikari.Permissions.MODERATE_MEMBERS) for role in roles):
        return True

    return False

#permissions


#add story start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.option('storyurl', 'Url of the story to be added')
@lightbulb.command('addstory','Adds your current story to receive new chapter noifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def addstory(ctx):
    with open('stories.json','r') as s:
        stories=json.load(s)
    
    if ctx.options.storyurl!=None and ws.checkStory(ctx.options.storyurl):
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

        await ctx.respond('**Story has been successfully added to this server\'s list.\nYou will receive new chapter notications from this story.**')


    else:
        await ctx.respond('**Oops!! There is something wrong with your story link. Check the link and try again.**')
        

    
#remove story start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.option('storyurl','Url of the story to be removed')
@lightbulb.command('removestory','removes your current story from receiving new chapter notifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def removestory(ctx):
    url=ctx.options.storyurl
    with open('stories.json','r') as f:
        stories=json.load(f)
    if ctx.channel_id is not None:
        for guild in stories:
            if guild==str(ctx.guild_id) and str(url) in stories[str(ctx.guild_id)]:
                stories[str(ctx.guild_id)].remove(str(url))

    with open('stories.json','w') as f:
        json.dump(stories,f,indent=2)

    await ctx.respond('**This story has been removed.\nYou will no loger receive new chapter notifications from this story.**')



#remove story end


#get stories start
@plugin.command
@lightbulb.command('getstories','fetch your server\'s stories that are getting new chapter updates')
@lightbulb.implements(lightbulb.SlashCommand)
async def getstories(ctx):
    with open('stories.json') as f:
        stories=json.load(f)
    msg=''
    if ctx.guild_id is not None:
        for guild in stories:
            if guild==str(ctx.guild_id):
                for key in stories[guild]:
                    #msg=str(msg)+'*'+str(key)+'\n'
                    msg=f'{str(msg)} {str(key)}\n'
    if not msg:
        msg='**So empty!! No stories were added to your list.**'
    else:
        msg=f'**Your stories list:\n** {msg}'

    await ctx.respond(msg)

#get stories end


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

