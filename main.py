import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv


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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(430432809371435008)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    attachments = message.attachments
    if message.content:
        embed.add_field(name="Deleted message: ", value=message.content, inline=False)
    if attachments:
        embed.set_image(url=attachments[0].url)

    embed.add_field(name="Author: ", value=str(message.author), inline=False)
    embed.add_field(name="Channel: ", value=str(message.channel), inline=False)
    embed.add_field(name="Time: ", value=str(message.created_at) + ", UMT", inline=False)
    await channel.send(embed=embed)
    # исправить время удаленного сообщения (добавить автора удаления сообщения)


@bot.event
async def on_message(message):
    flag = True
    for word in message.content.lower().split():
        for restricted in bad_words:
            if word == restricted:
                await message.delete()
                flag = False
    if flag is True:
        if stats.get(str(message.author)):
            stats[str(message.author)] = stats[str(message.author)] + 1
        else:
            stats[str(message.author)] = 1
    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    await ctx.guild.kick(user)


@bot.command()
async def meme(message):
    await message.channel.send(file=discord.File("img\\" + random.choice(os.listdir("img"))))


@bot.command()
async def PM(ctx, *, message=""):
    channel = bot.get_channel(669481745435066398)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    embed.add_field(name="Anon message", value="User " + str(ctx.author.id) + ": " + message, inline=False)
    if ctx.message.attachments:
        embed.set_image(url=ctx.message.attachments[0].url)
    await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number))


@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name} got a role called: {role.name} by {ctx.author.name}")


@bot.command()
async def stat(ctx):
    embed = discord.Embed(description='', colour=0xD5A6BD)
    for key, value in stats.items():
        embed.add_field(name=key + ": ", value=str(value) + " messages", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def allmute(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)


@bot.command()
async def allunmute(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)


@bot.command()
async def mute(ctx, user: discord.Member):
    vc = ctx.author.voice.channel
    await user.edit(mute=True)

bot.run(TOKEN)
