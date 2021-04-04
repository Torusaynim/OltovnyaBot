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
    await channel.send("Deleted message: " + message.content + "\nAuthor: " + str(message.author))
    # добавить время удаленного сообщения


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
    await message.channel.send(file=discord.File("D:\Python\DiscordBot\img\\"+random.choice(os.listdir("D:\Python\DiscordBot\img"))))


bot.run(TOKEN)