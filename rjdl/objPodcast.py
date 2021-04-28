import requests
from bs4 import BeautifulSoup


class Podcast:
    """This object represents a RadioJvan podcast.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`url` is equal.

    .. versionadded:: 1.0.0

    Args:
        url (:obj:`str`): Podcast url.

    Attributes:
        artist (:obj:`str`): Podcast artist.
        name (:obj:`str`): Podcast name.
        url (:obj:`str`): Podcast url.
        cover (:obj:`str`): Podcast cover url.
        likes (:obj:`str`): Podcast likes on RadioJavan.
        plays (:obj:`str`): Podcast plays on RadioJavan.
        date_added (:obj:`str`): Date that podcast was added on RadioJavan.
        quality (:obj:`str`): Podcast quality.
        tracklist (List[:obj:`str`]): Podcast tracklist.
        details (:obj:`str`): Podcast details on RadioJavan. None, if no details was available.
        tags (:obj:`dict`): Podcast tags on RadioJavan. Names as keys and urls as values.
        download_link (:obj:`str`): Podcast direct download link.
        size (:obj:`str`): Size of Podcast direct download link file.

    Raises:
        :class:`ValueError`
        :class:`ConnectionError`
    """

    def __init__(self, url: str):
        try:
            response = requests.get(url, allow_redirects=True)
            url = response.url
            content = response.content

            if not url.startswith("https://www.radiojavan.com/podcasts/podcast/"):
                raise ValueError("Invalid url!")

            if '?' in url:
                url = url.split('?')[0]
            self.url = url
            self.quality = "192"

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "songInfo"})
            self.name, self.artist = data[0].text.strip().split("\n")

            data = BeautifulSoup(content, "html.parser").findAll("img", href=False, attrs={"class": "cover"})
            self.cover = data[0]["src"]

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"id": "tracklist"})
            if data:
                tracklist = data[0].ul.prettify().replace("</li>", '').replace("<li>", '').replace("&amp;", '&')
                self.tracklist = list(filter(lambda x: x, [track.strip() for track in tracklist.split("\n")[2: -3]]))
            else:
                self.tracklist = []

            data = BeautifulSoup(content, "html.parser").findAll("span", href=False, attrs={"class": "rating"})
            self.likes = data[0].text.split()[0]

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "views"})
            self.plays = data[0].text.split(':')[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "dateAdded"})
            self.date_added = data[0].text.split(':')[1].strip()

            data = BeautifulSoup(content, "html.parser").findAll("span", href=False, attrs={"class": "tags"})
            self.tags = {tag.a.text: tag.a["href"] for tag in data}

            data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "mp3Description"})
            details = data[0].prettify().replace("<br/>", '').replace("&amp;", '&').splitlines()[7:-1]
            self.details = "\n".join([line.strip() for line in details])
            if not self.details.strip():
                self.details = None

            file_name = self.url.split('/')[-1]

            response = requests.post("https://www.radiojavan.com/podcasts/podcast_host", params={"id": file_name})
            self.download_link = f"{response.json()['host']}/media/podcast/mp3-192/{file_name}.mp3"

            header = requests.head(self.download_link, allow_redirects=True)
            self.size = str(round(int(header.headers["Content-Length"].strip()) / 1048675.44, 2))
        except requests.exceptions.SSLError:
            raise ValueError("Invalid url!") from None
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Check your connection!") from None

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.url == other.url
