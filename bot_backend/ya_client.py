from yandex_music import ClientAsync
from .settings import get_ya_acc_info
import asyncio

settings = get_ya_acc_info()
client = asyncio.run(ClientAsync(get_ya_acc_info().YMToken).init())
client.request.set_timeout(30)
