from abc import ABC, abstractmethod
from .songs import BaseSong, YA_Song
from bot_backend.ya_client import client
from typing import List


class BaseAlbum(ABC):
    @abstractmethod
    def __init__(self):
        pass


class YA_Album(BaseAlbum):
    def __init__(self, album_id) -> None:
        self.album_id = album_id
        self.tracks: List[BaseSong] = []
        self.title: str
        self.preview: str

    async def fetch_album(self):
        album = await client.albums_with_tracks(self.album_id)

        self.title = album.title
        self.preview = "https://" + album.og_image.replace("%%", "1000x1000")

        for track in album.volumes[0]:
            self.tracks.append(await YA_Song(track_object=track).fetch_track())

        return self
