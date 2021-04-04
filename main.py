import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>')


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
    channel = bot.get_channel(827903072667041802)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    attachments = message.attachments
    if message.content:
        embed.add_field(name="Deleted message: ", value=message.content, inline=False)
    if attachments:
        embed.set_image(url=attachments[0].url)

    embed.add_field(name="Author: ", value=str(message.author), inline=False)
    await channel.send(embed=embed)
    # добавить время удаленного сообщения (а еще кто удалил)


@bot.event
async def on_message(message):
    if message.content == 'vitali4':  # сделать через список
        await message.delete()
    await bot.process_commands(message)


@bot.command()
async def kick(ctx, user: discord.Member):
    await ctx.guild.kick(user)


@bot.command()
async def meme(message):
    await message.channel.send(file=discord.File("img\\" + random.choice(os.listdir("img"))))


@bot.command()
async def PM(ctx, *, message=None):
    channel = bot.get_channel(827903072667041802)
    await channel.send("User "+str(ctx.author.id)+" said: "+message)


@bot.command()
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number))


@bot.command()
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name} got a role called: {role.name} by {ctx.author.name}")


bot.run(TOKEN)
