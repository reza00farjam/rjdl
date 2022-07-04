import os
import time
from urllib import parse
from abc import ABC, abstractmethod

import requests
from .models import Album, Music, Playlist, Podcast, Video
from .types import MusicQuality, URLType, VideoQuality

from bs4 import BeautifulSoup as bs


class DownloadCallback(ABC):
    """Abstract class for implementing callbacks for `DownloadManager`"""

    @abstractmethod
    def on_fetching(self, url: str):
        """Called when starting to fetch data from url."""
        pass

    @abstractmethod
    def on_fetched(self, data):
        """Called when a url has been fetched."""
        pass

    @abstractmethod
    def on_downloading(self, dl_url: str, dl_size: int):
        """Called when starting to downloading."""
        pass

    @abstractmethod
    def on_progress(self, progress: float, speed: float):
        """Called when downloading progress.

        Args:
            progress: Progress in percentage (between 0 and 100).
            speed: Download speed in bytes/second.
        """
        pass

    @abstractmethod
    def on_downloaded(self, path: str):
        """Called when a url has been downloaded."""
        pass


class DownloadManager:
    """Manage process of downloading urls

    Args:
        `urls`: List of urls to download.
        `path`: Path to save the files.
        `music_quality`: Quality of the musics.
        `video_quality`: Quality of the videos.
        `info`: If True, just print info about the url and don't download anything.
    """

    def __init__(
        self,
        urls: list[str],
        path: str = "",
        music_quality: MusicQuality = MusicQuality.q320,
        video_quality: VideoQuality = VideoQuality.q720,
        info: bool = False,
    ):
        self.path = path
        self.music_quality = music_quality
        self.video_quality = video_quality
        self.info = info

        self._queue: list[str] = urls
        self._callbacks: list[DownloadCallback] = []

        # Create path if it doesn't exist
        # It will use default path if the given path wasn't accessible
        if not os.path.exists(self.path):
            if not os.access(os.path.dirname(self.path), os.W_OK):
                self.path = ""
            else:
                os.mkdir(self.path)

        # Create a requests session
        self.s = requests.Session()

    def add_callback(self, callback: DownloadCallback):
        """Add a callback to the list of callbacks.
        After adding a callback, it automatically will be called.

        Args:
            callback (:obj:`DownloadCallback`): The callback to add.
        """
        self._callbacks.append(callback)

    def start(self):
        """Start process of fetching and downloading for all urls in the queue."""
        for item in self._queue:
            self._fetch(item)

    def _fetch(self, url: str) -> None:
        """Fetch data for a url.

        Raises:
            `ValueError`: If the url is not a valid url.
        """
        any(c.on_fetching(url) for c in self._callbacks)

        response = self.s.get(url, allow_redirects=True)
        url = response.url
        content = response.content

        url = parse.urlparse(url)
        if url.scheme != "https":
            url = url._replace(scheme="https")

        if url.netloc != "www.radiojavan.com":
            raise ValueError(f"The url {url.geturl()} is not a valid RadioJavan url.")

        # Remove other parts of url
        url = parse.urlparse(url.scheme + "://" + url.netloc + url.path)

        try:
            path = url.path.split("/")[1:3]
            path = "/".join(path)
            type_ = URLType(path)
        except IndexError:
            raise ValueError(
                "Path must be one of the: " + ", ".join([str(t) for t in URLType])
            )

        url = url.geturl()
        soup = bs(content, "html.parser")

        match type_:
            case URLType.ALBUM:
                data = Album.parse(soup, url)
                urls = data.tracks
            case URLType.MUSIC:
                data = Music.parse(soup, url)
                urls = [data.url]
            case URLType.PLAYLIST:
                data = Playlist.parse(soup, url)
                urls = data.tracks
            case URLType.PODCAST:
                data = Podcast.parse(soup, url)
                urls = [data.url]
            case URLType.VIDEO:
                data = Video.parse(soup, url)
                urls = [data.url]
            case _:
                raise ValueError(f"Unknown url type: {type_}")

        any(c.on_fetched(data) for c in self._callbacks)

        if not self.info:
            for url in urls:
                dl_link = self._get_dl_link(url, type_)
                self._download(dl_link)

    def _get_dl_link(self, url: str, type_: URLType) -> str:
        """Get the download link from `radiojavan.com`.

        Args:
            url (:obj:`str`): The url to get the download link for.
            type_ (:obj:`URLType`): The type of the url.

        Raises:
            `ValueError`: If the url is not a valid url.

        Returns:
            `str`: The download link.
        """
        name = url.split("/")[-1]

        def get_dl_host(host: str) -> str:
            response = self.s.post(host, params={"id": name})
            return response.json()["host"]

        match type_:
            case URLType.MUSIC:
                dl_host = get_dl_host("https://www.radiojavan.com/mp3s/mp3_host")
                download_link = (
                    f"{dl_host}/media/mp3/mp3-" + f"{self.music_quality}/{name}.mp3"
                )
            case URLType.PODCAST:
                dl_host = get_dl_host(
                    "https://www.radiojavan.com/podcasts/podcast_host"
                )
                download_link = f"{dl_host}/media/podcast/mp3-192/{name}.mp3"
            case URLType.VIDEO:
                match self.video_quality:
                    case VideoQuality.q480:
                        q = "lq"
                    case VideoQuality.q720:
                        q = "hq"
                    case VideoQuality.q1080:
                        q = "hd"
                dl_host = get_dl_host("https://www.radiojavan.com/videos/video_host")
                download_link = f"{dl_host}/media/music_video/{q}/{name}.mp4"
            case _:
                raise ValueError(
                    f"For getting the download link, the url {url} is not a valid url."
                )

        return download_link

    def _download(self, url: str) -> None:
        """Downloads given direct download link.

        Args:
            url (:obj:`str`): Valid downloadable url.

        Raises:
            :class:`BrokenPipeError`
            :class:`ConnectionError`
            :class:`FileExistsError`
        """
        file_name = url.split("/")[-1]
        file_path = os.path.abspath(self.path) + "/" + file_name
        if os.path.isfile(file_path):
            raise FileExistsError(f"File {file_path} already exists.")

        print(url)

        with open(file_path, "wb") as file:
            try:
                response = self.s.get(url, allow_redirects=True, stream=True)
                total_length = response.headers["Content-Length"]

                if total_length is None:
                    file.write(response.content)
                else:
                    total_length = int(total_length.strip())
                    any(c.on_downloading(url, total_length) for c in self._callbacks)
                    dl = 0
                    start = time.perf_counter()

                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        file.write(data)

                        done = 100 * dl / total_length
                        speed = round((dl / (time.perf_counter() - start)), 2)

                        any(c.on_progress(done, speed) for c in self._callbacks)

                    any(c.on_downloaded(self.path + file_name) for c in self._callbacks)
            except Exception as e:
                file.close()
                os.remove(self.path + file_name)
                raise e from None
