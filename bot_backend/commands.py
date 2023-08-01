import discord
from discord.ext import commands
from discord.utils import get

from bot_backend.providers.__abctract__ import BaseProvider
from bot_backend.providers.__convert__ import convert
from bot_backend.providers.exceptions import ProviderNotSupported
from bot_backend.settings import get_bot_settings

bot = commands.Bot(
    command_prefix=get_bot_settings().prefix, intents=discord.Intents().all()
)


@bot.command()
async def start(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет, {author.mention}!")


@bot.command(
    name="play",
    aliases=["p"],
    help="Играет выбранную композицию/плейлист из Youtube/Spotify/Яндекс Музыки",
)
async def play(ctx, *args):
    query = " ".join(args)
    provider = ""
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


@bot.command(
    name="leave",
    aliases=["disconnect", "l", "d"],
    help="Отключится от голосового канала",
)
async def disconnect(ctx):
    if get(ctx.bot.voice_clients, guild=ctx.guild):
        await ctx.voice_client.disconnect()
    else:
        pass


@bot.command(name="join", aliases=["j"], help="Подключиться к голосовому каналу")
async def connect(ctx):
    if not get(ctx.bot.voice_clients, guild=ctx.guild):
        await ctx.author.voice.channel.connect()
    else:
        pass


@bot.command(name="queue", aliases=["q"], help="Отобразить очередь треков")
async def queue(ctx):
    music_queue = BaseProvider.song_queue
    retval = ""
    for i in range(0, len(music_queue)):
        # display a max of 5 songs in the current queue
        if i > 4:
            retval += "\n..."
            break

        retval += music_queue[i].song_info["title"] + "\n"

    if retval != "":
        await ctx.send(retval)
    else:
        await ctx.send("No music in queue")


@bot.command(name="pause", help="Ставит на паузу текущую композицию")
async def pause(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_playing():
        vc.pause()
    elif not vc:
        await ctx.send("Connect to a voice channel!")
    elif not vc.is_playing():
        pass


@bot.command(
    name="resume", aliases=["r"], help="Продолжает проигрывание текущей композиции"
)
async def resume(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc and not vc.is_playing():
        vc.resume()
    elif not vc:
        await ctx.send("Connect to a voice channel!")
    elif vc.is_playing():
        pass


@bot.command(
    name="skip",
    aliases=["s"],
    help="Пропускает текущую композицию и переходит к следующей",
)
async def skip(ctx):
    music_queue = BaseProvider.song_queue
    if get(ctx.bot.voice_clients, guild=ctx.guild):
        get(ctx.bot.voice_clients, guild=ctx.guild).stop()
        await play(ctx, music_queue[0].song_info["query"])
