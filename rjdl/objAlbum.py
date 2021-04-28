import requests
from bs4 import BeautifulSoup
from rjdl.objMusic import Music


class Album:
    """
    This object represents a RadioJvan album.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`url` is equal.

    .. versionadded:: 1.0.0

    Args:
        url (:obj:`str`): Album url.
        quality (:obj:`str`, optional): Album quality ('256' or '320').

    Attributes:
        artist (:obj:`str`): Album artist.
        name (:obj:`str`): Album name.
        url (:obj:`str`): Album url.
        cover (:obj:`str`): Album cover url.
        length (:obj:`str`): Album length.
        quality (:obj:`str`): Album quality.
        date_added (:obj:`str`): Date that album was added on RadioJavan.

    Raises:
            :class:`ValueError`
            :class:`ConnectionError`
    """

    def __init__(self, url: str, quality: str = "320"):
        try:
            response = requests.get(url, allow_redirects=True)
            url = response.url
            content = response.content

            if not url.startswith("https://www.radiojavan.com/mp3s/album/"):
                raise ValueError("Invalid url!")

            if '?' in url:
                url = url.split('?')[0]
            self.url = url

            if quality not in ["256", "320"]:
                raise ValueError("This quality isn't available!")
            self.quality = quality

            data = BeautifulSoup(content, "html.parser").findAll("meta", href=False, attrs={"property": "og:title"})
            self.artist, self.name = data[0].attrs["content"].split(" - ")

            data = BeautifulSoup(content, "html.parser").findAll("img", href=False)
            self.cover = data[-1]["src"]

            data = BeautifulSoup(content, "html.parser").findAll("script", href=False)
            self.__tracks = eval(str(data[-3]).split("\n")[11][17:-1])
            self.length = len(self.__tracks)

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "dateAdded"})
            self.date_added = data[0].text.split(':')[1].strip()
        except requests.exceptions.SSLError:
            raise ValueError("Invalid url!") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection!") from None

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.url == other.url

    def track(self, index: int) -> Music:
        """
        Args:
            index (:obj:`int`): Index of desired album track.

        Returns:
            :class:`rjdl.Music`

        Raises:
            :class:`IndexError`
            :class:`ConnectionError`
        """

        return Music("https://www.radiojavan.com/mp3s/mp3/" + self.__tracks[index]["mp3"], self.quality)
