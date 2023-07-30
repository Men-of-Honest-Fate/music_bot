from bot_backend.commands import bot
from settings import get_bot_settings
import discord

if __name__ == "__main__":
    # TODO: Разобраться нужен ли этот event флаг тут вообще
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening))

    bot.run(get_bot_settings().token)
