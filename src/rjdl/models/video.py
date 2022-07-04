from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from .base import URLBase


@dataclass(frozen=True, eq=False)
class Video(URLBase):

    """This class represents a Radio Javan video.

    Objects of this class are comparable in terms of equality.
    Two objects of this class are
    considered equal, if their :attr:`url` is equal.

    Attributes:
        url (:obj:`str`): Video url.
        artist (:obj:`str`): Video artist.
        name (:obj:`str`): Video name.
        thumb (:obj:`str`): Video thumbnail url.
        likes (:obj:`str`): Video likes on RadioJavan.
        plays (:obj:`str`): Video plays on RadioJavan.
        date_added (:obj:`str`): Date that video was added on RadioJavan.
        tags (:obj:`dict`): Video tags on RadioJavan. Names as keys and urls as values.
        director (:obj:`dict`): Video director. None, if director wasn't specified.
    """

    artist: str
    name: str
    thumb: str
    likes: str
    plays: str
    date_added: str
    tags: dict[str]
    director: dict[str] | None

    def parse(soup: bs, url: str) -> Video:
        """Parse video from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): BeautifulSoup object.
            url (:obj:`str`): Video url.

        Returns:
            :obj:`Video`: Video object.
        """

        data = soup.find("div", href=False, attrs={"class": "songInfo"})
        artist, name = data.text.strip().split("\n")[:2]

        data = soup.find("meta", href=False, attrs={"itemprop": "thumbnailUrl"})
        thumb = data.attrs["content"]

        data = soup.find("span", href=False, attrs={"class": "rating"})
        likes = data.text.split()[0]

        data = soup.find("div", href=False, attrs={"class": "views"})
        plays = data.text.split(":")[1].strip()

        data = soup.find("div", href=False, attrs={"class": "date_added"})
        date_added = data.text.split(":")[1].strip()

        data = soup.findAll("span", href=False, attrs={"class": "tags"})
        tags = {tag.a.text: tag.a["href"] for tag in data}

        data = soup.find("div", href=False, attrs={"id": "directed_by"})
        director = None if not data else data.text.split(":")[-1].strip()

        return Video(url, artist, name, thumb, likes, plays, date_added, tags, director)
