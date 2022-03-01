import hikari
import lightbulb
import json
import logging
import dotenv
import os


plugin=lightbulb.Plugin('ChannelPlugin')

dotenv.load_dotenv()
LOGCHANNEL=os.getenv('LOGCHANNEL')


logging.basicConfig(filename='logs.txt',format='%(asctime)s %(name)s %(levelname)s %(message)s', filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.ERROR)


#region set channel
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.option('channel','Mention the channel in which you want to receive updates. New channel will be created if left empty.',
required=False,
type=hikari.TextableGuildChannel,
channel_types=[hikari.ChannelType.GUILD_TEXT,hikari.ChannelType.GUILD_NEWS]
)
@lightbulb.command('setchannel','sets a channel to receive new chapter notifications')
@lightbulb.implements(lightbulb.SlashCommand)
async def setchannel(ctx:lightbulb.SlashContext):
    try:
        logger.info('Set channel command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.channel_id)

        with open('channels.json','r') as f:
            channels=json.load(f)

        msgs={
            "exists":"This channel has been already added.",
            "success":"Channel setup is done. You will receive the new chapter and new announcemnt updates in the mentioned channel.\nUse `/followstory` and `/followauthor` commands to follow stories and authors"
        }

        msg=''

        channel=ctx.options.channel
        if channel:
            channel_id=channel.id
            msgs['success']=f'Channel setup is done. New chapter and new announcement updates will be shared in <#{channel_id}>.\nUse `/followstory` and `/followauthor` commands to follow stories and authors if you\'re not following any.'

        else:
            try:
                guild=ctx.get_guild()
                created_channel=await guild.create_text_channel('Wattpad-Library',topic='Channel to post new chapter links and new announcements from authors.')
                if created_channel:
                    channel_id=created_channel.id
                    msgs['success']=f'New channel is created succesfully. New chapter and new announcement updates will be shared in <#{channel_id}>.\nUse `/followstory` and `/followauthor` commands to follow stories and authors if you\'re not following any.'
                else:
                    logger.critical('something went wrong with the creation of channel', exc_info=1)
                

            except Exception as e:
                logger.fatal('Excpetion occured when sending channel msg to log server for guild Id: %s and server name: %s',guild.id,guild.name)
                msgstr=hikari.Embed(title=f'🛑Error:', description='An Error occured while creating a channel in this channel. Please try again.', color=0xFF0000)
                
                await ctx.respond(embed=msgstr)
        if not channels:
                channels[str(ctx.guild_id)]=[channel_id]
                msg=msgs['success']
        else:
            if str(ctx.guild_id) not in channels:
                    channels[str(ctx.guild_id)]=[str(channel_id)]
            else:
                for channel in channels:

                    if channel==str(ctx.guild_id) and str(channel_id) in channels[str(ctx.guild_id)]:
                        msg=msgs['exists']
                    elif channel==str(ctx.guild_id) and str(channel_id) not in channels[str(ctx.guild_id)]:
                        #channels[str(ctx.guild_id)].append(str(ctx.channel_id))
                        channels[str(ctx.guild_id)]=[(str(channel_id))]
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
        logger.critical('Exception occured in setting up a channel for guild %s',ctx.guild_id,exc_info=1)
        raise e


#endregion set channel



#region add channel
# @plugin.command
# @lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.owner_only)
# @lightbulb.command('addchannel','This channel will be added to receive new chapter notifications of your stories')
# @lightbulb.implements(lightbulb.SlashCommand)
# async def addchannel(ctx:lightbulb.SlashContext):
    # try:
    #     logger.info('Add channel command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.channel_id)
    #     msgs={
    #         "exists":"This channel has been already added.",
    #         "success":"This channel will receive new chapter notifications of your stories from now."
    #     }
    #     with open('channels.json','r') as f:
    #             channels=json.load(f)

    #     msg=''
    #     if ctx.channel_id is not None:
    #         if not channels:
    #                 channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
    #                 msg=msgs['success']
    #         else:
    #             if str(ctx.guild_id) not in channels:
    #                     channels[str(ctx.guild_id)]=[str(ctx.channel_id)]
    #             else:
    #                 for channel in channels:

    #                     if channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
    #                         msg=msgs['exists']
    #                     elif channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
    #                         channels[str(ctx.guild_id)].append(str(ctx.channel_id))
    #                         msg=msgs['success']

    #     with open('channels.json','w') as f:
    #         json.dump(channels,f,indent=2)
    #     if msg is not None:
    #         em=hikari.Embed(title='Sucess:',description=msg,color=0Xff500a)
    #         await ctx.respond(embed=em)
    #     else:
    #         emContent='Uh-oh, something is not right. Please check `/getchannels` to see if the channel is added.'
    #         emErr=hikari.Embed(f'🛑 Error:',description=f'{emContent}',color=0xFF0000)
    #         await ctx.respond(embed=emErr)

    # except Exception as e:
    #     logger.fatal('Exception has occured in addchannel command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
    #     raise e


# endregion addchannel


#region unset channel
@plugin.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(hikari.Permissions.ADMINISTRATOR)|lightbulb.checks.has_role_permissions(hikari.Permissions.MODERATE_MEMBERS)|lightbulb.checks.has_role_permissions(hikari.Permissions.MANAGE_CHANNELS)|lightbulb.owner_only)
@lightbulb.command('unsetchannel','New chapter and announcements will not be shared in any channel if you execute this command.')
@lightbulb.implements(lightbulb.SlashCommand)
async def removechannel(ctx:lightbulb.SlashContext):
    try:
        logger.info('Remove channel command has been triggered for guild %s and channel %s',ctx.guild_id,ctx.channel_id)
        with open('channels.json','r') as f:
            channels=json.load(f)

        if ctx.channel_id is not None:
            for channel in channels:
                if channel==str(ctx.guild_id):
                    if channels[str(ctx.guild_id)]:
                        channels[str(ctx.guild_id)]=[]
                        emContent='New chapter and announcment updates will no longer be shared in any channel.\nUse `/setchannel` command if you want to setup a new channel.'
                        em=hikari.Embed(title='Sucsess!',description=emContent, color=0Xff500a)

                    else:
                        emContent='Curretly no channel is setup for sharing updates. Use `/setchannel` command to setup.'
                        em=hikari.Embed(title='Empty:',description=emContent, color=0xFF0000)

                #region obselete
                # if channel==str(ctx.guild_id) and str(ctx.channel_id) not in channels[str(ctx.guild_id)]:
                #     emContent='This channel is not receiving new chapter notifications of your stories from the beginning.'
                #     em=hikari.Embed(title='Not Found:',description=emContent, color=0xFF0000)
                    
                #     await ctx.respond(embed=em)
                # elif channel==str(ctx.guild_id) and str(ctx.channel_id) in channels[str(ctx.guild_id)]:
                #     channels[str(ctx.guild_id)].remove(str(ctx.channel_id))

                #     with open('channels.json','w') as f:
                #         json.dump(channels,f,indent=2)

                    
                #     emContent='New chapter and announcment updates will no longer be shared in any channel.\nUse `/setchannel` command if you want to setup a new channel.'
                #     em=hikari.Embed(title='Sucsess!',description=emContent, color=0Xff500a)
                #endregion obselete

                    with open('channels.json','w') as f:
                        json.dump(channels,f,indent=2)

                    await ctx.respond(embed=em) 
    except Exception as e:
        logger.fatal('Exception has occured in removechannel command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
        raise e


#endregion unset channel 


#region check channels
#get channels start
@plugin.command
@lightbulb.command('checkchannels','Check in which channel the new chapter and announcement updates are being shared currently')
@lightbulb.implements(lightbulb.SlashCommand)
async def getchannels(ctx):
    try:
        logger.info('Get channels command has been triggered for guild %s and chnnel %s',ctx.guild_id,ctx.channel_id)
        with open('channels.json') as f:
            channels=json.load(f)
        msg=''
        if ctx.guild_id is not None:
            if channels:
                for channel in channels:
                    if channel==str(ctx.guild_id):
                        if not channels[channel]:
                            emContent='No channel is setup to receive updates from the bot. Use `/setchannel` command to setup a channel.'
                            em=hikari.Embed(title='Empty:',description=emContent,color=0Xff500a)
                            
                            await ctx.respond(embed=em)
                        else:
                            for key in channels[channel]:
                                msg=f'{msg}\n <#{key}>'
                            msgstr=f'Currently the new chapter and announcements are being posted in: {msg}'
                            em=hikari.Embed(title='Your channels:', description=msgstr,color=0Xff500a)
                            await ctx.respond(embed=em)

            else:
                emContent='No channel is setup to receive updates from the bot. Use `/setchannel` command to setup a channel.'
                em=hikari.Embed(title='Empty:',description=emContent,color=0Xff500a)
                            
                await ctx.respond(embed=em)

    except Exception as e:
        logger.fatal('Exception has occured in getchannels command for guild %s and channel %s',ctx.guild_id,ctx.channel_id,exc_info=1)
        raise e
        


#endregion check channels


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
