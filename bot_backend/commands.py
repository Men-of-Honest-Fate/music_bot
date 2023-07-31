import discord
from discord.ext import commands

from .settings import get_bot_settings
from .providers.__convert__ import convert
from .providers.exceptions import ProviderNotSupported

settings = get_bot_settings()

bot = commands.Bot(command_prefix=settings.prefix, intents=discord.Intents().all())


class Commands(commands.Cog):

    @bot.command()
    async def start(self, ctx):
        author = ctx.message.author
        await ctx.send(f"Привет, {author.mention}!")

    @bot.command(name="play", aliases=["p"], help="Plays a selected song from youtube/spotify/yandex music")
    async def play(self, ctx, *args):
        query = " ".join(args)
        provider = ''
        if "yandex.ru" in query:
            provider = "yandex"
        elif "youtube.com" in query:
            provider = "youtube"
        elif "spotify" in query:
            provider = "spotify"

        try:
            provider = convert(provider)
        except ProviderNotSupported:
            await ctx.send("Сервис не поддерживается")

        await provider.play(ctx, query)

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def leave(self, ctx, *args):
        pass
