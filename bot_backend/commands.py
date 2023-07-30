import discord
from discord.ext import commands

from ..settings import get_bot_settings

settings = get_bot_settings()

bot = commands.Bot(command_prefix=settings.prefix, intents=discord.Intents().all())


@bot.command()
async def start(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, {author.mention}!")
