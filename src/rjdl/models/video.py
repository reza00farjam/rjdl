import requests
from bs4 import BeautifulSoup


class Video:

    """This object represents a RadioJvan video.

    Objects of this class are comparable in terms of equality.
    Two objects of this class are
    considered equal, if their :attr:`url` is equal.

    .. versionadded:: 1.0.0

    Args:
        url (:obj:`str`): Video url.
        quality (:obj:`str`, optional): Video quality ('480p', '720p' or '1080p').

    Attributes:
        artist (:obj:`str`): Video artist.
        name (:obj:`str`): Video name.
        url (:obj:`str`): Video url.
        thumb (:obj:`str`): Video thumbnail url.
        likes (:obj:`str`): Video likes on RadioJavan.
        plays (:obj:`str`): Video plays on RadioJavan.
        date_added (:obj:`str`): Date that video was added on RadioJavan.
        quality (:obj:`str`): Video quality.
        tags (:obj:`dict`): Video tags on RadioJavan. Names as keys and urls as values.
        director (:obj:`dict`): Video director. None, if director wasn't specified.
        download_link (:obj:`str`): Video direct download link.
        size (:obj:`str`): Size of video direct download link file.

    Raises:
        :class:`ValueError`
        :class:`ConnectionError`
    """

    def __init__(self, url: str, quality: str = "720p"):
        try:
            response = requests.get(url, allow_redirects=True)
            url = response.url
            content = response.content

            if not url.startswith("https://www.radiojavan.com/videos/video/"):
                raise ValueError("Invalid url!")

            data = BeautifulSoup(content, "html.parser").findAll(
                "ul", href=False, attrs={"class": ""}
            )
            if quality not in data[0].text.strip().lower().split("\n"):
                raise ValueError("This quality isn't available!")
            self.quality = quality
            self.url = url

            data = BeautifulSoup(content, "html.parser").findAll(
                "div", href=False, attrs={"class": "songInfo"}
            )
            self.artist, self.name = data[0].text.strip().split("\n")

            data = BeautifulSoup(content, "html.parser").findAll(
                "meta", href=False, attrs={"itemprop": "thumbnailUrl"}
            )
            self.thumb = data[0].attrs["content"]

            data = BeautifulSoup(content, "html.parser").findAll(
                "span", href=False, attrs={"class": "rating"}
            )
            self.likes = data[0].text.split()[0]

            data = BeautifulSoup(content, "html.parser").findAll(
                "div", href=False, attrs={"class": "views"}
            )
            self.plays = data[0].text.split(":")[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll(
                "div", href=False, attrs={"class": "date_added"}
            )
            self.date_added = data[0].text.split(":")[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll(
                "span", href=False, attrs={"class": "tags"}
            )
            self.tags = {tag.a.text: tag.a["href"] for tag in data}

            data = BeautifulSoup(content, "html.parser").findAll(
                "div", href=False, attrs={"id": "directed_by"}
            )
            self.director = None if not data else data[0].text.split(":")[-1].strip()

            file_name = self.url.split("/")[-1]

            response = requests.post(
                "https://www.radiojavan.com/videos/video_host", params={"id": file_name}
            )
            quality = (
                "lq"
                if self.quality == "480p"
                else "hq"
                if self.quality == "720p"
                else "hd"
            )
            self.download_link = (
                f"{response.json()['host']}/media/music_video/{quality}/{file_name}.mp4"
            )

            header = requests.head(self.download_link, allow_redirects=True)
            self.size = str(
                round(int(header.headers["Content-Length"].strip()) / 1048675.44, 2)
            )
        except requests.exceptions.SSLError:
            raise ValueError("Invalid url!") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection!") from None

    def __eq__(self, other):
        if not isinstance(other, Video):
            return False
        return self.url == other.url
