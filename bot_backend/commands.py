import discord
from discord.ext import commands
from discord.utils import get
from .settings import get_bot_settings
from .providers.__convert__ import convert
from .providers.exceptions import ProviderNotSupported
from .providers.__abctract__ import BaseProvider

bot = commands.Bot(command_prefix=get_bot_settings().prefix, intents=discord.Intents().all())


@bot.command()
async def start(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, {author.mention}!")


@bot.command(name="play", aliases=["p"], help="Plays a selected song from youtube/spotify/yandex music")
async def play(ctx, *args):
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


@bot.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
async def disconnect(ctx):
    if get(ctx.bot.voice_clients, guild=ctx.guild):
        await ctx.voice_client.disconnect()
    else:
        pass


@bot.command(name="join", aliases=["j"], help="Kick the bot from VC")
async def connect(ctx):
    if not get(ctx.bot.voice_clients, guild=ctx.guild):
        await ctx.author.voice.channel.connect()
    else:
        pass


@bot.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
async def queue(ctx):
    music_queue = BaseProvider.song_queue
    retval = ""
    for i in range(0, len(music_queue)):
        # display a max of 5 songs in the current queue
        if i > 4:
            retval += "\n..."
            break

        retval += music_queue[i].song_info['title'] + "\n"

    if retval != "":
        await ctx.send(retval)
    else:
        await ctx.send("No music in queue")


@bot.command(name="pause", help="Pauses the current song being played")
async def pause(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_playing():
        vc.pause()
    elif not vc:
        await ctx.send("Connect to a voice channel!")
    elif not vc.is_playing():
        pass


@bot.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
async def resume(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc and not vc.is_playing():
        vc.resume()
    elif not vc:
        await ctx.send("Connect to a voice channel!")
    elif vc.is_playing():
        pass


@bot.command(name="skip", aliases=["s"], help="Skips the current song being played")
async def skip(ctx):
    music_queue = BaseProvider.song_queue
    if get(ctx.bot.voice_clients, guild=ctx.guild):
        get(ctx.bot.voice_clients, guild=ctx.guild).stop()
        await play(ctx, music_queue[0].song_info['query'])
