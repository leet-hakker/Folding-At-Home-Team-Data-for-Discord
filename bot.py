import discord
from discord.ext import commands
import os
import format
import foldingathome as fah
import time

team_number = 235150
channelA = 581941336580816917
channelB = 581941356780584990
channelC = 582710022128140314
bot = commands.Bot(command_prefix='fold ')
bot.remove_command('help')

@bot.command(pass_context=True)
async def leaderboard(ctx,donor=None):
    if donor:
        try:
            stats = fah.donor_stats(team_number, donor)
        except :
            await ctx.message.channel.send("Something went wrong. You may have entered an invalid donor or there may be a problem reaching Folding@Home, please try again.\nIf this has happened before, please try again later.")

        title = 'Folding@Home statistics for {}'.format(stats[0])
        description = "Donor '{}'".format(donor)
        embed = discord.Embed(title=title, description=description, color=0x4286f4)
        embed.add_field(name="Total credits for team", value=stats[1], inline=False)
        embed.add_field(name="Total work units completed for team", value=stats[2], inline=False)
        await ctx.message.channel.send(embed=embed)
    else:
        stats = fah.teamstats(team_number)
        description = 'Team {}'.format(stats["name"])
        rank = "Rank out of {}".format(stats["total_teams"])
        embed = discord.Embed(title="Folding@Home statistics", description=description, color=0x4286f4)
        embed.add_field(name="Total credits", value=str(stats["credit"]), inline=False)
        embed.add_field(name="Total work units", value=str(stats["wus"]), inline=False)
        embed.add_field(name=rank, value=str(stats["rank"]), inline=False)
        embed.add_field(name="Total number of donors", value=str(len(stats["donors"])), inline=False)
        embed.set_thumbnail(url=stats["logo"])
        await ctx.message.channel.send(ctx.message.channel, embed=embed)

@bot.event
async def on_member_join(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_remove(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_update(before, after):
    await update_count(await get_fah_stats())

async def get_fah_stats():
    team = fah.teamstats(team_number)
    highest_scorer = fah.highest_scorer(team)
    team_score = fah.team_score(team)
    team_wus = fah.team_work_units(team)

    return highest_scorer, team_score, team_wus

async def update_count(stats):
    hs, ts, twus = stats

    await bot.get_channel(channelA).edit(name=await format.convert_string(hs[0] + ' : ') + str(hs[1]))
    await bot.get_channel(channelB).edit(name=await format.convert_string('total score' + ' : ' + str(ts)))
    await bot.get_channel(channelC).edit(name=await format.convert_string('total wus' + ' : ' + str(twus)))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await update_count(await get_fah_stats())

bot.run('NTgxOTEzNjA0MDk0NDI3MTQ2.XOx7xg.831JHIIFvgmufjEuwZBuYTnIQQQ')
