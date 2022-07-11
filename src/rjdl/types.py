from enum import Enum


class MusicQuality(str, Enum):
    """This enum represents music qualities."""

    q320 = "320"
    q256 = "256"


class VideoQuality(str, Enum):
    """This enum represents video qualities."""

    q480 = "480"
    q720 = "720"
    q1080 = "1080"


class URLType(str, Enum):
    """This enum represents URL types."""

    MUSIC = "mp3s/mp3"
    VIDEO = "videos/video"
    ALBUM = "mp3s/album"
    PODCAST = "podcasts/podcast"
    PLAYLIST = "playlists/playlist"
