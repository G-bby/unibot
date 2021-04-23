#unibot v1.1 by G_bby
import discord
from discord.ext import commands
from discord.utils import get
import trials, member_plus, roster
import secrets #secrets.py contains the line: KEY = (discord bot client_id) and PASTE = (link to pastebin)
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

client_id=secrets.KEY

def fixuid(userid):
    return userid.replace('!', '')

#create databases if they don't exist
if not os.path.exists(trials.TRIALFILE):
    with open(trials.TRIALFILE, 'w') as trial_db:
        trial_db.write("[]")

if not os.path.exists(member_plus.MEMBERPLUSFILE):
    with open(member_plus.MEMBERPLUSFILE, 'w') as memplus_db:
        memplus_db.write("[]")

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
                error = trials.renewTrial(fixuid(member.mention))
                error = roster.updateRank(fixuid(member.mention), "Trial")
            elif member_role in member.roles:
                await ctx.channel.send("User is already Member")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                error = trials.newTrial(fixuid(member.mention)) #add to trial database
                error = roster.updateRank(fixuid(member.mention), "Trial")
                await member.add_roles(trial_role)
        elif role == "Member":
            if member_role in member.roles:
                await ctx.channel.send("User is already Member")
                error = roster.updateRank(fixuid(member.mention), "Member")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                if trial_role in member.roles:
                    error = trials.removeTrial(fixuid(member.mention))
                    await member.remove_roles(trial_role)
                    # remove user from trial database
                    trials.removeTrial(fixuid(member.mention))
                await member.add_roles(member_role)
                error = roster.updateRank(fixuid(member.mention), "Member")
        elif role == "Member+":
            if member_plus_role in member.roles:
                error = member_plus.newMemberPlus(fixuid(member.mention))
                error = roster.updateRank(fixuid(member.mention), "Member+")
                await ctx.channel.send("User is already Member+")
            else:
                #await client.get_channel(announcement_channelid).send(member.mention + "has been promoted to " + role + "!")
                if trial_role in member.roles:
                    error = trials.removeTrial(fixuid(member.mention))
                    await member.remove_roles(trial_role)
                    # remove user from trial database
                    trials.removeTrial(fixuid(member.mention))
                if member_role not in member.roles:
                    await member.add_roles(member_role)
                await member.add_roles(member_plus_role)
                error = member_plus.newMemberPlus(fixuid(member.mention))
                error = roster.updateRank(fixuid(member.mention), "Member+")

                #pull name from roster database if available
                name = roster.getName(fixuid(member.mention))
                if name != "NOT-FOUND":
                    error = member_plus.updateName(fixuid(member.mention), name)

@client.command(aliases=['rosteradd'])
async def addtoroster(ctx, member : discord.Member, rank):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        try:
            error = roster.updateRank(fixuid(member.mention), rank)
        except Exception as e:
            print(e)

@client.command(aliases =['rosterremove'])
async def removefromroster(ctx, member : discord.Member):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        error = roster.remove(fixuid(member.mention))

@client.command(aliases = ['youtube'])
async def updateyoutube(ctx, link):
    error = roster.updateYouTube(fixuid(ctx.author.mention), link)
    if error == 1:
        await ctx.channel.send("Youtube link updated!")
    elif error == -3:
        await ctx.channel.send("Only Trials and above can use this command")
    elif error == -4:
        await ctx.channel.send("Invalid youtube link")


@client.command(aliases =['uproster'])
async def updateRoster(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        rosterlist = roster.getRoster()
        rTrials = []
        rMembers = []
        rMemberPluses = []
        rAdmins = []
        rOwners = []

        for person in rosterlist:
            if person.get('rank') == "Trial":
                rTrials.append(person)
            elif person.get('rank') == "Member":
                rMembers.append(person)
            elif person.get('rank') == "Member+":
                rMemberPluses.append(person)
            elif person.get('rank') == "Admin":
                rAdmins.append(person)
            elif person.get('rank') == "Owner":
                rOwners.append(person)
            else:
                print("user has invalid rank value\n")

        mOwners = ""
        mAdmins = ""
        mMemberPluses = ""
        mMembers = ""
        mTrials = ""

        #print change name message
        await ctx.channel.send("If you do not want to be tagged in further roster messages please use $upname <name> to change your name")

        #print Owners
        mOwners += "** ----------------**\n:red_circle: **OWNERS** :red_circle:\n** ----------------**\n"

        for owner in rOwners:
            if len(mOwners) + len("***" + owner.get('name') + "***\n" + "<" + owner.get('youtube') + ">\n\n") < 2000:
                mOwners += "***" + owner.get('name') + "***\n" + "<" + owner.get('youtube') + ">\n\n"
            else:
                await ctx.channel.send(mOwners)
                mOwners = "***" + owner.get('name') + "***\n" + "<" + owner.get('youtube') + ">\n\n"
        await ctx.channel.send(mOwners)

        # print Admins
        mAdmins += "** ----------------**\n:red_circle: **ADMINS** :red_circle:\n** ----------------**\n"

        for admin in rAdmins:
            if len(mAdmins) + len("***" + admin.get('name') + "***\n" + "<" + admin.get('youtube') + ">\n\n") < 2000:
                mAdmins += "***" + admin.get('name') + "***\n" + "<" + admin.get('youtube') + ">\n\n"
            else:
                await ctx.channel.send(mAdmins)
                mAdmins = "***" + admin.get('name') + "***\n" + "<" + admin.get('youtube') + ">\n\n"
        await ctx.channel.send(mAdmins)

        # print Member Pluses
        mMemberPluses += "** ----------------**\n:green_circle: **MEMBERS+** :green_circle:\n** ----------------**\n"

        for memberplus in rMemberPluses:
            if len(mMemberPluses) + len("***" + memberplus.get('name') + "***\n" + "<" + memberplus.get('youtube') + ">\n\n") < 2000:
                mMemberPluses += "***" + memberplus.get('name') + "***\n" + "<" + memberplus.get('youtube') + ">\n\n"
            else:
                await ctx.channel.send(mMemberPluses)
                mMemberPluses = "***" + memberplus.get('name') + "***\n" + "<" + memberplus.get('youtube') + ">\n\n"
        await ctx.channel.send(mMemberPluses)

        # print Members
        mMembers += "** ----------------**\n:blue_circle: **MEMBERS** :blue_circle:\n** ----------------**\n"

        for member in rMembers:
            if len(mMembers) + len(
                    "***" + member.get('name') + "***\n" + "<" + member.get('youtube') + ">\n\n") < 2000:
                mMembers += "***" + member.get('name') + "***\n" + "<" + member.get('youtube') + ">\n\n"
            else:
                await ctx.channel.send(mMembers)
                mMembers = "***" + member.get('name') + "***\n" + "<" + member.get('youtube') + ">\n\n"
        await ctx.channel.send(mMembers)

        # print Trials
        mTrials += "** ----------------**\n:yellow_circle: **TRIALS** :yellow_circle:\n** ----------------**\n"

        for trial in rTrials:
            if len(mTrials) + len(
                    "***" + trial.get('name') + "***\n" + "<" + trial.get('youtube') + ">\n\n") < 2000:
                mTrials += "***" + trial.get('name') + "***\n" + "<" + trial.get('youtube') + ">\n\n"
            else:
                await ctx.channel.send(mTrials)
                mTrials = "***" + trial.get('name') + "***\n" + "<" + trial.get('youtube') + ">\n\n"
        await ctx.channel.send(mTrials)


@client.command(aliases = ['expire'])
async def expiretrials(ctx):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        expired = trials.purgeTrials()
        if len(expired) > 0:
            message = "The trial status for "
            for trial in expired:
                message += trial['userid'] + " "
                error = roster.updateRank(trial['userid'], "Expired")
            message += "has expired. [remove role manually]"
        else:
            message = "No trials have expired"
        await ctx.channel.send(message)

@client.command(aliases = ['check'])
async def checktrial(ctx, *, member : discord.Member = "test"):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    if admin_role in ctx.author.roles:
        trial = trials.getTrial(fixuid(member.mention))
        if trial['userid'] != "NOT_FOUND":
            await ctx.channel.send("User's trial expires at " + trial['expiration'])
        else:
            await ctx.channel.send("User is not trial")
    else:
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
async def updateName(ctx, *, name):
    member_plus_role = discord.utils.get(ctx.guild.roles, name="Member+")
    if member_plus.nameTaken(name) or roster.nameTaken(name) or name.__contains__(" "):
        await ctx.channel.send("Name is already in use or contains a space")
    else:
        person = roster.updateName(ctx.author.mention, name)
        if person['userid'] != "NOT_FOUND":
            await ctx.channel.send("Name has been updated in the roster database")
        else:
            await ctx.channel.send("Only Trials, Members, and Member+ can use this command")

        # update mem+ name
        if member_plus_role in ctx.author.roles:
                memberplus = member_plus.updateName(ctx.author.mention, name)
                if memberplus['userid'] != "NOT_FOUND":
                    await ctx.channel.send("Name has been updated in the Member+ database")
                else:
                    await ctx.channel.send("You are not in the Member+ database")

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
    await ctx.channel.send(secrets.PASTE)

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
    await ctx.channel.send("Documentation for UniBot is now on GitHub: https://github.com/G-bby/unibot")

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
        await ctx.send("Usage: $app")


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
