import discord
from discord.utils import get
from youtube_dl import YoutubeDL

from bot_backend.models.songs import BaseSong
from bot_backend.settings import get_mpeg_settings, get_youtube_settings

from .__abctract__ import BaseProvider


class Youtube(BaseProvider, BaseSong):
    vc = None
    is_playing: bool = False
    is_paused: bool = False
    is_looped: bool = False
    music_queue = []

    def __init__(self):
        self.settings: dict = get_youtube_settings().__dict__()
        self.ctx = None
        self.ffmpeg_settings: dict = get_mpeg_settings().__dict__()

    async def parce(self, item):
        with YoutubeDL(self.settings) as ydl:
            if "https" in item:
                try:
                    info = ydl.extract_info(item, download=False)
                except:
                    return False
            else:
                try:
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)[
                        "entries"
                    ][0]
                except:
                    return False

        return {
            "source": info["formats"][0]["url"],
            "title": info["title"],
            "query": item,
        }

    def play_next(self):
        if len(self.song_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.song_queue[0].song_info["source"]

            # remove the first element as you are currently playing it
            self.song_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.ffmpeg_settings),
                after=lambda e: self.play_next(),
            )
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, ctx):
        self.is_playing = True
        if len(self.song_queue) > 0:
            m_url = self.song_queue[0].song_info["source"]

            # try to connect to voice channel if you are not already connected
            if get(ctx.bot.voice_clients, guild=ctx.guild) is None:
                self.vc = await self.song_queue[0].voice_channel.connect()

                # in case we fail to connect
                if self.vc is None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                self.vc = get(ctx.bot.voice_clients, guild=ctx.guild)
                await self.vc.move_to(self.song_queue[0].voice_channel)

            # remove the first element as you are currently playing it
            self.song_queue.pop(0)
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.ffmpeg_settings),
                after=lambda e: self.play_next(),
            )
        else:
            self.is_playing = False

    async def play(self, ctx, *args):
        query = " ".join(args)
        try:
            self.voice_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("Connect to a voice channel!")
        if self.voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            self.song = await self.parce(query)
            if type(self.song) == type(True):
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist "
                    "or a livestream format."
                )
            else:
                await ctx.send("Song added to the queue")
                song = BaseSong()
                song.song_info = self.song
                song.voice_channel = self.voice_channel
                self.song_queue.append(song)
                if (
                    not get(ctx.bot.voice_clients, guild=ctx.guild)
                    or not get(ctx.bot.voice_clients, guild=ctx.guild).is_playing()
                ):
                    await self.play_music(ctx)

    async def skip(self, ctx):
        if get(ctx.bot.voice_clients, guild=ctx.guild):
            get(ctx.bot.voice_clients, guild=ctx.guild).stop()
            # try to play next in the queue if it exists
            await self.play_music(ctx)

    async def clear(self, ctx):
        if (
            get(ctx.bot.voice_clients, guild=ctx.guild) is not None
            and get(ctx.bot.voice_clients, guild=ctx.guild).is_playing()
        ):
            self.vc.stop()
        self.song_queue = []
        await ctx.send("Music queue cleared")

    # async def add(self, ctx, url):
    #     url = ' '.join(url)
    #     with youtube_dl.YoutubeDL(self.settings) as ydl:
    #         try:
    #             info = ydl.extract_info(url, download=False)
    #         except:
    #             info = ydl.extract_info(f"ytsearch:{url}",
    #                                     download=False)['entries'][0]
    #
    #     url = info['formats'][0]['url']
    #     name = info['title']
    #     time = str(datetime.timedelta(seconds=info['duration']))
    #     self.queue.q_add([name, time, url])
    #     embed = discord.Embed(description=f'Записываю [{name}]({url}) в очередь 📝',
    #                           colour=discord.Colour.red())
    #     await ctx.message.reply(embed=embed)
    #
    # def step_and_remove(self, voice_client):
    #     if loop_flag:
    #         songs_queue.q_add(songs_queue.get_value()[0])
    #     songs_queue.q_remove()
    #     if not voice_client.is_playing() and songs_queue.get_value():
    #         voice_client.play(discord.FFmpegPCMAudio(
    #             executable="ffmpeg\\bin\\ffmpeg.exe",
    #             source=songs_queue.get_value()[0][2],
    #             **self.ffmpeg_settings),
    #             after=lambda e: self.step_and_remove(voice_client))
    #
    # async def play(self, ctx, url):
    #     await self.add(ctx, ' '.join(url))
    #     await ctx.message.add_reaction(emoji='🎸')
    #     voice_client = ctx.guild.voice_client
    #     if not voice_client.is_playing() and songs_queue.get_value():
    #         voice_client.play(discord.FFmpegPCMAudio(
    #             executable="ffmpeg\\bin\\ffmpeg.exe",
    #             source=songs_queue.get_value()[0][2],
    #             **self.ffmpeg_settings),
    #             after=lambda e: self.step_and_remove(voice_client))


# @bot.event
# async def on_ready():
#     print('Status: online')
#     await bot.change_presence(activity=discord.Activity(
#         type=discord.ActivityType.listening, name='советы пьяного бомжа'))

#########################[JOIN BLOCK]#########################

# @bot.command(aliases=['j', 'J', 'jn', 'JN', 'Jn', 'о', 'О', 'от', 'ОТ', 'От',
#                       'сюда', 'СЮДА', 'Сюда', 'присоединись', 'ПРИСОЕДИНИСЬ',
#                       'Присоединись', 'Присоединиться', 'ПРИСОЕДИНИТЬСЯ',
#                       'присоединиться', 'ощшт', 'Ощшт', 'ОЩШТ', 'Join', 'JOIN'])


# @bot.command(aliases=['Disconnect', 'DISCONNECT', 'DC', 'dc', 'Dc', 'Disc',
#                       'disc', 'DISC', 'leave', 'Leave', 'LEAVE', 'Дисконнект',
#                       'ДИСКОННЕКТ', 'дисконнект', 'откл', 'ОТКЛ', 'Откл',
#                       'отключись', 'ОТКЛЮЧИСЬ', 'Отключись', 'отключиться',
#                       'ОТКЛЮЧИТЬСЯ', 'Отключиться', 'вшысщттусе', 'Вшысщттусе',
#                       'ВШЫСЩТТУСЕ', 'ВС', 'вс', 'Вс', 'Вшыс', 'вшыс', 'ВШЫС',
#                       'дуфму', 'Дуфму', 'ДУФМУ', 'Выйди', 'ВЫЙДИ', 'выйди',
#                       'кыш', 'КЫШ', 'Кыш', 'уйди', 'Уйди', 'УЙДИ', 'd', 'в'])


# @bot.command()
#
# def audio_player_task(voice_client):
#     if not voice_client.is_playing() and songs_queue.get_value():
#         voice_client.play(discord.FFmpegPCMAudio(
#             executable="ffmpeg\\bin\\ffmpeg.exe",
#             source=songs_queue.get_value()[0][2],
#             **FFMPEG_OPTIONS),
#             after=lambda e: step_and_remove(voice_client))

#
# @bot.command(aliases=['Play', 'PLAY', 'играй', 'ИГРАЙ', 'Играй', 'сыграй',
#                       'Сыграй', 'СЫГРАЙ', 'здфн', 'Здфн', 'ЗДФН', 'p', 'P',
#                       'pl', 'PL', 'Pl', 'з', 'З', 'зд', 'ЗД', 'Зд', 'Плей',
#                       'ПЛЕЙ', 'плей'])
#
#
# @bot.command()
# async def loop(ctx):
#     global loop_flag
#     loop_flag = True
#     await ctx.message.reply('Залуплено')
#
#
# @bot.command()
# async def unloop(ctx):
#     global loop_flag
#     loop_flag = False
#     await ctx.message.reply('Отлуплено')
#
#
# @bot.command(aliases=['Queue', 'QUEUE', 'йгугу', 'Йгугу', 'ЙГУГУ', 'очередь',
#                       'Очередь', 'ОЧЕРЕДЬ', 'список', 'Список', 'СПИСОК',
#                       'list', 'List', 'LIST', 'дшые', 'Дшые', 'ДШЫЕ', 'Лист',
#                       'лист', 'ЛИСТ', 'песни', 'Песни', 'ПЕСНИ', 'songs',
#                       'Songs', 'SONGS', 'ыщтпы', 'ЫЩТПЫ', 'Ыщтпы', 'q'])
# async def queue(ctx):
#     if len(songs_queue.get_value()) > 0:
#         only_names_and_time_queue = []
#         for i in songs_queue.get_value():
#             name = i[0]
#             if len(i[0]) > 30:
#                 name = i[0][:30] + '...'
#             only_names_and_time_queue.append(f'📀 `{name:<33}   {i[1]:>20}`\n')
#         c = 0
#         queue_of_queues = []
#         while c < len(only_names_and_time_queue):
#             queue_of_queues.append(only_names_and_time_queue[c:c + 10])
#             c += 10
#
#         embed = discord.Embed(title=f'ОЧЕРЕДЬ [LOOP: {loop_flag}]',
#                               description=''.join(queue_of_queues[0]),
#                               colour=discord.Colour.red())
#         await ctx.send(embed=embed)
#
#         for i in range(1, len(queue_of_queues)):
#             embed = discord.Embed(description=''.join(queue_of_queues[i]),
#                                   colour=discord.Colour.red())
#             await ctx.send(embed=embed)
#     else:
#         await ctx.send('Очередь пуста 📄')
#
#
# @bot.command(aliases=['ps', 'wait', 'wt', 'stop', 'стоп', 'пауза'])
# async def pause(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     if voice:
#         voice.pause()
#         await ctx.message.reply('Шо ты сделал? Порвал струну. Без неё играй!')
#
#
# @bot.command(aliases=['rs', 'continue', 'cnt', 'ct', 'продолжить'])
# async def resume(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     if voice:
#         if voice.is_paused():
#             voice.resume()
#             await ctx.message.reply('Поменял струну.')
#
#
# @bot.command(aliases=['sk', 'next', 'следующая', 'скип', 'скипнуть'])
# async def skip(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     if voice:
#         voice.stop()
#
#
# @bot.command(aliases=['cl', 'очистить', 'c'])
# async def clear(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     if voice:
#         voice.stop()
#         while not songs_queue.is_empty():
#             songs_queue.q_remove()
#
#
# @bot.command(aliases=['rem', 'r', 'удалить'])
# async def remove(ctx, index):
#     try:
#         if len(songs_queue.get_value()) > 0:
#             index = int(index) - 1
#             if index >= 0:
#                 d = songs_queue.q_rem_by_index(index)[0]
#                 await ctx.message.reply(f'Вычеркнул из списка: {d}')
#         else:
#             await ctx.message.reply('Нечего удалять')
#     except:
#         await ctx.message.reply(f'Песни с таким индексом не существует')
#
#
# bot.run(settings['token'])
