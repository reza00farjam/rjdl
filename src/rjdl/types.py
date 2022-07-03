from enum import Enum


class MusicQuality(str, Enum):
    """This enum represents music qualities."""

    q320 = "320"
    q256 = "256"


class VideoQuality(str, Enum):
    """This enum represents video qualities."""

    q480 = "480p"
    q720 = "720p"
    q1080 = "1080p"


class URLType(str, Enum):
    """This enum represents URL types."""

    MUSIC = "mp3s/mp3"
    VIDEO = "videos/video"
    ALBUM = "mp3s/albums"
    PODCAST = "podcasts/podcast"
    PLAYLIST = "playlists/playlist"
