from .yandex import Yandex
from .youtube import Youtube
from .spotify import Spotify
from .exceptions import ProviderNotSupported


def convert(*args):
    convert: dict = {
        "yandex": Yandex(),
        "youtube": Youtube(),
        "spotify": Spotify()
    }
    try:
        return convert[args[0]]
    except KeyError:
        raise ProviderNotSupported
