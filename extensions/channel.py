import hikari
import lightbulb
import json
import logging

plugin=lightbulb.Plugin('ChannelPlugin')


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)



#addchannel command start
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.owner_only)
@lightbulb.command('addchannel','This channel will be added to receive new chapter notifications of your stories')
@lightbulb.implements(lightbulb.SlashCommand)
async def addchannel(ctx:lightbulb.SlashContext):
    try:
        logger.info('Add channel command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.channel_id)
        msgs={
            "exists":"This channel has been already added.",
            "success":"This channel will receive new chapter notifications of your stories from now."
        }
        with open('channels.json','r') as f:
                channels=json.load(f)

        msg=''
        if ctx.channel_id is not None:
            if not channels:
                    channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
                    msg=msgs['success']
            else:
                if str(ctx.guild_id) not in channels:
                        channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
                else:
                    for channel in channels:

                        if channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                            msg=msgs['exists']
                        elif channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                            channels[str(ctx.guild_id)].append(str(ctx.channel_id))
                            msg=msgs['success']

        with open('channels.json','w') as f:
            json.dump(channels,f,indent=2)
        if msg is not None:
            em=hikari.Embed(title='Sucess:',description=msg,color=0Xff500a)
            await ctx.respond(embed=em)
        else:
            emContent='Uh-oh, something is not right. Please check `/getchannels` to see if the channel is added.'
            emErr=hikari.Embed(f'🛑 Error:',description=f'{emContent}',color=0xFF0000)
            await ctx.respond(embed=emErr)

    except Exception as e:
        logger.fatal('Exception has occured in addchannel command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
        raise e


#addchannel command end

#remove channel start
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.owner_only)
@lightbulb.command('removechannel','This channel will be removed from receiving new chapter notifications of your stories')
@lightbulb.implements(lightbulb.SlashCommand)
async def removechannel(ctx:lightbulb.SlashContext):
    try:
        logger.info('Remove channel command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.channel_id)
        with open('channels.json','r') as f:
            channels=json.load(f)

        if ctx.channel_id is not None:
            for channel in channels:
                if channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                    emContent='This channel is not receiving new chapter notifications of your stories from the beginning.'
                    em=hikari.Embed(title='Not Found:',description=emContent, color=0xFF0000)
                    
                    await ctx.respond(embed=em)
                elif channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                    channels[str(ctx.guild_id)].remove(str(ctx.channel_id))

                    with open('channels.json','w') as f:
                        json.dump(channels,f,indent=2)

                    
                    emContent='This channel will not receive new chapter notifications from now.'
                    em=hikari.Embed(title='Sucsess!',description=emContent, color=0Xff500a)

                    await ctx.respond(embed=em) 
    except Exception as e:
        logger.fatal('Exception has occured in removechannel command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
        raise e


#remove channel end

#get channels start
@plugin.command
@lightbulb.command('getchannels','Gives your server\'s channels that are currently receiving new chapter updates')
@lightbulb.implements(lightbulb.SlashCommand)
async def getchannels(ctx):
    try:
        logger.info('Get channels command has been triggered for guild %s and chnnel %s',ctx.guild_id,ctx.channel_id)
        with open('channels.json') as f:
            channels=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            for channel in channels:
                if channel==str(ctx.guild_id):
                    if not channels[channel]:
                        emContent='No channels in this server are receiving new chapter notifications.'
                        em=hikari.Embed(title='Empty:',description=emContent,color=0Xff500a)
                        
                        await ctx.respond(embed=em)
                    else:
                        for key in channels[channel]:
                            msg=f'{msg}\n <#{key}>'
                        
                        em=hikari.Embed(title='Channels in this server that are receiving new chapter notifications:', description=msg,color=0Xff500a)
                        await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in getchannels command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
        raise e
        


#get channels end


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
