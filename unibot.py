#unibot v1.1 by G_bby
import discord
from discord.ext import commands
from discord.utils import get
import trials, member_plus
import key #key.py contains the line: KEY = (discord bot client_id)
import os
#intents = discord.Intents()
#intents.members = True
#client = commands.Bot(command_prefix="$", intents =intents)
client = commands.Bot(command_prefix="$")

admin_apps_channelid = 791665220279074835
admin_upload_queue_channelid = 797196680435990550
moderation_log_channelid = 797196806172835891
announcement_channelid = 784865866865049610
muted_roleid = 745010908761161739
admin_role_tag = "<@&791663054940012565>"

userrolename = "User"

client_id=key.KEY

if not os.path.exists(trials.TRIALFILE):
    with open(trials.TRIALFILE, 'w') as trial_db:
        trial_db.write("[]")

@client.event
async def on_ready():
    print("Bot is ready")

#@client.event
#async def on_member_join(member):
#    print(str(member) + " has joined the discord")
#    user_role = get(member.guild.roles, name=userrolename)
#    await member.add_roles(user_role)

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount+1)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason="an unspecified reason"):
    await client.get_channel(moderation_log_channelid).send(str(member) + " has been kicked for " + reason + " by " + str(ctx.author))
    try:
        await member.send("You have been kicked from Universe Editing for " + reason)
        await member.kick(reason=reason)
    except discord.errors.Forbidden:
        print("failed to message user")
        await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason="an unspecified reason"):
    await client.get_channel(moderation_log_channelid).send(str(member) + " has been banned for " + reason + " by " + str(ctx.author))
    try:
        await member.send("You have been banned from Universe Editing for " + reason)
        await member.ban(reason=reason)
    except discord.errors.Forbidden:
        print("failed to message user")
        await member.ban(reason=reason)

@client.command(aliases=['p'])
async def promote(ctx, member : discord.Member, role):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    trial_role = discord.utils.get(ctx.guild.roles, name="Trial")
    member_role = discord.utils.get(ctx.guild.roles, name="Member")
    member_plus_role = discord.utils.get(ctx.guild.roles, name="Member+")
    if admin_role in ctx.author.roles:
        if role == "Trial":
            if trial_role in member.roles:
                await ctx.channel.send("User Trial has been renewed")
                error = trials.renewTrial(member.mention)
            elif member_role in member.roles:
                await ctx.channel.send("User is already Member")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                error = trials.newTrial(member.mention)
                await member.add_roles(trial_role)
        elif role == "Member":
            if member_role in member.roles:
                await ctx.channel.send("User is already Member")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                if trial_role in member.roles:
                    error = trials.removeTrial(member.mention)
                    await member.remove_roles(trial_role)
                await member.add_roles(member_role)
        elif role == "Member+":
            if member_plus_role in member.roles:
                error = member_plus.newMemberPlus(member.mention)
                await ctx.channel.send("User is already Member+")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                if trial_role in member.roles:
                    error = trials.removeTrial(member.mention)
                    await member.remove_roles(trial_role)
                if member_role not in member.roles:
                    await member.add_roles(member_role)
                await member.add_roles(member_plus_role)
                error = member_plus.newMemberPlus(member.mention)

@client.command(aliases = ['expire'])
async def expiretrials(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        expired = trials.purgeTrials()

    message = "The trial status for "
    for trial in expired:
        message += trial['userid'] + " "
    message += "has expired. [remove role manually]"
    await ctx.channel.send(message)

@client.command(aliases = ['check'])
async def checktrial(ctx):
    trial = trials.getTrial(ctx.author.mention)
    if trial['userid'] != "NOT_FOUND":
        await ctx.channel.send("Your trial expires at " + trial['expiration'] + " PST")
    else:
        await ctx.channel.send("Only trials that became trial after 2021-04-13 can use this command")

@client.command(aliases = ['us'])
async def updateSocials(ctx, *, links):
    member_plus_role = discord.utils.get(ctx.guild.roles, name="Member+")
    if member_plus_role in ctx.author.roles:
        memberplus = member_plus.updateSocials(ctx.author.mention, links)
        if memberplus['userid'] != "NOT_FOUND":
            await ctx.channel.send("Your socials have been updated in the database")
        else:
            await ctx.channel.send("Only Member+ can use this command")

@client.command()
async def clearSocials(ctx, userid):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        memberplus = member_plus.updateSocials(userid, "")
        if memberplus['userid'] != "NOT_FOUND":
            await ctx.channel.send("This user's socials have been cleared")
        else:
            await ctx.channel.send("This user is not in the database")
    else:
        await ctx.channel.send("Only Admin can use this command")

@client.command(aliases = ['upname'])
async def updateMemPlusName(ctx, name):
    if member_plus.nameTaken(name):
            await ctx.channel.send("Name is already in use")
    else:
        memberplus = member_plus.updateName(ctx.author.mention, name)
        if memberplus['userid'] != "NOT_FOUND":
            await ctx.channel.send("Name has been updated in the database")
        else:
            await ctx.channel.send("Only Member+ can use this command")

@client.command(aliases = ['s'])
async def socials(ctx, name):
    if member_plus.getSocials(name) != "":
        await ctx.channel.send(member_plus.getSocials(name))
    else:
        await ctx.channel.send("This user has no socials in the database")


@client.command(aliases=['q'])
async def queue(ctx, *, link):
    if str(ctx.channel) == "✅ready-to-upload-✅":
        trial_role = discord.utils.get(ctx.guild.roles, name="Trial")
        member_role = discord.utils.get(ctx.guild.roles, name="Member")
        if trial_role in ctx.author.roles or member_role in ctx.author.roles:
            await client.get_channel(admin_upload_queue_channelid).send(ctx.author.mention + " has queued an edit for upload: " + link)
            await ctx.channel.send("Your upload has been queued.")


@client.command(aliases = ['m'])
async def mute(ctx,member : discord.Member, *, reason="an unspecified reason"):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        await client.get_channel(moderation_log_channelid).send(str(member) + " has been muted for " + reason + " by " + str(ctx.author))
        muted_role = ctx.guild.get_role(muted_roleid)
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(member.mention + " has been muted for " + reason)

@client.command(aliases = ['um'])
async def unmute(ctx,member : discord.Member):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        await client.get_channel(moderation_log_channelid).send(str(member) + " has been unmuted by " + str(ctx.author))
        muted_role = ctx.guild.get_role(muted_roleid)
        await member.remove_roles(muted_role)

@client.command(aliases = ['paste'])
async def plugins(ctx):
    await ctx.channel.send("***REMOVED***")

@client.command(aliases=['luma'])
async def lumamatte(ctx):
    await ctx.channel.send("https://cdn.discordapp.com/attachments/794306658067021835/794592965917802506/lumamattev2.zip")
    await ctx.channel.send("https://cdn.discordapp.com/attachments/754027452757704876/790472565965586442/How_to_use_a_luma_matte.mp4")

@client.command(aliases=['velo'])
async def velocity(ctx):
    await ctx.channel.send("https://www.youtube.com/watch?v=sqyFfIeSIH0")

@client.command(aliases=['dof'])
async def depth(ctx):
    await ctx.channel.send("https://youtu.be/YXaAXfaLaHs")
    await ctx.channel.send("https://youtu.be/tqbtDHLIjbc")

@client.command(aliases=['fovoptions'])
async def mcfov(ctx, fov=70):
    if fov < 360:
        optionfov=(int(fov)-70)/40
        await ctx.channel.send("for an fov of " + str(fov) + " set your fov to " + str(optionfov) + " in your options.txt file")

@client.command(aliases=['svs'])
async def smoothvsharp(ctx):
    await ctx.channel.send("https://cdn.discordapp.com/attachments/754027452757704876/776347188245692426/Smooth_vs_Sharp_Velo.mp4")

@client.command(aliases=['replay'])
async def replaytutorial(ctx):
    await ctx.channel.send("https://www.youtube.com/watch?v=8QcqgWa7kOU")
    await ctx.channel.send("https://www.youtube.com/watch?v=mTIRr-zyKIE")

@client.command(aliases=['rpmdl'])
async def replaydownload(ctx):
    await ctx.channel.send("https://www.replaymod.com/download/")

@client.command()
async def ffmpeg(ctx):
    await ctx.channel.send("https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z [FFMPEG Download Link]\nGraphics by OE9:\nhttps://cdn.discordapp.com/attachments/760554084443881501/806535764728217640/Installing_FFMPEG_Correctly.png\nhttps://cdn.discordapp.com/attachments/760554084443881501/806541250118418492/Easier_Way_to_install_FFMPEG.png")

@client.command(aliases=['intros'])
async def logos(ctx):
    await ctx.channel.send("https://drive.google.com/drive/folders/1_wtStjgu_dSh4gpZ2NrhfX-tAIdeddxk?usp=sharing")

@client.command(aliases=['app'])
async def apply(ctx):
    await ctx.channel.send("https://docs.google.com/forms/d/e/1FAIpQLSe3fRMRnGKoW-e02Z3ryvWPvhdTxUAqNZQBYKx7ktcRedQR7A/viewform")

@client.command(aliases=['r2r'])
async def ratiotoresolutions(ctx, w=16, h=9):
    ratio = int(w) / int(h)
    if ratio < 6:
        hd = 1280/ratio
        fhd = 1920/ratio
        wqhd = 2560/ratio
        uhd = 3840/ratio
        eightkuhd = 7680/ratio
        await ctx.channel.send("Some resolutions in " + str(w) + ":" + str(h) + "\n" + "1280x" + str(round(hd)) + "\n1920x" + str(round(fhd)) +
          "\n2560x" + str(round(wqhd)) + "\n3840x" + str(round(uhd)) + "\n7680x" +
          str(round(eightkuhd)))

@client.command(aliases=['h'])
async def unibothelp(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    member_role = discord.utils.get(ctx.guild.roles, name="Member")
    trial_role = discord.utils.get(ctx.guild.roles, name="Trial")
    await ctx.channel.send("---Uni-Bot-Commands---\n"
                           "$velo -- sends the t3c velocity tutorial\n"
                           "$plugins or $paste -- sends the plugins pastebin\n"
                           "$app <link> -- sends in an application to Uni (only works in apps channel)")

    if member_role in ctx.author.roles or trial_role in ctx.author.roles:
        await ctx.channel.send("---Member/Trial-Commands---\n"
                               "$queue <links> or $q <links> -- submits an edit to be uploaded to Uni channel (only works in submit-uploads channel)")

    if admin_role in ctx.author.roles:
        await ctx.channel.send("---Admin-Commands---\n"
                               "$clear <number> or $c <number> -- deletes the last <number> messages from current channel\n"
                               "$kick @user <reason> or $k @user <reason> -- kicks a user for a reason\n"
                               "$ban @user <reason> or $b @user <reason> -- bans a user for a reason\n"
                               "$mute @user <reason> or $m @user <reason> -- mutes a user for a reason\n"
                               "$unmute @user or $um @user -- unmutes a user\n"
                               "$promote @user <Trial/Member/Member+> or $p @user <Trial/Member/Member+> -- promotes a user to specified role")

@client.command()
async def ping(ctx):
    await ctx.channel.send("Pong.")

@clear.error
async  def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        print("someone tried to run clear without permissions")

@apply.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send("Usage: $app <link>")


@kick.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: $k @user")
    if isinstance(error, commands.errors.MissingPermissions):
        print("kick command failed")
    if isinstance(error, commands.errors.CommandInvokeError):
        print("kick command failed")

@ban.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: $b @user")
    if isinstance(error, commands.errors.MissingPermissions):
        print("ban command failed")
    if isinstance(error, commands.errors.CommandInvokeError):
        print("ban command failed")

@mute.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: $m @user")
    if isinstance(error, commands.errors.MissingPermissions):
        print("mute command failed")
    if isinstance(error, commands.errors.CommandInvokeError):
        print("mute command failed")

@unmute.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: $m @user")
    if isinstance(error, commands.errors.MissingPermissions):
        print("unmute command failed")
    if isinstance(error, commands.errors.CommandInvokeError):
        print("unmute command failed")

@queue.error
async def info_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: $q <links>")

client.run(client_id)
