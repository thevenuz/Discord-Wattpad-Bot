import hikari
import lightbulb
import json

plugin=lightbulb.Plugin('ChannelPlugin')

#TODO later: define permissions in a single place and use them in all plugins
#permissions
@lightbulb.Check
def is_AdminOrMod(ctx):
    roles=ctx.member.get_roles()
    if any(role.permissions.all(hikari.Permissions.ADMINISTRATOR) for role in roles) or any(role.permissions.all(hikari.Permissions.MODERATE_MEMBERS) for role in roles):
        return True

    return False

#permissions

#addchannel command start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('addchannel','This channel will be added to receive new chapter notifications of your stories')
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

                    if channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                        await ctx.respond('This channel has been already added.')
                    elif channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                        channels[str(ctx.guild_id)].append(str(ctx.channel_id))

                        with open('channels.json','w') as f:
                            json.dump(channels,f,indent=2)

                        await ctx.respond('This channel will receive new chapter notifications of your stories from now.')


#addchannel command end

#remove channel start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('removechannel','This channel will be removed from receiving new chapter notifications of your stories')
@lightbulb.implements(lightbulb.SlashCommand)
async def removechannel(ctx):
    with open('channels.json','r') as f:
        channels=json.load(f)

    if ctx.channel_id is not None:
        for channel in channels:
            if channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                await ctx.respond('This channel is not receiving new chapter notifications of your stories from the beginning.')
            elif channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                channels[str(ctx.guild_id)].remove(str(ctx.channel_id))

                with open('channels.json','w') as f:
                    json.dump(channels,f,indent=2)

                await ctx.respond('This channel will not receive new chapter notifications from now.')


#remove channel end

#get channels start
@plugin.command
@lightbulb.add_checks(is_AdminOrMod)
@lightbulb.command('getchannels','Gives your server\'s channels that are currently receiving new chapter updates')
@lightbulb.implements(lightbulb.SlashCommand)
async def getchannels(ctx):
        with open('channels.json') as f:
            channels=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            for channel in channels:
                if channel==str(ctx.guild_id):
                    if not channels[channel]:
                        await ctx.respond('No channels in this server are receiving new chapter notifications.')
                    else:
                        for key in channels[channel]:
                            msg=f'{msg}\n <#{key}>'
                        await ctx.respond(f'Channels in this server that are receiving new chapter notifications:\n{msg}')
        


#get channels end


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
