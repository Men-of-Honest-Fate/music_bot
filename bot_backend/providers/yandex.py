import re
import discord
import requests

from discord.utils import get
from bot_backend.settings import get_mpeg_settings
from bot_backend.models.songs import BaseSong
from .__abctract__ import BaseProvider
from ..ya_client import client


class Yandex(BaseProvider):
    def __init__(self):
        self.client = discord.Client()
        self.token = "your-discord-token"
        self.ym_token = "your-yandex-music-token"
        self.header = {'Authorization': f'OAuth {self.ym_token}'}
        self.ffmpeg_settings = get_mpeg_settings().__dict__()

    async def add(self, ctx, *args):
        pass

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

    async def play(self, ctx, *args):
        music_name = " ".join(args)
        await self.parce(music_name)

        self.vc = get(client.voice_clients, guild=ctx.guild)
        if not self.vc:
            await self.song_queue[0].voice_channel.connect()
        else:
            await self.vc.move_to(self.song_queue[0].voice_channel)

        if (
                not self.vc
                or not self.vc.is_playing()
        ):
            voice_client.play(discord.FFmpegPCMAudio(track_url), after=lambda e: self.play_next())
        await voice_client.disconnect()

    async def parce(self, query):
        music_url = f'https://api.music.yandex.net/search?type=track&text={query}'
        response = await requests.get(music_url, headers=self.header).json()
        track_id = response['result']['tracks'][0]['id']
        track_url = f'https://music.yandex.ru/album/{track_id}/track/{track_id}'
        song = BaseSong()
        song.voice_channel = self.vc
        song.song_info = {"source": track_url, "query": music_url}
        self.song_queue.append(song)

        # await ctx.response.send_message("Ожидайте...", ephemeral=True)
        # if ctx.user.voice:
        #     VM: VoiceManager = await GM.get_guild(ctx.user.voice.channel, ctx.channel)
        #     mediaItem = await fetch_link(track)
        #     if not mediaItem:
        #         await ctx.edit_original_response(content="По вашему запросу ничего не найдено!")
        #     else:
        #         if not VM.queue:
        #             VM.queue.append(mediaItem)
        #             try:
        #                 await add_to_queue_message(ctx, mediaItem)
        #             except:
        #                 ...
        #             await event_loop(VM)
        #             await GM.delete_guild(ctx.guild.id)
        #         else:
        #             if ctx.user.voice.channel == VM.voiceChannel:
        #                 VM.queue.append(mediaItem)
        #                 await add_to_queue_message(ctx, mediaItem)
        #             else:
        #                 await ctx.edit_original_response(content="Похоже бот уже где-то играет!")
        # else:
        #     await ctx.edit_original_response(
        #         content="Для выполнения этого действия вы должны находится в голосовом канале!"
        #     )
        # """Обработка полученной ссылки"""
        #
        # valid_url_pattern = r"https://music\.yandex\.ru"
        # pattern_playlist = r"/users/([^/]+)/playlists/(\d+)"
        # pattern_track = r"/album/(\d+)/track/(\d+)"
        # pattern_album = r"/album/(\d+)"
        # pattern_text = r"^(https://music\.yandex\.ru)?[^/]*$"
        #
        # match_valid_url = re.search(valid_url_pattern, link)
        # match_text = re.search(pattern_text, link)
        # if not match_valid_url and not match_text:
        #     return None  # Если ссылка не является допустимой ссылкой на Яндекс.Музыку, возвращаем None
        #
        # match_playlist = re.search(pattern_playlist, link)
        # match_track = re.search(pattern_track, link)
        # match_album = re.search(pattern_album, link)
        #
        # if match_playlist:
        #     user_id = match_playlist.group(1)
        #     playlist_id = match_playlist.group(2)
        #
        #     return await Playlist(user_id, playlist_id).fetch_playlist()
        #
        # elif match_track:
        #     album_id = match_track.group(1)
        #     track_id = match_track.group(2)
        #
        #     return await Track(album_id, track_id).fetch_track()
        #
        # elif match_album:
        #     album_id = match_album.group(1)
        #
        #     return await Album(album_id).fetch_album()
        #
        # elif match_text:
        #     mediaItem = await client.search(prompt)
        #
        #     if not mediaItem.tracks and not mediaItem.best:
        #         return None
        #     else:
        #         if isinstance(mediaItem.best.result, track):
        #             return await Track(track_object=mediaItem.best.result).fetch_track()
        #         elif isinstance(mediaItem.best.result, album):
        #             return await Album(mediaItem.best.result.id).fetch_album()
        #         elif isinstance(mediaItem.best.result, artist):
        #             return await Playlist(mediaItem.playlists.results[0].uid,
        #                                   mediaItem.playlists.results[0].kind).fetch_playlist()
        #         else:
        #             return None
        # else:
        #     return None
#
#
# direct = "tracks\\"
# bdDir = "database\\"
#
#
# def proc_captcha(captcha_image_url):
#     print(captcha_image_url["x_captcha_url"])
#     return input("Код с картинки: ")
#
#
# def logPassAuth():
#     log = input("Введите почту: ")
#     password = input("Введите пароль: ")
#     try:
#         client = Client.from_credentials(log, password, captcha_callback=proc_captcha)
#         return client
#     except:
#         print("Неверный логин, пароль или капча")
#         logPassAuth()
#
#
# def authorization():
#     # bdDir = 'database\\'
#     # print(os.path.exists(bdDir))
#     if os.path.exists(bdDir) == False:
#         os.mkdir("database")
#         conn = sqlite3.connect(f"{bdDir}YMbase.db")
#         cur = conn.cursor()
#         cur.execute(
#             """CREATE TABLE IF NOT EXISTS userInfo(
#                 userid INT PRIMARY KEY,
#                 YMtoken TEXT,
#                 display_name TEXT);
#                 """
#         )
#         conn.commit()
#         print("бд создана")
#         print(
#             "Вам необходимо единоразово войти в свой аккаунт яндекс для получения API токена."
#         )
#
#         logPassClient = logPassAuth()
#         # print(logPassClient)
#         token = logPassClient["token"]
#         uinfo = []
#         uinfo.append(logPassClient.accountStatus().account["uid"])
#         uinfo.append("None")
#         uinfo.append(logPassClient.accountStatus().account["display_name"])
#         # print(uinfo)
#         cur.execute("INSERT INTO userInfo VALUES(?, ?, ?);", uinfo)
#         conn.commit()
#         try:
#             client = Client.from_token(token)
#             print(client["token"])
#             print(uinfo[0])
#             cur.execute(
#                 """UPDATE userInfo set YMtoken = ? where userid = ?""",
#                 (f"{client['token']}", uinfo[0]),
#             )
#             conn.commit()
#             conn.close()
#             print("бд заполнена и закрыта")
#             print(f"{uinfo[2]}, токен успешно получен.")
#             return client
#
#         except:
#             print(
#                 "Ошибка авторизации по токену. Будет использована авторизация лог\пар"
#             )
#             conn.close()
#             return logPassAuth()
#     else:
#         conn = sqlite3.connect(f"{bdDir}YMbase.db")
#         cur = conn.cursor()
#         cur.execute("""SELECT * from userInfo""")
#         records = cur.fetchall()
#         conn.close()
#         print("ваш токен успешно считан:")
#         # print(records[0][1])
#         try:
#             print(records[0][1])
#             print("\n\n\n")
#             client = Client.from_token(records[0][1])
#             print(f"\n\n\n{records[0][2]}, авторизация по токену завершена\n\n\n")
#             return client
#         except:
#             print(
#                 "Ошибка авторизации по токену. Будет использована авторизация лог\пар"
#             )
#             return logPassAuth()
#
#
# type_to_name = {
#     "track": "трек",
#     "artist": "исполнитель",
#     "album": "альбом",
#     "playlist": "плейлист",
#     "video": "видео",
#     "user": "пользователь",
#     "podcast": "подкаст",
#     "podcast_episode": "эпизод подкаста",
# }
#
#
# def send_search_request_and_print_result(client, query):
#     search_result = client.search(query)
#
#     text = [f'Результаты по запросу "{query}":', ""]
#
#     best_result_text = ""
#     if search_result.best:
#         type_ = search_result.best.type
#         best = search_result.best.result
#
#         # print(best)
#         print(best.id)
#
#         if type_ in ["track", "podcast_episode"]:
#             artists = ""
#             if best.artists:
#                 artists = " - " + ", ".join(artist.name for artist in best.artists)
#
#             best_result_text = best.title + artists
#             path = direct + best_result_text + ".mp3"
#             best.download(path)
#             res = best_result_text + ".mp3"
#             return res
#     else:
#         print("трек не найден")
#         return "-1"
#
#
# def playlists_list(client):
#     alb_list = client.users_playlists_list()
#     user_playlists = client.users_playlists_list()
#     last_list = list(p.title for p in user_playlists)
#     last_list.append("likes")
#     last_list.append("плейлист дня")
#     return last_list
#
#
# def playlist_info(client, title_list):
#     user_playlists = client.users_playlists_list()
#     if title_list == "likes":
#         tracks = client.users_likes_tracks()
#         total_tracks = len(tracks.tracks)
#         return f"В очередь будет добавлено {total_tracks} track(s) из плейлиста liked tracks."
#     elif title_list == "плейлист дня":
#         PersonalPlaylistBlocks = client.landing(blocks=["personalplaylists"]).blocks[0]
#         DailyPlaylist = next(
#             x.data.data
#             for x in PersonalPlaylistBlocks.entities
#             if x.data.data.generated_playlist_type == "playlistOfTheDay"
#         )
#         total_tracks = DailyPlaylist.track_count
#         # print(DailyPlaylist)
#         return f"В очередь будет добавлен плейлист дня. {total_tracks} track(s)."
#     else:
#         playlist = next((p for p in user_playlists if p.title == title_list), None)
#         if playlist == None:
#             return f"playlist not found"
#         total_tracks = playlist.track_count
#         return f"В очередь будет добавлен плейлист {playlist.title}. {total_tracks} track(s)."
#
#
# def tracks_from_playlist(client, title_list):
#     # print(alb_list)
#     user_playlists = client.users_playlists_list()
#     # print('specify --playlist-name', list(p.title for p in user_playlists))
#
#     if title_list == "likes":
#         tracks = client.users_likes_tracks()
#         total_tracks = len(tracks.tracks)
#         print(f"Playing liked tracks. {total_tracks} track(s).")
#     elif title_list == "плейлист дня":
#         PersonalPlaylistBlocks = client.landing(blocks=["personalplaylists"]).blocks[0]
#         DailyPlaylist = next(
#             x.data.data
#             for x in PersonalPlaylistBlocks.entities
#             if x.data.data.generated_playlist_type == "playlistOfTheDay"
#         )
#         total_tracks = DailyPlaylist.track_count
#         # print(total_tracks)
#         tracks = (
#             DailyPlaylist.tracks
#             if DailyPlaylist.tracks
#             else DailyPlaylist.fetch_tracks()
#         )
#         # print(tracks)
#     else:
#         playlist = next((p for p in user_playlists if p.title == title_list), None)
#         if playlist == None:
#             print(f"playlist not found")
#         total_tracks = playlist.track_count
#         print(
#             f"Playing {playlist.title} ({playlist.playlist_id}). {total_tracks} track(s)."
#         )
#         tracks = playlist.tracks if playlist.tracks else playlist.fetch_tracks()
#         # print(tracks)
#
#     short_track_mass = []
#     for i, short_track in enumerate(tracks):
#         short_track_mass.append(short_track)
#         # print(i)
#     tracks_list = []
#     for i in range(0, total_tracks):
#         track = (
#             short_track_mass[i].track
#             if short_track_mass[i].track
#             else short_track_mass[i].fetchTrack()
#         )
#         # print(f'{track.title}_{track.artists[0].name}.mp3')
#         # tracks_list.append(f'{track.title}_{track.artists[0].name}.mp3')
#         tracks_list.append(f"{track.title} {track.artists[0].name}")
#
#     # print(tracks_list)
#     return tracks_list
#
#
# def albums_to_playlist(client, ALBUM_ID):
#     album = client.albums_with_tracks(ALBUM_ID)
#     tracks = []
#     for i, volume in enumerate(album.volumes):
#         if len(album.volumes) > 1:
#             tracks.append(f"💿 Диск {i + 1}")
#         tracks += volume
#     # print(tracks)
#     tracks_list = []
#     for track in tracks:
#         if isinstance(track, str):
#             # print(track)
#             tracks_list.append(track)
#         else:
#             artists = ""
#             if track.artists:
#                 artists = " - " + ", ".join(artist.name for artist in track.artists)
#             # print(track.title + artists)
#             tracks_list.append(track.title + artists)
#     # print(tracks_list)
#     text = "АЛЬБОМ\n\n"
#     text += f"{album.title}\n"
#     text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
#     tracks_list.append(text)
#     return tracks_list
#
#
# def add_to_likes(client, query):
#     search_result = client.search(query)
#     print(search_result)
#     if search_result.best:
#         best = search_result.best.result
#
#     # print(best)
#     print(best.id)
#     conn = sqlite3.connect(f"{bdDir}YMbase.db")
#     cur = conn.cursor()
#     cur.execute("""SELECT * from userInfo""")
#     records = cur.fetchall()
#     conn.close()
#     res = client.users_likes_tracks_add(best.id, records[0][0])
#     print(res)
#
#
# def remove_from_likes(client, query):
#     search_result = client.search(query)
#     print(search_result)
#     if search_result.best:
#         best = search_result.best.result
#
#     # print(best)
#     print(best.id)
#     conn = sqlite3.connect(f"{bdDir}YMbase.db")
#     cur = conn.cursor()
#     cur.execute("""SELECT * from userInfo""")
#     records = cur.fetchall()
#     conn.close()
#     res = client.susers_likes_tracks_remove(best.id, records[0][0])
#     print(res)
