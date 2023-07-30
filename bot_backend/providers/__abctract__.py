from abc import ABC, abstractmethod
from ...settings import get_mpeg_settings


class BaseProvider(ABC):
    @abstractmethod
    def __init__(self):
        self.ctx = None
        self.ffmpeg_settings: dict = get_mpeg_settings().__dict__()

    @abstractmethod
    def add(self, *args):
        pass

    @abstractmethod
    def play(self, *args):
        pass

    @abstractmethod
    def parse(self, *args):
        pass

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