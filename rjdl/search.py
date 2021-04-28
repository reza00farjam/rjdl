import requests
from bs4 import BeautifulSoup


def search(string: str) -> dict:

    """Searches given string in RadioJavan database and return a dictionary of founded results.

    Args:
        string (:obj:`str`): String to be searched.

    Returns:
        :obj:`dict`

    Raises:
        :class:`ConnectionError`
    """

    content = requests.get("https://www.radiojavan.com/search", params={"q": string}).content

    data = BeautifulSoup(content, "html.parser").findAll("div", href=False, attrs={"class": "itemContainer"})
    items = {item.a.attrs["href"]: {"artist": item.text.strip().split("\n")[0],
                                    "name": item.text.strip().split("\n")[1]}
             for item in data}

    return {"music": dict(filter(lambda x: x[0].startswith("/mp3s/mp3/"), items.items())),
            "video": dict(filter(lambda x: x[0].startswith("/videos/video/"), items.items())),
            "album": dict(filter(lambda x: x[0].startswith("/mp3s/album/"), items.items())),
            "podcast": dict(filter(lambda x: x[0].startswith("/podcasts/podcast/"), items.items()))}
