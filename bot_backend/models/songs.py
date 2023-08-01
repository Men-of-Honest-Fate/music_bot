# TODO: Добавить абстрактный класс композиции и плейлиста, добавить реализацию для каждого сервиса
from abc import ABC
from discord import VoiceChannel


class BaseSong(ABC):
    song_info: dict = {}
    voice_channel: VoiceChannel = None
