from abc import ABC, abstractmethod
from bot_backend.models.songs import BaseSong


class BaseProvider(ABC):
    song_queue: list[BaseSong] = []

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def play(self, ctx, *args):
        pass

    @abstractmethod
    async def parce(self, item):
        pass

    async def get_queue(self):
        return self.song_queue

    # TODO: Передвинуть функционал join/leave в commands.py
    # @staticmethod
    # async def join(ctx):
    #     if ctx.message.author.voice:
    #         if not ctx.voice_client:
    #             await ctx.message.author.voice.channel.connect(reconnect=True)
    #         else:
    #             await ctx.voice_client.move_to(ctx.message.author.voice.channel)
    #     else:
    #         await ctx.message.reply('❗ Вы должны находиться в голосовом канале ❗')
    #
    # @staticmethod
    # def disconnect(ctx):
    #     if ctx.voice_client:
    #         await ctx.voice_client.disconnect()
    #     else:
    #         pass
