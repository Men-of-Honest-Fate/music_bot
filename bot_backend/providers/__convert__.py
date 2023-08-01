from .exceptions import ProviderNotSupported
from .spotify import Spotify
from .yandex import Yandex
from .youtube import Youtube


def convert(*args):
    convert: dict = {"yandex": Yandex(), "youtube": Youtube(), "spotify": Spotify()}
    try:
        return convert[args[0]]
    except KeyError:
        raise ProviderNotSupported
