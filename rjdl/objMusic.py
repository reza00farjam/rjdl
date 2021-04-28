import requests
from bs4 import BeautifulSoup


class Music:
    """This object represents a RadioJvan music.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`url` is equal.

    .. versionadded:: 1.0.0

    Args:
        url (:obj:`str`): Music url.
        quality (:obj:`str`, optional): Music quality ('256' or '320').

    Attributes:
        artist (:obj:`str`): Music artist.
        name (:obj:`str`): Music name.
        url (:obj:`str`): Music url.
        cover (:obj:`str`): Music cover url.
        likes (:obj:`str`): Music likes on RadioJavan.
        plays (:obj:`str`): Music plays on RadioJavan.
        date_added (:obj:`str`): Date that music was added on RadioJavan.
        quality (:obj:`str`): Music quality.
        lyrics (:obj:`str`): Music lyrics. None, if no lyrics was available.
        details (:obj:`str`): Music details on RadioJavan. None, if no details was available.
        tags (:obj:`dict`): Music tags on RadioJavan. Names as keys and urls as values.
        download_link (:obj:`str`): Music direct download link.
        size (:obj:`str`): Size of music direct download link file.

    Raises:
        :class:`ValueError`
        :class:`ConnectionError`
    """

    def __init__(self, url: str, quality: str = "320"):
        try:
            response = requests.get(url, allow_redirects=True)
            url = response.url
            content = response.content

            if not url.startswith("https://www.radiojavan.com/mp3s/mp3/"):
                raise ValueError("Invalid url!")

            if '?' in url:
                url = url.split('?')[0]
            self.url = url

            if quality not in ["256", "320"]:
                raise ValueError("This quality isn't available!")
            self.quality = quality

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "songInfo"})
            self.artist, self.name = data[0].text.strip().split("\n")

            data = BeautifulSoup(content, "html.parser").findAll("img", href=False, attrs={"class": "cover"})
            self.cover = data[0]["src"]

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "lyricsContainer"})
            lyrics = data[0].prettify().replace("<br/>", '').splitlines()[2:-4]
            self.lyrics = "\n".join(lyrics)
            if "No lyrics yet" in self.lyrics:
                self.lyrics = None

            data = BeautifulSoup(content, "html.parser").findAll("span", href=False, attrs={"class": "rating"})
            self.likes = data[0].text.split()[0]

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "views"})
            self.plays = data[0].text.split(':')[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "dateAdded"})
            self.date_added = data[0].text.split(':')[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "mp3Description"})
            details = data[0].prettify().replace("<br/>", '').replace("&amp;", '&').splitlines()[7:-1]
            self.details = "\n".join([line.strip() for line in details])
            if not self.details.strip():
                self.details = None

            data = BeautifulSoup(content, "html.parser").findAll("span", href=False, attrs={"class": "tags"})
            self.tags = {tag.a.text: tag.a["href"] for tag in data}

            file_name = self.url.split('/')[-1]

            response = requests.post("https://www.radiojavan.com/mp3s/mp3_host", params={"id": file_name})
            self.download_link = f"{response.json()['host']}/media/mp3/mp3-{self.quality}/{file_name}.mp3"

            header = requests.head(self.download_link, allow_redirects=True)
            self.size = str(round(int(header.headers["Content-Length"].strip()) / 1048675.44, 2))
        except requests.exceptions.SSLError:
            raise ValueError("Invalid url!") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection!") from None

    def __eq__(self, other):
        if not isinstance(other, Music):
            return False
        return self.url == other.url
