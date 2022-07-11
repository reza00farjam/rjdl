from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup as bs

from .base import URLBase


@dataclass(frozen=True, eq=False)
class Music(URLBase):
    """This class represents a music from Radio Javan

    Attributes:
        url (:obj:`str`): Music url.
        artist (:obj:`str`): Music artist.
        name (:obj:`str`): Music name.
        cover (:obj:`str`): Music cover url.
        likes (:obj:`str`): Music likes on RadioJavan.
        plays (:obj:`str`): Music plays on RadioJavan.
        date_added (:obj:`str`): Date that music was added on Radio Javan.
        lyrics (:obj:`str`): Music lyrics. None, if no lyrics was available.
        details (:obj:`str`): Music details on RadioJavan. None, \
            if no details was available.
        tags (:obj:`dict`): Music tags on RadioJavan. Names as keys and urls as values.
    """

    artist: str
    name: str
    cover: str
    likes: str
    plays: str
    date_added: str
    lyrics: str | None
    details: str | None
    tags: dict[str]

    def parse(soup: bs, url: str) -> Music:
        """Parse music from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): The music page.
            url (:obj:`str`): Music url.

        Returns:
            :obj:`Music`: Music object.
        """

        data = soup.find("div", href=False, attrs={"class": "songInfo"})
        artist, name = data.text.strip().split("\n")[:2]

        data = soup.find("img", href=False, attrs={"class": "cover"})
        cover = data["src"]

        data = soup.find("div", href=False, attrs={"class": "lyricsContainer"})
        lyrics = data.prettify().replace("<br/>", "").splitlines()[2:-4]
        lyrics = "\n".join(lyrics)
        if "No lyrics yet" in lyrics:
            lyrics = None

        data = soup.find("span", href=False, attrs={"class": "rating"})
        likes = data.text.split()[0]

        data = soup.find("div", href=False, attrs={"class": "views"})
        plays = data.text.split(":")[1].strip()

        data = soup.find("div", href=False, attrs={"class": "dateAdded"})
        date_added = data.text.split(":")[1].strip()

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

        data = soup.findAll("span", href=False, attrs={"class": "tags"})
        tags = {tag.a.text: tag.a["href"] for tag in data}

        return Music(
            url, artist, name, cover, likes, plays, date_added, lyrics, details, tags
        )
