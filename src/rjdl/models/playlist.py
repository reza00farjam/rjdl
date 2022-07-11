from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from .base import URLBase


@dataclass(frozen=True, eq=False)
class Playlist(URLBase):

    """This class represents a Radio Javan playlist.

    Objects of this class are comparable in terms of equality.
    Two objects of this class are considered equal, if their :attr:`url` is equal.

    Attributes:
        url (:obj:`str`): Playlist url.
        id (:obj:`str`): Playlist id.
        creator (:obj:`str`): Playlist creator.
        name (:obj:`str`): Playlist name.
        cover (:obj:`str`): Playlist cover url.
        followers (:obj:`str`): Playlist followers on RadioJavan.
        length (:obj:`int`): Playlist length.
        tracks (:obj:`list` of :obj:`str`): urls of playlist tracks.
    """

    id_: str
    creator: str
    name: str
    cover: str
    followers: str
    length: int
    tracks: list[str]

    def parse(soup: bs, url: str) -> Playlist:
        """Parse playlist from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): The playlist page.
            url (:obj:`str`): The playlist url.

        Returns:
            :obj:`Playlist`: Playlist object.
        """

        data = soup.find("div", href=False, attrs={"class": "songInfo"})
        name = data.text.strip().split("\n")[0]
        creator = data.text.strip().split("\n")[1][11:-2]
        followers = data.text.strip().split("|")[-1].strip().split()[0]

        data = soup.findAll("img", href=False)
        cover = data[-1]["src"]

        data = soup.findAll("div", href=False, attrs={"class": "songInfo"})
        id_ = url.split("/")[-1]
        __tracks = [f"playlist_start?id={id}&index={i}" for i in range(len(data) - 1)]
        length = len(__tracks)
        tracks = [f"https://www.radiojavan.com/mp3s/{i}" for i in __tracks]

        return Playlist(url, id_, creator, name, cover, followers, length, tracks)
