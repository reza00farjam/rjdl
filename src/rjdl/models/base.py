from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from bs4 import BeautifulSoup as bs


@dataclass(frozen=True, eq=False)
class URLBase(ABC):
    """This class is base class for all models.
    It contains only one attribute :attr:`url` which is url of the model.
    """

    url: str

    def __eq__(self, other):
        if not isinstance(other, URLBase):
            return False
        return self.url == other.url

    @abstractmethod
    def parse(self, soup: bs, url: str) -> URLBase:
        """Parse model from BeautifulSoup object.

        Args:
            soup (:obj:`bs4.BeautifulSoup`): BeautifulSoup object.
            url (:obj:`str`): Url of the model.

        Returns:
            :obj:`URLBase`: Model object.
        """
        pass
