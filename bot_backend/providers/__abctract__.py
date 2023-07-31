from abc import ABC, abstractmethod

class BaseProvider(ABC):
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