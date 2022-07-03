from __future__ import annotations

import ast
from dataclasses import dataclass

from bs4 import BeautifulSoup as bs
from .base import URLBase


@dataclass(frozen=True, eq=False)
class Album(URLBase):
    """This class represents a Radio Javan album.

    Objects of this class are comparable in terms of equality. Two objects of
    this class are considered equal, if their :attr:`url` is equal.

    Attributes:
        url (:obj:`str`): Album url.
        artist (:obj:`str`): Album artist.
        name (:obj:`str`): Album name.
        cover (:obj:`str`): Album cover url.
        date_added (:obj:`str`): Date that album was added on RadioJavan.
        length (:obj:`int`): Album length.
        tracks (:obj:`list` of :obj:`str`): urls of album tracks.
    """

    artist: str
    name: str
    cover: str
    date_added: str
    length: int
    tracks: list[str]

    def parse(soup: bs, url: str) -> Album:
        """Parse album from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): The album page.
            url (:obj:`str`): Album url.

        Returns:
            :obj:`Album`: Album object.
        """

        data = soup.find("meta", href=False, attrs={"property": "og:title"})
        artist, name = data.attrs["content"].split(" - ")

        data = soup.findAll("img", href=False)
        cover = data[-1]["src"]

        data = soup.find("div", href=False, attrs={"class": "dateAdded"})
        date_added = data.text.split(":")[1].strip()

        data = soup.findAll("script", href=False)
        __tracks = ast.literal_eval(str(data[-3]).split("\n")[11][17:-1])
        length = len(__tracks)
        tracks = [f"https://www.radiojavan.com/mp3s/mp3/{i}" for i in __tracks]

        return Album(url, artist, name, cover, date_added, length, tracks)
