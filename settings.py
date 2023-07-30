import os
import dotenv

dotenv.load_dotenv(".env")


class Bot_Settings:
    token: str = os.getenv("TOKEN")
    bot: str = "HonestMusicBot"
    id: str = os.getenv("ID")
    prefix: str = "/"


class FFMPEG_Settings:
    options: str = "-vn"
    before_options: str = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

    def __dict__(self):
        return {
            "options": self.options,
            "before_options": self.before_options,
        }


class YDL_Settings:
    format: str = "bestaudio/best"
    extractaudio: bool = True
    noplaylist: bool = True
    simulate: bool = True
    preferredquality: str = "192"
    preferredcodec: str = "mp3"
    key: str = "FFmpegExtractAudio"

    def __dict__(self):
        return {
            "format": self.format,
            "extractaudio": self.extractaudio,
            "noplaylist": self.noplaylist,
            "simulate": self.simulate,
            "preferredquality": self.preferredquality,
            "preferredcodec": self.preferredcodec,
            "key": self.key
        }


class YA_Account:
    login: str = os.getenv("LOGIN")
    password: str = os.getenv("PASS")

    def __dict__(self):
        return {
            "login": self.login,
            "password": self.password
        }


def get_bot_settings() -> Bot_Settings:
    settings = Bot_Settings()
    return settings


def get_mpeg_settings() -> FFMPEG_Settings:
    settings = FFMPEG_Settings()
    return settings


def get_youtube_settings() -> YDL_Settings:
    settings = YDL_Settings()
    return settings


def get_ya_acc_info() -> YA_Account:
    info = YA_Account()
    return info
