import requests
from bs4 import BeautifulSoup
from rjdl.objMusic import Music


class Playlist:

    """This object represents a RadioJvan playlist.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`id` is equal.

    .. versionadded:: 1.0.0

    Args:
        url (:obj:`str`): Playlist url.
        quality (:obj:`str`, optional): Playlist quality ('256' or '320').

    Attributes:
        id (:obj:`str`): Playlist id.
        creator (:obj:`str`): Playlist creator.
        name (:obj:`str`): Playlist name.
        url (:obj:`str`): Playlist url.
        cover (:obj:`str`): Playlist cover url.
        length (:obj:`str`): Playlist length.
        quality (:obj:`str`): Playlist quality.
        followers (:obj:`str`): Playlist followers on RadioJavan.

    Raises:
        :class:`ValueError`
        :class:`ConnectionError`
    """

    def __init__(self, url: str, quality: str = "320"):
        try:
            response = requests.get(url, allow_redirects=True)
            url = response.url
            content = response.content

            if not url.startswith("https://www.radiojavan.com/playlists/playlist/"):
                raise ValueError("Invalid url!")

            if '?' in url:
                url = url.split('?')[0]
            self.url = url

            if quality not in ["256", "320"]:
                raise ValueError("This quality isn't available!")
            self.quality = quality

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "songInfo"})
            self.name = data[0].text.strip().split('\n')[0]
            self.creator = data[0].text.strip().split('\n')[1][11:-2]
            self.followers = data[0].text.strip().split('|')[-1].strip().split()[0]

            data = BeautifulSoup(content, "html.parser").findAll("img", href=False)
            self.cover = data[-1]["src"]

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "songInfo"})
            self.id = self.url.split("/")[-1]
            self.__tracks = [f"playlist_start?id={self.id}&index={i}" for i in range(len(data)-1)]
            self.length = len(self.__tracks)
        except requests.exceptions.SSLError:
            raise ValueError("Invalid url!") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection!") from None

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.id == other.id

    def track(self, index: int) -> Music:

        """
        Args:
            index (:obj:`int`): Index of desired playlist track.

        Returns:
            :class:`rjdl.Music`

        Raises:
            :class:`IndexError`
            :class:`ConnectionError`
        """

        return Music("https://www.radiojavan.com/mp3s/" + self.__tracks[index], self.quality)
