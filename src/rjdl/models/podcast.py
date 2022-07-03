from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from .base import URLBase


@dataclass(frozen=True, eq=False)
class Podcast(URLBase):

    """This class represents a Radio Javan podcast.

    Objects of this class are comparable in terms of equality.
    Two objects of this class are considered equal, if their :attr:`url` is equal.

    Attributes:
        url (:obj:`str`): Podcast url.
        artist (:obj:`str`): Podcast artist.
        name (:obj:`str`): Podcast name.
        cover (:obj:`str`): Podcast cover url.
        likes (:obj:`str`): Podcast likes on RadioJavan.
        plays (:obj:`str`): Podcast plays on RadioJavan.
        date_added (:obj:`str`): Date that podcast was added on RadioJavan.
        details (:obj:`str`): Podcast details on RadioJavan.\
            None, if details wasn't available.
        tags (:obj:`dict`): Podcast tags on RadioJavan.\
            Names as keys and urls as values.
        tracks (List[:obj:`str`]): Tracks of podcast.
    """

    artist: str
    name: str
    cover: str
    likes: str
    plays: str
    date_added: str
    details: str
    tags: dict[str]
    tracks: list[str]

    def parse(soup: bs, url: str) -> Podcast:
        """Parse podcast from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): BeautifulSoup object.
            url (:obj:`str`): Podcast url.

        Returns:
            :obj:`Podcast`: Podcast object.
        """

        data = soup.find("div", href=False, attrs={"class": "songInfo"})
        name, artist = data.text.strip().split("\n")

        data = soup.find("img", href=False, attrs={"class": "cover"})
        cover = data["src"]

        data = soup.find("div", href=False, attrs={"id": "tracklist"})
        if data:
            tracks = (
                data.ul.prettify()
                .replace("</li>", "")
                .replace("<li>", "")
                .replace("&amp;", "&")
            )
            tracks = list(
                filter(
                    lambda x: x,
                    [track.strip() for track in tracks.split("\n")[2:-3]],
                )
            )
        else:
            tracks = []

        data = soup.find("span", href=False, attrs={"class": "rating"})
        likes = data.text.split()[0]

        data = soup.find("div", href=False, attrs={"class": "views"})
        plays = data.text.split(":")[1].strip()

        data = soup.find("div", href=False, attrs={"class": "dateAdded"})
        date_added = data.text.split(":")[1].strip()

        data = soup.findAll("span", href=False, attrs={"class": "tags"})
        tags = {tag.a.text: tag.a["href"] for tag in data}

        data = soup.find("div", href=False, attrs={"class": "mp3Description"})
        details = (
            data.prettify()
            .replace("<br/>", "")
            .replace("&amp;", "&")
            .splitlines()[7:-1]
        )
        details = "\n".join([line.strip() for line in details])
        if not details.strip():
            details = None

        return Podcast(
            url, artist, name, cover, likes, plays, date_added, details, tags, tracks
        )
