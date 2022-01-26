import hikari
import lightbulb
import json

plugin=lightbulb.Plugin('ChannelPlugin')

#TODO later: define permissions in a single place and use them in all plugins
#permissions
@lightbulb.Check
def is_AdminOrMod(ctx):
    roles=ctx.member.get_roles()
    if any(role.permissions.all(hikari.Permissions.ADMINISTRATOR or hikari.Permissions.MODERATE_MEMBERS) for role in roles):
        return True

    return False

#permissions


@plugin.command
@lightbulb.command('channel','test plugin')
@lightbulb.implements(lightbulb.SlashCommand)
async def channel(ctx):
    await ctx.respond('channel')


#addchannel command start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('addchannel','adds ypur channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def addchannel(ctx):
    with open('channels.json','r') as f:
            channels=json.load(f)

    if ctx.channel_id is not None:
        if not channels:
                channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
        else:
            if str(ctx.guild_id) not in channels:
                    channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
            else:
                for channel in channels:
                    if channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                        channels[str(ctx.guild_id)].append(str(ctx.channel_id))
        
    with open('channels.json','w') as f:
        json.dump(channels,f,indent=2)

    await ctx.respond('Success.\nThis channel has been added to receive new chapter notifications.')


#addchannel command end

#remove channel start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('removechannel','removes your channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def removechannel(ctx):
    with open('channels.json','r') as f:
        channels=json.load(f)

    if ctx.channel_id is not None:
        for channel in channels:
            if channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                channels[str(ctx.guild_id)].remove(str(ctx.channel_id))

    with open('channels.json','w') as f:
        json.dump(channels,f,indent=2)

    await ctx.respond('This channel will not receive new chapter notifications from now.')


#remove channel end


#TODO later: move getchannels to this plugin
# #get channels start
# @plugin.command
# @lightbulb.command('getchannels','Gives a list of your current channels')
# @lightbulb.implements(lightbulb.SlashCommand)
# async def getchannels(ctx):
#         with open('channels.json') as f:
#             channels=json.load(f)
#         msg=''
#         check=hikari.api.Cache.get_guild_channel(hikari.api.Cache, 906917970620592178)
#         if ctx.guild_id is not None:
#             for channel in channels:
#                 if channel==str(ctx.guild_id):
#                     for key in channels[channel]:
#                         msg=str(msg)+'*'+str(hikari.impl.CacheImpl.get_guild_channel(int(key)).name)+'\n'
#         if not msg:
#             msg='No channels were added to your list.'
#         else:
#             msg='Your channels list:\n'+msg

#         await ctx.respond(msg)


# #get channels end



def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
