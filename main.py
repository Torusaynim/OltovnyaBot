import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
import datetime


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)

# Перенести в будущем в отдельный файл по возможности
bad_words = ['дурак', 'идиот', 'лох']

stats = {}


@bot.event
async def on_ready():
    """
    Function that shows in terminal when bot is online
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Testing command

    Greet your faithful bot and he will greet you as well

    :param ctx: information about sent message
    """
    await ctx.send('Hello!')


@bot.command()
async def roll(ctx, dice: str):
    """Simulate a dice throw

    In addition to command must be added number and size of dices in NdM format,
    where N is number of dices and M is the size of dice

    :param ctx: information about sent message
    :param dice: number and size of dices in NdM format
    """
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.event
async def on_message_delete(ctx):
    """Deleted messages processing

    Called every time someone deletes message

    :param ctx: information about sent message
    """
    channel = bot.get_channel(430432809371435008)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    attachments = ctx.attachments
    if ctx.content:
        embed.add_field(name="Deleted message: ", value=ctx.content, inline=False)
    if attachments:
        embed.set_image(url=attachments[0].url)

    timeunix = (ctx.created_at - datetime.datetime(1970, 1, 1)).total_seconds()
    value = datetime.datetime.fromtimestamp(timeunix)

    embed.add_field(name="Author: ", value=str(ctx.author), inline=False)
    embed.add_field(name="Channel: ", value=str(ctx.channel), inline=False)
    embed.add_field(name="Time: ", value=value.strftime('%d.%m.%Y %H:%M:%S'), inline=False)
    await channel.send(embed=embed)
    # исправить время удаленного сообщения (добавить автора удаления сообщения)


@bot.event
async def on_message(ctx):
    """Sent messages processing

    Called every time user sends message

    :param ctx: information about sent message
    """
    flag = True
    # await ctx.add_reaction("👍")
    for word in ctx.content.lower().split():
        for restricted in bad_words:
            if word == restricted:
                await ctx.delete()
                flag = False
    if flag is True:
        if stats.get(str(ctx.author)):
            stats[str(ctx.author)] = stats[str(ctx.author)] + 1
        else:
            stats[str(ctx.author)] = 1
    await bot.process_commands(ctx)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    """Kick user from the server

    In addition to command must be added mention of a user(@UserName#0000)

    :param ctx: information about sent message
    :param user: user mention (@UserName#0000)
    """
    await ctx.guild.kick(user)


@bot.command()
async def meme(ctx):
    """Send a random image

    Images are chosen from the img folder by random

    :param ctx: information about sent message
    """
    await ctx.channel.send(file=discord.File("img\\" + random.choice(os.listdir("img"))))


@bot.command()
async def anon(ctx, *, message=""):
    """Send anon message

    Message will be sent from the bot's perspective keeping the text and all the attachments to the message

    :param ctx: information about sent message
    :param message: message text
    """
    channel = bot.get_channel(669481745435066398)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    embed.add_field(name="Anon message", value="User " + str(ctx.author.id) + ": " + message, inline=False)
    if ctx.message.attachments:
        embed.set_image(url=ctx.message.attachments[0].url)
    await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, number):
    """Delete last N messages

    In addition to the command must be added number of the messages to be deleted

    :param ctx: information about sent message
    :param number: number of messages (int)
    """
    await ctx.channel.purge(limit=int(number))


@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    """Give user specific role

    In addition to the command must be added user mention and the role mention,
    After success bot sends corresponding message

    :param ctx: information about sent message
    :param user: user mention (@UserName#0000)
    :param role: role mention (@RoleName)
    """
    await user.add_roles(role)
    await ctx.send(f"{user.name} got a role called: {role.name} by {ctx.author.name}")


@bot.command()
async def stat(ctx):
    """Text messages statistics

    Bot counts every sent message when the bot is online using on_message(ctx) function,
    this command outputs current statistics in embed window

    :param ctx: information about sent message
    """
    embed = discord.Embed(description='', colour=0xD5A6BD)
    for key, value in stats.items():
        embed.add_field(name=key + ": ", value=str(value) + " messages", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    """Make bot join voice chat

    Bot joins the current VC the caller of command sits in

    :param ctx: information about sent message
    """
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def allmute(ctx):
    """Mute all users in the voice chat

    Disables ability to speak in the voice chat for every user in the current voice chat
    (it is not necessary for the bot to be in this voice channel)

    :param ctx: information about sent message
    """
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)


@bot.command()
async def allunmute(ctx):
    """Unmute all users in the voice chat

    Returns ability to speak in the voice chat for every user in the current voice chat
    (it is not necessary for the bot to be in this voice channel)

    :param ctx: information about sent message
    """
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)


@bot.command()
async def mute(ctx, user: discord.Member):
    """Mute the specific user

    In addition to the command must be added mention of the user to disable their ability to speak in the voice chat

    :param ctx: information about sent message
    :param user: user mention (@UserName#0000)
    """
    vc = ctx.author.voice.channel
    await user.edit(mute=True)

bot.run(TOKEN)
